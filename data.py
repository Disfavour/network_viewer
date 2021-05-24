import netCDF4 as nc
import numpy as np


class Data:
    def __init__(self, path):
        self.dataset = nc.Dataset(path)

    def get_3d_array(self):
        return self.dataset["data"][:]

    def get_dimensions(self):
        l = []
        for item in self.dataset.dimensions:
            l.append(item)
        return l

    def get_variables(self):
        l = []
        for item in self.dataset.variables:
            l.append(item)
        return l


if __name__ == "__main__":
    pass
    #a = Data("datasets/20111209 Lomonosov-1/network_average.nc")