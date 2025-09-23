import os.path

import pygame
import random
import copy
import ast
from utils.ui import *
from utils.block_interactions import *
from utils.util_functs import *
from utils.generator import *
import __main__ as main

def scene_game_create():
    main.loaded_chunks = [
                            [create_chunk(), [-1, -1]],
                            [create_chunk(), [0, -1]],
                            [create_chunk(), [1, -1]],
                            [create_chunk(), [-1, 0]],
                            [create_chunk(), [0, 0]],
                            [create_chunk(), [1, 0]],
                            [create_chunk(), [-1, 1]],
                            [create_chunk(), [0, 1]],
                            [create_chunk(), [1, 1]]
    ]

    for chunk in range(9):
        generate_chunk(chunk)
    for chunk in range(9):
        generate_tree(main.tree_queue[chunk], chunk)
    for chunk in range(9):
        render_blocks(0, chunk)

    main.current_scene = 4

def scene_game_load(path):
    with open(path + "/infos.json", "r") as file:
        read = json.load(file)
    main_chunk = read["CurrentChunk"]
    main.OX = read["PlayerX"]
    main.OY = read["PlayerY"]

    i = 0
    for y in range(main_chunk[1] -1, main_chunk[1] +2):
        for x in range(main_chunk[0] -1, main_chunk[0] +2):
            with open(path + f"/chunkdata/[{x}, {y}].chunk", "r") as file:
                main.loaded_chunks[i][0] = ast.literal_eval(file.read())
            main.loaded_chunks[i][1] = [x, y]
            i += 1

    for a in range(9):
        main.block_surface[a].fill((200, 250, 255))
        render_blocks(0, a)

    main.current_scene = 4

def scene_game(events):
    class Player:
        def __init__(self):
            self.speed = 8
            self.x = 0
            self.y = 0
            self.sprite = pygame.transform.scale(pygame.image.load("game/assets/entities/T-Player.png"), (64, 64))

        def player_default(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                main.OX += self.speed
            if keys[pygame.K_d]:
                main.OX -= self.speed
            if keys[pygame.K_w]:
                main.OY += self.speed
            if keys[pygame.K_s]:
                main.OY -= self.speed

            self.x = main.OX - main.surface.get_width() / 2
            self.y = main.OY - main.surface.get_height() / 2

            #text_render_multiline(10, 500, main.main_font, f"x:{self.x}\ny:{self.y}", True, (255, 255, 255), main.surface, "L", "T")

            main.surface.blit(self.sprite, (main.surface.get_width()/2 - 32, main.surface.get_height()/2 - 32))

    player = Player()

    chunk_draw_count = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if 6016 > ((x * 4096) + main.OX + 4096) > 0 and 5176 > ((y * 4096) + main.OY + 4096) > 0:
                main.surface.blit(main.block_surface[chunk_draw_count], (main.OX + (x * 4096), main.OY + (y * 4096)))
            chunk_draw_count += 1

    player.player_default()

    mouse = pygame.mouse.get_pos()
    for event in events:
        if main.block_in_reach and not main.paused:
            x = ((mouse[0] - main.OX) % 4096) // 64
            y = ((mouse[1] - main.OY) % 4096) // 64
            main.selected_block = (x, y)
            mouse_chunk = mouse_get_chunk()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Minable"]:
                    main.loaded_chunks[mouse_chunk][0][x][y] = int(0)
                    render_blocks([[x, y]], mouse_chunk)
                elif event.button == 3:
                    if main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Interactable"]:
                        block_interact(main.loaded_chunks[mouse_chunk][0][x][y], x, y, mouse_chunk)
                    elif main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Replacable"]:
                        main.loaded_chunks[mouse_chunk][0][x][y] = int(main.block_in_hand)
                        render_blocks([[x, y]], mouse_chunk)
                        #main.cur = main.cur_hammer

    if player.x > 0:
        main.OX = int(-4095 + main.surface.get_width() / 2)

        for i in [2, 5, 8]:
            with open(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{main.loaded_chunks[i][1]}.chunk", "w") as file:
                file.write(str(main.loaded_chunks[i][0]))

        for column in [2, 1]:
            for row in [0, 3, 6]:
                main.loaded_chunks[column + row] = copy.deepcopy(main.loaded_chunks[column + row - 1])
                main.block_surface[column + row] = copy.copy(main.block_surface[column + row - 1])

        for i in [0, 3, 6]:
            chunk_coords = [main.loaded_chunks[i + 1][1][0] - 1, main.loaded_chunks[i + 1][1][1]]
            if os.path.exists(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{chunk_coords}.chunk"):
                with open(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{chunk_coords}.chunk") as file:
                    main.loaded_chunks[i][0] = ast.literal_eval(file.read())
                    main.loaded_chunks[i][1] = chunk_coords
            else:
                generate_chunk(i)
                main.loaded_chunks[i][1][0] = main.loaded_chunks[i + 1][1][0]-1
            render_blocks(0, i)

    elif player.x < -4095:
        main.OX = int(0 + main.surface.get_width() / 2)

        for i in [0, 3, 6]:
            with open(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{main.loaded_chunks[i][1]}.chunk", "w") as file:
                file.write(str(main.loaded_chunks[i][0]))

        for column in [0, 1]:
            for row in [0, 3, 6]:
                main.loaded_chunks[column + row] = copy.deepcopy(main.loaded_chunks[column + row + 1])
                main.block_surface[column + row] = copy.copy(main.block_surface[column + row + 1])

        for i in [2, 5, 8]:
            chunk_coords = [main.loaded_chunks[i - 1][1][0] + 1, main.loaded_chunks[i - 1][1][1]]
            if os.path.exists(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{chunk_coords}.chunk"):
                with open(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{chunk_coords}.chunk") as file:
                    main.loaded_chunks[i][0] = ast.literal_eval(file.read())
                    main.loaded_chunks[i][1] = chunk_coords
            else:
                generate_chunk(i)
                main.loaded_chunks[i][1][0] = main.loaded_chunks[i - 1][1][0] + 1
            render_blocks(0, i)

    elif player.y > 0:
        main.OY = int(-4095 + main.surface.get_height() / 2)

        for i in [6, 7, 8]:
            with open(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{main.loaded_chunks[i][1]}.chunk",
                      "w") as file:
                file.write(str(main.loaded_chunks[i][0]))

        for row in [2, 1]:
            for col in [0, 1, 2]:
                dst = row * 3 + col
                src = (row - 1) * 3 + col
                main.loaded_chunks[dst] = copy.deepcopy(main.loaded_chunks[src])
                main.block_surface[dst] = copy.copy(main.block_surface[src])

        for i in [0, 1, 2]:
            chunk_coords = [main.loaded_chunks[i + 3][1][0], main.loaded_chunks[i + 3][1][1] - 1]
            chunk_path = f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{chunk_coords}.chunk"
            if os.path.exists(chunk_path):
                with open(chunk_path) as file:
                    main.loaded_chunks[i][0] = ast.literal_eval(file.read())
                    main.loaded_chunks[i][1] = chunk_coords
            else:
                generate_chunk(i)
                main.loaded_chunks[i][1][1] = main.loaded_chunks[i + 3][1][1] - 1
            render_blocks(0, i)
    elif player.y < -4095:
        main.OY = int(0 + main.surface.get_height() / 2)

        for i in [0, 1, 2]:
            with open(f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{main.loaded_chunks[i][1]}.chunk",
                      "w") as file:
                file.write(str(main.loaded_chunks[i][0]))

        for row in [0, 1]:
            for col in [0, 1, 2]:
                dst = row * 3 + col
                src = (row + 1) * 3 + col
                main.loaded_chunks[dst] = copy.deepcopy(main.loaded_chunks[src])
                main.block_surface[dst] = copy.copy(main.block_surface[src])

        for i in [6, 7, 8]:
            chunk_coords = [main.loaded_chunks[i - 3][1][0], main.loaded_chunks[i - 3][1][1] + 1]
            chunk_path = f"{main.GAMEPATH}/saves/{main.world_name}/chunkdata/{chunk_coords}.chunk"
            if os.path.exists(chunk_path):
                with open(chunk_path) as file:
                    main.loaded_chunks[i][0] = ast.literal_eval(file.read())
                    main.loaded_chunks[i][1] = chunk_coords
            else:
                generate_chunk(i)
                main.loaded_chunks[i][1][1] = main.loaded_chunks[i - 3][1][1] + 1
            render_blocks(0, i)


    ui(events, main.surface, main.SCALE)
    if main.img_save_timeout > 0:
        match main.img_save_timeout:
            case 2:
                save_world_icon()
            case 3:
                main.current_scene = 0
            case 6:
                save_world_icon()
        main.img_save_timeout += 1
        if main.img_save_timeout >= 7:
            main.img_save_timeout = 0
