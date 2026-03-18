#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tensorflow import keras
import pandas as pd

def train_model(df):

    model = keras.Sequential()

    # your LSTM architecture

    model.fit(...)

    model.save("lstm_model.h5")

