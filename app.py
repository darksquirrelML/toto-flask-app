import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import requests
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
import tensorflow as tf

# 👉 Limit CPU usage (VERY important for Render)
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

app = Flask(__name__)

MODEL_PATH = "lstm_model.h5"
MODEL_URL = "https://fcibqtbavrltcvzhfgjy.supabase.co/storage/v1/object/public/models/lstm_model.h5"

# 👉 Lazy load model (prevents startup crash)
model = None

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        r = requests.get(MODEL_URL, timeout=60)
        r.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)
        print("Download complete")

def get_model():
    global model
    if model is None:
        print("Loading model...")
        download_model()
        model = load_model(MODEL_PATH, compile=False)
        print("Model loaded successfully")
    return model

# 👉 Home page
@app.route("/")
def home():
    return "App is running"

# 👉 API prediction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json["input"]
        data = np.array(data).reshape(1, -1)

        prediction = get_model().predict(data)

        return jsonify({
            "prediction": prediction.tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 👉 HTML form (optional)
@app.route("/predict_form", methods=["POST"])
def predict_form():
    try:
        raw = request.form["input"]
        data = [float(x) for x in raw.split(",")]
        data = np.array(data).reshape(1, -1)

        prediction = get_model().predict(data)

        return f"Prediction: {prediction.tolist()}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
