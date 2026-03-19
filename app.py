#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# from flask import Flask, render_template
# from predict import predict

# app = Flask(__name__)

# @app.route("/predict")
# def run_prediction():

#     numbers = predict()

#     return render_template("prediction.html", numbers=numbers)


# In[ ]:


from flask import Flask, render_template
from predict import predict_numbers

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def run_prediction():
    numbers = predict_numbers()
    return render_template("prediction.html", numbers=numbers)

if __name__ == "__main__":
    app.run(debug=True)

