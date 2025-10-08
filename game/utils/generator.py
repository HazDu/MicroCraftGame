import random
import __main__ as main

from utils.util_functs import *


def generate_tree(queue, chunk):
    blocks = [
        [[-1, -4], 11], [[0, -4], 11], [[1, -4], 11],
        [[-2, -3], 11], [[-1, -3], 11], [[0, -3], 10], [[1, -3], 11], [[2, -3], 11],
        [[-2, -2], 11], [[-1, -2], 11], [[0, -2], 10], [[1, -2], 11], [[2, -2], 11],
        [[0, -1], 10],
        [[0, 0], 10],
    ]
    for coords in queue:
        for block in blocks:
            _x = coords[0] + block[0][0]
            _y = coords[1] + block[0][1]

            chunk_checked = change_block_over_border(chunk, _x, _y)
            _x = chunk_checked[1]
            _y = chunk_checked[2]
            chunk_checked = chunk_checked[0]

            if chunk_checked != -1:
                main.loaded_chunks[chunk_checked][0][_x][_y] = block[1]


def create_chunk():
    return [[0 for _ in range(64)] for _ in range(64)]

def generate_chunk(chunk):
    contents = []
    tree_queue = []
    for y in range(64):
        row = []
        for x in range(64):
            if random.randint(0, 100) == 0:
                main.tree_queue[chunk].append([x, y])
            row.append(random.randint(2, 2))
        contents.append(row)
    main.loaded_chunks[chunk][0] = contents
