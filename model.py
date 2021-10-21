import numpy as np
import pandas as pd
import math
from enum import Enum

import config


class ErrorType(Enum):
    MEAN_ABSOLUTE_ERR = 0
    MEAN_SQUARED_ERR = 1


class EquationModel(object):
    def __init__(self,
                 discharge=config.DATA_DISCHARGE,
                 radius=config.DATA_RADIUS,
                 data_file=config.DATA_FILE_PATH):
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
        for count in range(1, config.THEIS_MAX_ITERATIONS+1):
            new_fac = math.pow(self._ut/t, count)/ (count * math.factorial(count))
            if new_fac < config.THEIS_CALC_LIMIT:
                break
            wu -= math.pow(-1, count%2)*new_fac
        return wu

    def get_error(self, errtype = ErrorType.MEAN_ABSOLUTE_ERR):
        if errtype is ErrorType.MEAN_ABSOLUTE_ERR:
            err = (self.estimated_drawdown - self.data.drawdown).map(abs).mean()
        elif errtype is ErrorType.MEAN_SQUARED_ERR:
            err = (self.estimated_drawdown - self.data.drawdown).map(
                lambda x: x*x
            ).mean()
        return err
