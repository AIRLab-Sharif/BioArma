import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

def predict(x,y,x_p):
    reg = LinearRegression().fit(x, y)
    normalized = preprocessing.normalize(reg.predict(x_p.reshape(1, len(x_p))))
    normalized = reg.predict(x_p.reshape(1, len(x_p)))
    return normalized[0]