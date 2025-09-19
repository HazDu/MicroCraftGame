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
            main.loaded_chunks[chunk][0][x][y] = int(18)
            changed_blocks = [[x, y]]
            for i in destroy_radius:
                _x = x + i[0]
                _y = y + i[1]

                chunk_checked = get_coordinates_from_chunk(chunk)
                if _x < 0:
                    _x =  64 + _x
                    if _y < 0:
                        _y = 64 + _y
                        chunk_checked[0] = chunk_checked[0] - 1
                        chunk_checked[1] = chunk_checked[1] - 1
                    elif _y > 63:
                        _y = _y -64
                        chunk_checked[0] = chunk_checked[0] - 1
                        chunk_checked[1] = chunk_checked[1] + 1
                    else:
                        chunk_checked[0] = chunk_checked[0] - 1
                elif _x > 63:
                    _x = _x - 64
                    if _y < 0:
                        _y = 64 + _y
                        chunk_checked[0] = chunk_checked[0] + 1
                        chunk_checked[1] = chunk_checked[1] - 1
                    elif _y > 63:
                        _y = _y - 64
                        chunk_checked[0] = chunk_checked[0] + 1
                        chunk_checked[1] = chunk_checked[1] + 1
                    else:
                        chunk_checked[0] = chunk_checked[0] + 1
                else:
                    if _y < 0:
                        _y = 64 + _y
                        chunk_checked[1] = chunk_checked[1] - 1
                    elif _y > 63:
                        _y = _y - 64
                        chunk_checked[1] = chunk_checked[1] + 1

                chunk_checked = get_chunk_from_coordinates(chunk_checked[0], chunk_checked[1])

                if main.loaded_chunks[chunk_checked][0][_x][_y] != 12 and chunk_checked != -1:
                    if main.loaded_chunks[chunk_checked][0][_x][_y] == 14:
                        block_interact(14, _x, _y, chunk_checked)
                    else:
                        main.loaded_chunks[chunk_checked][0][_x][_y] = int(0)
                        changed_blocks.append([_x, _y])
                        render_blocks(changed_blocks, chunk_checked)

