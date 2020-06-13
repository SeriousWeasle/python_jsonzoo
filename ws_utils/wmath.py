import math

def mapRange(value, min_val, max_val, min_out, max_out):
    try:
        out = (((value - min_val)/(max_val-min_val))*(max_out-min_out)) + min_out
    except: out = max_out
    return out