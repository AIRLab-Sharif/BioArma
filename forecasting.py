import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks

def predict(x,y,x_p):
    reg = LinearRegression().fit(x, y)
    regressed = reg.predict(x_p.reshape(1, len(x_p)))[0]
    max_indxs = findMaxs(regressed)
    return regressed, max_indxs

def findMaxs(sigg):
    return find_peaks(sigg)
