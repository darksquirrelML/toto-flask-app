#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from db import supabase


# -------------------------
# Load data
# -------------------------
def load_data():

    response = supabase.table("toto_results") \
        .select("*") \
        .order("draw_no", desc=True) \
        .limit(1000) \
        .execute()

    df = pd.DataFrame(response.data)

    df['Winning'] = df['winning_no'].apply(
        lambda x: [int(i) for i in str(x).split(',')]
    )

    return df

import progress

from datetime import datetime


def train_model(model, epochs, X, y):

    progress.training_status["status"] = "training"
    progress.training_status["progress"] = 0

    for epoch in range(epochs):

        print(f"Epoch {epoch+1}/{epochs}")

        # model.fit(X, y, epochs=1, batch_size=32, verbose=1)
        history = model.fit(X, y, epochs=1, batch_size=32, verbose=1)

        loss = history.history['loss'][0]
        acc = history.history.get('binary_accuracy', [0])[0]


        progress.training_status["loss"] = round(loss, 4)
        progress.training_status["accuracy"] = round(acc, 4)

        progress_value = int(((epoch + 1) / epochs) * 100)
        progress.training_status["progress"] = progress_value

        print(progress.training_status)

        # time.sleep(0.2)

    progress.training_status["status"] = "completed"

    supabase.table("model_meta").upsert({
        "id": 1,
        "last_trained": datetime.now().isoformat()
    }).execute()



# -------------------------
# Convert to multihot
# -------------------------
def draws_to_multihot(df):

    X = []

    for _, row in df.iterrows():

        v = np.zeros(49)

        for n in row['Winning']:
            v[n-1] = 1

        if row['additional_no']:
            v[int(row['additional_no'])-1] = 1

        X.append(v)

    return np.array(X)


# -------------------------
# Build model
# -------------------------
def build_model(window_size, features=49):

    model = keras.Sequential([
        layers.Input(shape=(window_size, features)),
        layers.LSTM(128),
        layers.Dense(64, activation='relu'),
        layers.Dense(features, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['binary_accuracy']
    )

    return model


# -------------------------
# Train model
# -------------------------
# def train():

#     print("TRAIN FUNCTION STARTED")   # 👈 ADD THIS


#     df = load_data()

#     data_X = draws_to_multihot(df)

#     window_size = 15

#     sequences = []
#     targets = []

#     for i in range(len(data_X) - window_size):
#         sequences.append(data_X[i:i+window_size])
#         targets.append(data_X[i+window_size])

#     sequences = np.array(sequences)
#     targets = np.array(targets)

#     model = build_model(window_size)

#     print("Training model...")
#     model.fit(sequences, targets, epochs=20, batch_size=32)

#     model.save("lstm_model.h5")

#     print("Model saved as lstm_model.h5")


def train():

    print("TRAIN FUNCTION STARTED")

    df = load_data()
    data_X = draws_to_multihot(df)

    window_size = 15

    sequences = []
    targets = []

    for i in range(len(data_X) - window_size):
        sequences.append(data_X[i:i+window_size])
        targets.append(data_X[i+window_size])

    sequences = np.array(sequences)
    targets = np.array(targets)

    model = build_model(window_size)

    print("Training model...")

    # ✅ USE THIS (important)
    train_model(model, epochs=50, X=sequences, y=targets)

    model.save("lstm_model.h5")

    print("Model saved as lstm_model.h5")

