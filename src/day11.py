import math
from functools import partial

import numpy as np

from PowerGrid import PowerGrid

GRID_SIZE = 300


def power_level(x, y, serial):
    rack_id = x + 10
    pwr = (rack_id * y + serial) * rack_id
    pwr = pwr // 100 % 10
    return pwr - 5


def region_edges(x, y, sel_size, pwr_grid):
    right = x + sel_size
    top = y + sel_size

    top_edge = pwr_grid[x:right, top]
    right_edge = pwr_grid[right, y:top]
    top_right_corner = pwr_grid[right, top]
    return np.sum(top_edge) + np.sum(right_edge) + top_right_corner


def find_sum_arr(serial, sel_cap=GRID_SIZE):
    power_fun = partial(power_level, serial=serial)

    pwr_grid = np.fromfunction(power_fun, (GRID_SIZE, GRID_SIZE))

    sum_arr = np.empty((GRID_SIZE, GRID_SIZE, sel_cap))
    sum_arr[:, :, 0] = pwr_grid

    for x in range(GRID_SIZE):
        print("x: {}".format(x))

        for y in range(GRID_SIZE):
            for sel_size in range(1, sel_cap):
                if x + sel_size >= GRID_SIZE or y + sel_size >= GRID_SIZE:
                    sum_arr[x, y, sel_size] = np.nan
                    continue

                edge_sum = region_edges(x,
                                        y,
                                        sel_size,
                                        pwr_grid)

                sel_sum = sum_arr[x, y, sel_size - 1] + edge_sum

                sum_arr[x, y, sel_size] = sel_sum

    return sum_arr


def part1(serial):
    sel_cap = 3
    sum_arr = find_sum_arr(serial, sel_cap)[:, :, 2]
    location = np.where(sum_arr == np.nanmax(sum_arr))
    return (location[0][0], location[1][0])


def part2(serial, sel_cap=GRID_SIZE):
    sum_arr = find_sum_arr(serial, sel_cap)
    location = np.where(sum_arr == np.nanmax(sum_arr))
    return (location[0][0], location[1][0], location[2][0] + 1)


if __name__ == "__main__":
    assert power_level(122, 79, 57) == -5
    assert power_level(217, 196, 39) == 0
    assert power_level(101, 153, 71) == 4

#    assert part1(18) == (33, 45)
#    assert part1(42) == (21, 61)

#    assert part2(18, 20) == (90, 269, 16)
#    assert part2(42) == (232, 251, 12)

    serial = 6878
    print("part 1: {}\npart 2: {}".format(part1(serial), part2(serial)))
