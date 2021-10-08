import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
import os

from model import EquationModel, ErrorType

model = EquationModel(8.155, 582, "./data.csv")

s_poss = np.logspace(-14, -2, 200)
t_poss = np.logspace(-3, 3, 100)

# print(f'ncols\t{len(t_poss)}')
# print(f'nrows\t{len(s_poss)}')
# print('xllcorner\t0')
# print('yllcorner\t0')
# print('cellsize\t1')
# print('NODATA_value\t-999')

errs = np.zeros(shape=(len(t_poss), len(s_poss)))

for si in range(len(s_poss)):
    for ti in range(len(t_poss)):
        model.set_aquifer_properties(s_poss[si], t_poss[ti])
        err = model.get_error()
        if err > 20:
            err = 22
        errs[ti, si]=err


if not os.path.exists("./data"):
    os.mkdir("./data")
np.save("./data/field.npy", errs)
plt.pcolormesh(errs)
plt.show()

