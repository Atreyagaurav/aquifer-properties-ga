from collections import namedtuple

import numpy as np
import scipy.ndimage.filters as filters

Point = namedtuple("Point", "x y")

GRID_COLUMNS = 10
GRID_ROWS = 10
DEFAULT_WATER_HEAD = 100

WELL_POSITIONS = [
    Point(2,3),
    Point(6,8)
]

CONTAMINANTS = {
    Point(5,5): 20,
    Point(7,5): 15
}


class AquiferSystem:
    def __init__(self,
                 shape:(int,int)=(GRID_COLUMNS, GRID_ROWS),
                 water_head:float=DEFAULT_WATER_HEAD,
                 wells:list[Point]=[],
                 contaminant:{Point:float}={},
                  ):
        # initialize well locations
        self.shape = shape
        self.wells = np.zeros(shape, int)
        for point in wells:
            self.wells[point.x, point.y] = 1

        # initialize groundwater levels
        self.groundwater_level = np.zeros(shape, int)

        # initialize contaminant position and concentrations
        self.contaminant = np.zeros(shape, int)
        for point, conc in contaminant.items():
            self.contaminant[point.x, point.y] = conc

    def contaminant_dispersion(self):
        self.contaminant = filters.gaussian_filter(
            self.contaminant,
            5)

    def show_contaminants(self):
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                print(f'{self.contaminant[row,col]:3.2f}',
                      end= ' ')
            print()
        


syst = AquiferSystem(wells=WELL_POSITIONS,
                    contaminant=CONTAMINANTS)

syst.show_contaminants()
syst.contaminant_dispersion()
