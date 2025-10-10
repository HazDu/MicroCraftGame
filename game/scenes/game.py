import os.path
import zipfile
import pygame
import random
import math
import copy
import ast
from utils.ui import *
from utils.block_interactions import *
from utils.util_functs import *
from utils.generator import *
import __main__ as main

#classes
class Player:
    def __init__(self):
        self.speed = 6
        self.x = 0
        self.y = 0
        self.jump_vel = -0.5
        self.jump_max_vel = -25
        self.sprite = pygame.transform.scale(pygame.image.load("game/assets/entities/T-Player.png"), (64, 64))
        self.hitbox = {
            "top": 32,
            "left": 12,
            "bottom": -32,
            "right": -12,
        }

    def player_default(self):
        keys = pygame.key.get_pressed()

        self.x = main.OX - (main.surface.get_width() / 2)
        self.y = main.OY - (main.surface.get_height() / 2)

        standing_x = clamp(int((self.x // 64) * -1) -1 , 0, 63)
        standing_y = clamp(int((self.y // 64) * -1) -1 , 0, 63)
        # text_render_multiline(500, 10, main.main_font, f"{standing_x}, {standing_y}", True, (255, 255, 255), main.surface, "x", "x")

        #collision check
        is_collidable = {
            "North": False,
            "South": False,
            "East": False,
            "West": False,
        }

        if standing_x - 1 < 0:
            check_chunk = 3
            standing_xx = 63
        else:
            check_chunk = 4
            standing_xx = standing_x - 1
        if main.block_data[main.loaded_chunks[check_chunk][0][standing_xx][standing_y]]["Collidable"]:
            is_collidable["West"] = True

        if standing_x + 1 > 63:
            check_chunk = 5
            standing_xx = 0
        else:
            check_chunk = 4
            standing_xx = standing_x + 1
        if main.block_data[main.loaded_chunks[check_chunk][0][standing_xx][standing_y]]["Collidable"]:
            is_collidable["East"] = True

        if standing_y - 1 < 0:
            check_chunk = 1
            standing_yy = 63
        else:
            check_chunk = 4
            standing_yy = standing_y - 1
        if main.block_data[main.loaded_chunks[check_chunk][0][standing_x][standing_yy]]["Collidable"]:
            is_collidable["North"] = True

        if standing_y + 1 > 63:
            check_chunk = 7
            standing_yy = 0
        else:
            check_chunk = 4
            standing_yy = standing_y + 1
        if main.block_data[main.loaded_chunks[check_chunk][0][standing_x][standing_yy]]["Collidable"]:
            is_collidable["South"] = True

       # text_render_multiline(500, 50, main.main_font, f"N: {is_collidable["North"]}\ns: {is_collidable["South"]}\nE: {is_collidable["East"]}\nW: {is_collidable["West"]}\n", True, (255, 255, 255), main.surface, "x", "x")

        #movement left/right
        if keys[pygame.K_a]:
            moving_space = (self.x + self.hitbox["left"])*-1 - standing_x*64
            if not is_collidable["West"] or moving_space >= self.speed:
                main.OX += self.speed
            elif moving_space > 0:
                main.OX += moving_space
        if keys[pygame.K_d]:
            moving_space = (standing_x+1)*64 + (self.x + self.hitbox["right"])
            if not is_collidable["East"] or moving_space >= self.speed:
                main.OX -= self.speed
            elif moving_space > 0:
                main.OX -= moving_space

        #movement jump
        if main.loaded_chunks[4][0][standing_x][standing_y] == 34 and keys[pygame.K_SPACE] and not is_collidable["North"]  :
            main.OY += self.speed
        else:
            for event in main.EVENTS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.jump_vel = 10
            if self.jump_vel > 1:
                main.OY += self.jump_vel
                self.jump_vel = self.jump_vel / 1.2
            if -1 < self.jump_vel < 1:
                self.jump_vel = -1

            moving_space = (standing_y + 1)*64 + (self.y + self.hitbox["bottom"])
            if not is_collidable["South"] or moving_space >= self.jump_vel*-1:
                main.OY += self.jump_vel
                if self.jump_max_vel < self.jump_vel < 0:
                    self.jump_vel = self.jump_vel * 1.2
            elif moving_space > 0:
                main.OY += moving_space*-1
            if moving_space == 0 and self.jump_vel <= 0:
                self.jump_vel = 0

            moving_space = (self.y + self.hitbox["top"])*-1 - standing_y*64
            if is_collidable["North"] and self.jump_vel > 1 and moving_space < self.jump_vel:
                main.OY += moving_space
                self.jump_vel = 0

        main.surface.blit(self.sprite, (main.surface.get_width() / 2 - 32, main.surface.get_height() / 2 - 32))

class Item:
    def __init__(self):
        self.item_id = 0
        self.x = 0
        self.y = 0
        self.lifetime = 0
        self.rot = 0
    def item_default(self):
        draw_coords = world_coords_to_screen_coords(self.x, self.y)
        img = pygame.transform.rotozoom(main.item_data[self.item_id]["Texture"], round(self.rot), 0.66666)
        if self.lifetime > 1500:
            img = tint_image(img, (255, 0, 0, 50))

        rect = img.get_rect()
        rect.center = draw_coords[0], draw_coords[1]
        main.surface.blit(img, rect)
        self.lifetime += 1
        self.rot += 0.5



        #text_render_multiline(100, 100, main.main_font, f"{draw_coords}", True, (255, 255, 255), main.surface, "", "")



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
        if main.menu_create_worldtype == 0:
            generate_chunk_2d_flat(chunk)

    for chunk in range(9):
        generate_trees(main.tree_queue[chunk], chunk)

    for chunk in range(9):
        render_blocks(0, chunk)

    main.OX = -1120
    main.OY = -1476
    main.current_scene = 4

def scene_game_load(path):
    with open(path + "/infos.json", "r") as file:
        read = json.load(file)
    main_chunk = read["CurrentChunk"]
    main.OX = read["PlayerX"]
    main.OY = read["PlayerY"]
    main.gamemode = read["GameMode"]
    main.inventory = read["Inventory"]

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


player = Player()
def scene_game(events):
    chunk_draw_count = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if 6016 > ((x * 4096) + main.OX + 4096) > 0 and 5176 > ((y * 4096) + main.OY + 4096) > 0:
                main.surface.blit(main.block_surface[chunk_draw_count], (main.OX + (x * 4096), main.OY + (y * 4096)))
            chunk_draw_count += 1

    #block interacting
    mouse = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_chunk = mouse_get_chunk()

    if main.block_in_reach and not main.paused:
        x = int(((mouse[0] - main.OX) % 4096) // 64)
        y = int(((mouse[1] - main.OY) % 4096) // 64)
        main.selected_block = (x, y)

        if mouse_buttons[0] and main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Hardness"] > 0:
            main.break_progress += 100 / (main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Hardness"])* main.break_speed
            if main.break_progress >= 100 and main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Minable"]:
                if main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][0] != -1 and main.gamemode == 0:
                    new_item = Item()
                    new_item.item_id = main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][0]
                    new_item.x = mouse[0] - main.OX
                    new_item.y = mouse[1] - main.OY
                    main.item_entities.append(new_item)
                main.loaded_chunks[mouse_chunk][0][x][y] = int(0)
                render_blocks([[x, y]], mouse_chunk)
                main.break_progress = 0
        else:
            main.break_progress = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Interactable"]:
                        block_interact(main.loaded_chunks[mouse_chunk][0][x][y], x, y, mouse_chunk)
                    elif main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Replacable"]:
                        main.loaded_chunks[mouse_chunk][0][x][y] = int(main.block_in_hand)
                        render_blocks([[x, y]], mouse_chunk)
                main.break_progress = 0
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                main.break_progress = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_F3] and keys[pygame.K_a]:
                re_render_loaded_chunks()

    #Player chunk teleport
    if player.x > 0:
        main.OX = int(-4095 + main.surface.get_width() / 2)

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [0, 1, 6, 7]:
                    i[0] += 1
                elif i[0] in [2, 8]:
                    main.chunk_render_queue.pop(index)

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
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    elif player.x < -4095:
        main.OX = int(0 + main.surface.get_width() / 2)

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [2, 1, 8, 7]:
                    i[0] -= 1
                elif i[0] in [0, 6]:
                    main.chunk_render_queue.pop(index)

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
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    elif player.y > 0:
        main.OY = int(-4095 + main.surface.get_height() / 2)

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [2, 0, 3, 5]:
                    i[0] += 3
                elif i[0] in [8, 6]:
                    main.chunk_render_queue.pop(index)

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
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    elif player.y < -4095:
        main.OY = int(0 + main.surface.get_height() / 2)

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [8, 6, 3, 5]:
                    i[0] -= 3
                elif i[0] in [0, 2]:
                    main.chunk_render_queue.pop(index)

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
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    player.player_default()
    for item in main.item_entities:
        item.item_default()
        if item.lifetime > 1800:
            main.item_entities.remove(item)

    if main.mods_active:
        for mod in main.loaded_mods:
            with zipfile.ZipFile(f"{main.MODPATH}/{mod}", 'r') as zip_ref:
                if "scripts/game_loop.py" in zip_ref.namelist():
                    with zip_ref.open("scripts/game_loop.py") as file:
                        exec(file.read())

    if len(main.chunk_render_queue) > 2:
        while main.chunk_render_queue[0] in main.chunk_render_queue[1:]:
            main.chunk_render_queue.pop(0)
    if len(main.chunk_render_queue) > 0:
        main.chunk_render_queue = render_chunk(main.chunk_render_queue, 15)
        if len(main.chunk_render_queue) > 9:
            main.chunk_render_queue.pop(0)


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
