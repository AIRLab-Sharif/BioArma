import numpy as np
from scipy.signal import butter,filtfilt


def LPFilter(time, data):
    try:
        fs = 50
        cutoff = 1
        nyq = 0.5 * fs
        order = 4      
        filtered_data = butter_lowpass_filter(data, cutoff, nyq, order)
    except Exception as e:
        print(e)
        filtered_data = data
    return filtered_data

def butter_lowpass_filter(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y
