#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, jsonify, redirect, request

import pandas as pd
from db import supabase
from predict import predict_numbers

from train import train
from flask import redirect, request

import progress

app = Flask(__name__)

@app.route('/progress')

# def get_progress():
#     return jsonify(training_status)
def get_progress():
    return jsonify(progress.training_status)




@app.route('/last-trained')
def last_trained():
    # your code here
    return {"last_trained": "..."}



def load_data():
    response = (supabase.table("toto_results")
        .select("*")
        .order("draw_no", desc=True)
        .limit(1000) 
        .execute())

    df = pd.DataFrame(response.data)

    # ✅ ADD THIS LINE
    df = df[::-1].reset_index(drop=True)

    df['Winning'] = df['winning_no'].apply(
        lambda x: [int(i) for i in str(x).split(',')]
    )

    return df

from scraper import scrape_toto_latest, update_supabase

@app.route("/update")
def update_data():

    draws = scrape_toto_latest()
    update_supabase(draws)

    # return render_template("train.html", message="Data updated successfully!")
    return redirect("/trends?updated=1")


from datetime import datetime

@app.route('/last-updated')
def last_updated():
    response = supabase.table("toto_results") \
        .select("draw_date") \
        .order("draw_date", desc=True) \
        .limit(1) \
        .execute()

    if response.data:
        last_time = response.data[0]["draw_date"]
    else:
        last_time = None

    return {"last_updated": last_time}


import threading

@app.route("/train")
def run_training():
    thread = threading.Thread(target=train)
    thread.start()

    return {"status": "training started"}



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict")
def run_prediction():
    numbers = predict_numbers()
    return render_template("prediction.html", numbers=numbers)


@app.route("/trends")
def trends():
    df = load_data()
    df = df[::-1]
    return render_template("trends.html", tables=df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)

