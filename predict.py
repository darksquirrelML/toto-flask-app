from tensorflow import keras
import numpy as np
import pandas as pd
from db import supabase


# -------------------------
# Load data from Supabase
# -------------------------
def load_data():

    response = supabase.table("toto_results") \
        .select("*") \
        .order("draw_no", desc=True) \
        .limit(1000) \
        .execute()

    df = pd.DataFrame(response.data)

    # Convert string → list of numbers
    df['Winning'] = df['winning_no'].apply(
        lambda x: [int(i) for i in str(x).split(',')]
    )

    return df


# -------------------------
# Convert to ML input
# -------------------------


def draws_to_multihot(df):

    X = []

    for _, row in df.iterrows():

        v = np.zeros(49)

        # main numbers
        for n in row['Winning']:
            v[int(n) - 1] = 1

        # additional number
        if row['additional_no']:

            add_no = int(row['additional_no'])
            v[add_no - 1] = 1

        X.append(v)

    return np.array(X)

# -------------------------
# Prediction function
# -------------------------
def predict_numbers():

    print("STEP 1: Load data from Supabase")
    df = load_data()

    print("STEP 2: Convert to multihot")
    data_X = draws_to_multihot(df)

    window_size = 15

    if len(data_X) < window_size:
        return ["Not enough data"]

    print("STEP 3: Load model")
    model = keras.models.load_model("lstm_model.h5")

    print("STEP 4: Prepare input")
    last_seq = data_X[-window_size:]
    inp = last_seq.reshape((1, window_size, 49))

    print("STEP 5: Predict")
    pred = model.predict(inp)[0]

    # Select top 7 numbers
    numbers = np.argsort(pred)[-7:] + 1

    print("FINAL PREDICTION:", numbers)

    return sorted(numbers.tolist())

