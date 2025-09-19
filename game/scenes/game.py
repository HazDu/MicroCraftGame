import pygame
import random
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
            with open(path + f"\chunkdata\[{x}, {y}].chunk", "r") as file:
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

            main.surface.blit(self.sprite, (main.surface.get_width()/2 - 32, main.surface.get_height()/2 - 32))

    player = Player()

    chunk_draw_count = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if 6016 > ((x * 4096) + main.OX + 4096) > 0 and 5176 > ((y * 4096) + main.OY + 4096) > 0:
                main.surface.blit(main.block_surface[chunk_draw_count], (main.OX + (x * 4096), main.OY + (y * 4096)))
            chunk_draw_count += 1

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

    player.player_default()
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
