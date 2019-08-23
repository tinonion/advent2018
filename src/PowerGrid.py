import numpy as np


class PowerGrid:
    def __init__(self, size, serial):
        self.size = size
        self.grid = np.empty((size, size))
        self.serial = serial

        self.set_power_cells()

    def power_level(self, x, y):
        grid_serial = self.serial

        rack_id = x + 10
        pwr = (rack_id * y + grid_serial) * rack_id
        pwr = int(str(pwr)[-3])
        return pwr - 5

    def set_power_cells(self):
        size = self.size

        for x in range(size):
            for y in range(size):
                self.grid[x, y] = self.power_level(x, y)

    def get_power_cell(self, x, y):
        return self.grid[x, y]

    def region_edges(self, x, y, region_size):
        size = self.size
        right = x + region_size
        top = y + region_size

        if right >= size or top >= size:
            # how outside the bounds the most outside bound is
            shrink = max(right, top) - size + 1

            right -= shrink
            top -= shrink

        top_edge = self.grid[x:right, top]
        right_edge = self.grid[right, y:top]
        top_right_corner = self.grid[right, top]
        return np.sum(top_edge) + np.sum(right_edge) + top_right_corner
