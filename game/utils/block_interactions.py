import pygame
import __main__; main = __main__
from game.utils.util_functs import *

def block_interact(block_id, x, y, chunk):
    match block_id:
        case 14:
            destroy_radius = [
                                [-1, -3], [0, -3], [1, -3],
                                [-2, -2], [-1, -2], [0, -2], [1, -2], [2, -2],
                                [-3, -1], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1], [3, -1],
                                [-3, 0], [-2, 0], [-1, 0], [1, 0], [2, 0], [3, 0],
                                [-3, 1], [-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1], [3, 1],
                                [-2, 2], [-1, 2], [0, 2], [1, 2], [2, 2],
                                [-1, 3], [0, 3], [1, 3]
                              ]
            main.loaded_chunks[chunk][0][x][y] = int(0)
            changed_blocks = [[x, y]]
            for i in destroy_radius:
                _x = x + i[0]
                _y = y + i[1]

                chunk_checked = change_block_over_border(chunk, _x, _y)
                _x = chunk_checked[1]
                _y = chunk_checked[2]
                chunk_checked = chunk_checked[0]

                if main.loaded_chunks[chunk_checked][0][_x][_y] != 12 and chunk_checked != -1:
                    if main.loaded_chunks[chunk_checked][0][_x][_y] == 14:
                        block_interact(14, _x, _y, chunk_checked)
                    else:
                        main.loaded_chunks[chunk_checked][0][_x][_y] = int(0)
                        changed_blocks.append([_x, _y])
                        render_blocks(changed_blocks, chunk_checked)

