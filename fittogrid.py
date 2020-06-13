import math
from ws_utils import mapRange
from PIL import Image

grid = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]]

shape = [
    [1,0,1],
    [0,0,1],
    [0,1,0]
]

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if x + len(shape[0]) <= len(grid[0]) and y + len(shape) <= len(grid):
            for sy in range(len(shape)):
                for sx in range(len(shape[sy])):
                    cx = sx + x
                    cy = sy + y
                    if shape[sy][sx] == 1:
                        grid[cy][cx] += 1

max_n = 0
for r in grid:
    for n in r:
        max_n = max(max_n, n)

out = Image.new("RGB", (5,5), 0)
pixels = out.load()

for y in range(len(grid)):
    for x in range(len(grid[y])):
        pixels[x, y] = (int(mapRange(grid[y][x], 0, max_n, 0, 255)), 0, 0)

out = out.resize((250, 250), resample=Image.NEAREST)
out.show()

print(grid)