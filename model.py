import numpy as np
import pandas as pd
import math
from enum import Enum


CALC_LIMIT = 1e-4
MAX_ITERATIONS = 10


class ErrorType(Enum):
    MEAN_ABSOLUTE_ERR = 0
    MEAN_SQUARED_ERR = 1


class EquationModel(object):
    def __init__(self, discharge, radius, data_file):
        self.data = pd.read_csv(data_file)
        self.pumping_discharge = discharge
        self.radius = radius

    def set_aquifer_properties(self, storativity, trasnmissivity):
        self.storativity = storativity
        self.trasnmissivity = trasnmissivity
        self._srt_coeff = self.pumping_discharge / (4 * math.pi * self.trasnmissivity)
        self._E = 0.57721
        self._ut = self.radius * self.radius * self.storativity / (4 * self.trasnmissivity)
        self.estimated_drawdown = self.data.time.map(lambda tm: self._srt_coeff * self._get_wu(tm))

    def _get_wu(self, t):
        wu = -math.log(self._ut/t) - self._E
        for count in range(1, MAX_ITERATIONS+1):
            new_fac = math.pow(self._ut/t, count)/ (count * math.factorial(count))
            if new_fac < CALC_LIMIT:
                break
            wu -= math.pow(-1, count%2)*new_fac
        return wu

    def get_error(self, errtype = ErrorType.MEAN_ABSOLUTE_ERR):
        if errtype is ErrorType.MEAN_ABSOLUTE_ERR:
            err = (self.estimated_drawdown - self.data.drawdown).map(abs).sum()
        elif errtype is ErrorType.MEAN_SQUARED_ERR:
            err = (self.estimated_drawdown - self.data.drawdown).map(
                lambda x: x*x
            ).sum()
        return err
    
        

