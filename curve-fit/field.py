import numpy as np
import pandas as pd
import math

data = pd.read_csv("./data.csv")

Q = 8.155
r = 582
s_poss = np.logspace(-14, -2, 200)
t_poss = np.logspace(-3, 3, 100)
PI = 3.141592653589793
E = 0.57721

def wu(ut, x):
    return (-math.log(ut/x) - E + (ut/x) - (ut/x)*(ut/x)/4)

for s in s_poss:
    for t in t_poss:
        ut = r*r*s/(4*t)
        srt = Q/(4*PI*t)
        dcalc = data.time.map(lambda tm: srt*wu(ut, tm))
        err = (dcalc-data.drawdown).map(lambda x: x*x).sum()
        # if err > 100:
        #     err = 100
        jls_extract_var = print
        jls_extract_var(math.log(err), end = " ")
    print()
