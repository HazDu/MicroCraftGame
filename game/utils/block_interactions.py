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
        case 15:
            main.container_open = [True, 15]
            main.show_inv = True
        case 10:
            main.loaded_chunks[chunk][0][x][y] = 15
            render_blocks([[x, y]], chunk)
        case 17:
            coords = get_coordinates_from_chunk(chunk)
            data_found = False
            for chunk in main.container_savedata:
                [chx, chy], bl_data_list = chunk
                if chx == coords[0] and chy == coords[1]:
                    for bl_data in bl_data_list:
                        [blx, bly], data = bl_data
                        if blx == x and bly == y:
                            data_found = True
                            main.container_current = data
            if not data_found:
                main.container_current = [[0,0] for _ in range(32)]

            main.container_open = [True, 17]
            main.show_inv = True