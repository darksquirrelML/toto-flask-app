#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import requests
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model

app = Flask(__name__)

MODEL_PATH = "lstm_model.h5"

MODEL_URL = "https://fcibqtbavrltcvzhfgjy.supabase.co/storage/v1/object/public/models/lstm_model.h5"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        r = requests.get(MODEL_URL)
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)

# Load model once
download_model()
model = load_model(MODEL_PATH)

# 👉 HTML page
@app.route("/")
def home():
    return render_template("index.html")

# 👉 API
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["input"]
    data = np.array(data).reshape(1, -1)
    prediction = model.predict(data)

    return jsonify({
        "prediction": prediction.tolist()
    })

# 👉 HTML form submit
@app.route("/predict_form", methods=["POST"])
def predict_form():
    raw = request.form["input"]

    data = [float(x) for x in raw.split(",")]
    data = np.array(data).reshape(1, -1)

    prediction = model.predict(data)

    return f"Prediction: {prediction.tolist()}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# if __name__ == "__main__":
#     app.run()

