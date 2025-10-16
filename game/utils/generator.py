import random
import __main__ as main

from utils.util_functs import *

def generate_chunk_type(chunk, worldtype):
    match worldtype:
        case 0:
            generate_chunk_2d_flat(chunk)
        case _:
            generate_chunk(chunk)

def generate_tree(x, y, chunk):
    blocks = [
        [[-1, -4], 11], [[0, -4], 11], [[1, -4], 11],
        [[-2, -3], 11], [[-1, -3], 11], [[0, -3], 10], [[1, -3], 11], [[2, -3], 11],
        [[-2, -2], 11], [[-1, -2], 11], [[0, -2], 10], [[1, -2], 11], [[2, -2], 11],
        [[0, -1], 10],
        [[0, 0], 10],
    ]
    for block in blocks:
        _x = x + block[0][0]
        _y = y + block[0][1]

        chunk_checked = change_block_over_border(chunk, _x, _y)
        _x = chunk_checked[1]
        _y = chunk_checked[2]
        chunk_checked = chunk_checked[0]

        if chunk_checked != -1:
            if main.block_data[main.loaded_chunks[chunk_checked][0][_x][_y]]["Replacable"]:
                main.loaded_chunks[chunk_checked][0][_x][_y] = block[1]
                render_blocks([[_x, _y]], chunk_checked)

def create_chunk():
    return [[0 for _ in range(64)] for _ in range(64)]

def generate_chunk(chunk):
    main.loaded_chunks[chunk][0] = [[4 for _ in range(64)] for _ in range(64)]

def generate_chunk_2d_flat(chunk):
    if main.loaded_chunks[chunk][1][1] == 0:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if y == 32:
                    row.append(2)
                    if random.randint(0, 16) == 0:
                        main.tree_queue[chunk].append([x, y-1])
                elif 58 > y > 32:
                    row.append(1)
                elif y >= 58:
                    row.append(random.choice([1, 4]))
                elif y < 32:
                    row.append(0)
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents
    elif 3 > main.loaded_chunks[chunk][1][1] >= 1:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if y < 58 or main.loaded_chunks[chunk][1][1] == 1:
                    if random.randint(0, 100) <= 5:
                        row.append(random.randint(29, 33))
                    else:
                        row.append(4)
                else:
                    row.append(random.choice([4, 36]))
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents
    elif main.loaded_chunks[chunk][1][1] >= 3:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if random.randint(0, 100) <= 10:
                    row.append(random.randint(37, 40))
                else:
                    row.append(36)
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents