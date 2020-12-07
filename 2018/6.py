#!/usr/bin/env python3
# coding: utf-8

import numpy as np
from collections import Counter

def manhattan_distance(a: tuple, b: tuple) -> 'distance':  # (lasso) "taxicab-metric"
    return abs((a[0]-b[0]) + (a[1]-b[1]))


with open('6.data', 'r') as file:
    points = sorted([
        (
            int(line.replace(' ', '').strip().split(',')[0]),
            int(line.replace(' ', '').strip().split(',')[1])
        )
        for line in file.readlines()
        ], key=lambda x: x[1])

# getting area size
grid = []
for y in range(1000):
    row = []
    for x in range(1000):
        point_distance = []
        for point in points:
            point_distance.append(manhattan_distance((x, y), point))
        point_distance = np.array([p if p != 0 else np.nan for p in point_distance])

        row.append(str(point_distance.tolist().index(np.nanmin(point_distance))))
    grid.append(row)

c = Counter(coord for rows in grid for coord in set(rows))
p = c.most_common(1)[0][0]
size = c.most_common(1)[0][1]
print(f'Task One: Index of point {points[int(p)]} is {p} and the size of his area is {size}')
