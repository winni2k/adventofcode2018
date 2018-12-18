from itertools import chain

import numpy as np


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


class GridPopulator:

    def __init__(self, min_x, min_y, max_x, max_y, points):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.points = points
        self.x = np.array([p[0] for p in points])
        self.y = np.array([p[1] for p in points])

    def find_dist_to_all_points(self, i, j):
        dist_x = abs(self.x - i)
        dist_y = abs(self.y - j)
        return dist_x + dist_y

    def find_nearest_point(self, i, j):
        dist = self.find_dist_to_all_points(i, j)
        min_idx = np.argmin(dist)
        num_min = sum(dist == dist[min_idx])
        if num_min == 1:
            return min_idx
        else:
            return -1


lines = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".splitlines()
lines = open('input.txt').readlines()

points = sorted(tuple(map(int, l.strip().split(','))) for l in lines)

min_x = min(points, key=lambda p: p[0])
max_x = max(points, key=lambda p: p[0])
min_y = min(points, key=lambda p: p[1])
max_y = max(points, key=lambda p: p[1])
print(min_x[0], max_x[0], min_y[1], max_y[1])

delta_x = min_x[0]
delta_y = min_y[1]
adj_max_x = max_x[0] - delta_x
adj_max_y = max_y[1] - delta_y
adj_points = [(p[0] - delta_x, p[1] - delta_y) for p in points]
print(f'adjusted max x and y: {adj_max_x}, {adj_max_y}')

grid = np.zeros((adj_max_x + 1, adj_max_y + 1), dtype=np.int)

adj_point_set = set(adj_points)
populator = GridPopulator(0, 0, adj_max_x, adj_max_y, adj_point_set)
for i in range(adj_max_x + 1):
    for j in range(adj_max_y + 1):
        grid[i, j] = sum(populator.find_dist_to_all_points(i, j))

print(sum(1 for _ in filter(lambda p: p < 10000, grid.flatten())))
