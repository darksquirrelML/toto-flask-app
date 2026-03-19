import numpy as np

def predict_numbers():
    return list(np.random.choice(range(1, 50), 7, replace=False))
