#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template
from predict import predict

app = Flask(__name__)

@app.route("/predict")
def run_prediction():

    numbers = predict()

    return render_template("prediction.html", numbers=numbers)

