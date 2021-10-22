import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
import os

from model import EquationModel, ErrorType
import config

model = EquationModel()

s_poss = np.logspace(config.PARA_MIN_LOG_S, config.PARA_MAX_LOG_S, 200)
t_poss = np.logspace(config.PARA_MIN_LOG_T, config.PARA_MAX_LOG_T, 100)

# filled these by looking at the solution
s_poss2 = np.logspace(-4.3, -4.4, 200)
t_poss2 = np.logspace(.7, .78, 100)

LEN = len(t_poss) * len(s_poss)
errs = np.zeros(shape=(len(t_poss), len(s_poss)))
errs2 = np.zeros(shape=(len(t_poss2), len(s_poss2)))

for si in range(len(s_poss)):
    for ti in range(len(t_poss)):
        model.set_aquifer_properties(s_poss[si], t_poss[ti])
        err = model.get_error()
        if err > 20:
            err = 22
        errs[ti, si]=err

for si in range(len(s_poss2)):
    for ti in range(len(t_poss2)):
        model.set_aquifer_properties(s_poss2[si], t_poss2[ti])
        err = model.get_error()
        # if err > .20:
        #     err = .22
        errs2[ti, si]=err


if not os.path.exists("./data"):
    os.mkdir("./data")
np.save("./data/field.npy", errs)
np.save("./data/field-zoom.npy", errs2)
print('Fields saved to ./data directory.')
