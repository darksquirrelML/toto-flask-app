#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tensorflow import keras
import numpy as np

def predict():

    model = keras.models.load_model("lstm_model.h5")

    pred = model.predict(...)

    return pred

