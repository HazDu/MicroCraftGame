import pygame
import os
import json
import zipfile
from pygame import SRCALPHA
from game.utils.util_functs import *
import __main__ as main


def ui(events, surf, scale):
    surface = pygame.Surface((1920, 1080), SRCALPHA)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main.show_esc = not main.show_esc
            elif event.key == pygame.K_e:
                main.show_inv = not main.show_inv
            elif event.key == pygame.K_F1:
                main.show_debug = not main.show_debug

    #Block selector
    mouse = pygame.mouse.get_pos()
    grid_size = 16 * scale

    block_x = grid_size * ((mouse[0] - main.OX) // grid_size) + main.OX
    block_y = grid_size * ((mouse[1] - main.OY) // grid_size) + main.OY

    if point_distance((surf.get_width() / 2, surf.get_height() / 2), (mouse[0], mouse[1])) < 300:
        main.block_in_reach = True
        sel_col = (255,255,0)
    else:
        main.block_in_reach = False
        sel_col = (255, 0, 0)

    pygame.draw.rect(surface, sel_col, (block_x, block_y, (16 * scale), (16 * scale)), 3)
    surf.blit(surface, (0,0))

    #change cursor
    x = ((mouse[0] - main.OX) % 4096) // 64
    y = ((mouse[1] - main.OY) % 4096) // 64
    mouse_chunk = mouse_get_chunk()
    if main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Interactable"]:
        main.cur = main.cur_circle

    #ESC Screen
    if main.show_esc:
        pygame.draw.rect(surf, (68, 41, 31), (460, 190, 1000, 700))

        if button(960, 250, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Resume", main.surface, events, "M", "T"):
            main.show_esc = False
        if button(960, 350, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Save", main.surface, events, "M", "T"):
            save_world()
            main.show_esc = False
            main.img_save_timeout = 5
        if button(960, 450, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Save & Quit", main.surface, events, "M", "T"):
            save_world()
            main.show_esc = False
            main.img_save_timeout = 1


    #Inventory
    if main.show_inv:
        pygame.draw.rect(main.surface, (64, 64, 64), (460, 190, 1000, 700))
        block_id = 0
        for y in range(3):
            for x in range(8):

                block_id += 1
                if block_id < len(main.block_data):
                    showable = False
                    while not showable:
                        if not main.block_data[block_id]["InvShow"]:
                            block_id += 1
                        else:
                            showable = True
                    if button(500 + (x * 80), 230 + (y * 80), 64, 64, main.block_data[block_id]["Texture"], (255, 255, 255, 60), 0, main.surface, events, "L", "T"):
                        main.block_in_hand = block_id
                        main.show_inv = False
                    if block_id == main.block_in_hand:
                        pygame.draw.rect(main.surface, (21, 128, 210), (500 + (x * 80), 230 + (y * 80), 64, 64), 3)

    #ui elements added by mods
    if main.mods_active:
        for mod in main.loaded_mods:
            with zipfile.ZipFile(f"{main.MODPATH}/{mod}", 'r') as zip_ref:
                if "scripts/ui.py" in zip_ref.namelist():
                    with zip_ref.open("scripts/ui.py") as file:
                        exec(file.read())


    #Debug Infos
    if main.show_debug:
        mx = ((mouse[0] - main.OX) % 4096) // 64
        my = ((mouse[1] - main.OY) % 4096) // 64
        debug_txt = (f"FPS: {main.clock.get_fps():.2f}\n"
                     f"MouseX: {mouse[0]}\nMoseY: {mouse[1]}\n"
                     f"BlockHover ID: {main.loaded_chunks[mouse_get_chunk()][0][mx][my]}, X: {mx}, Y: {my}\n"
                     f"MouseChunk: {mouse_get_chunk()}\n"
                     f"MainChunk: {main.loaded_chunks[4][1]}\n"
                     f"PlayerXY: {main.OX - main.surface.get_width() / 2}, {main.OY - main.surface.get_height() / 2}\n")
        text_render_multiline(10, 10, main.main_font, debug_txt, True, (255, 255, 255), surf, "L", "T")
        pygame.draw.rect(main.surface, (250, 1, 209), (main.OX, main.OY, 4096, 4096), 3)

