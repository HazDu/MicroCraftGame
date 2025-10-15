import pygame
import os
import json
import zipfile
import math
from pygame import SRCALPHA
from game.utils.util_functs import *
import __main__ as main



def ui(events, surf, scale):
    surface = pygame.Surface((1920, 1080), SRCALPHA)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not main.show_inv:
                main.show_esc = not main.show_esc
            elif event.key == pygame.K_e and not main.show_esc:
                if main.show_inv:
                    main.container_open[0] = False
                main.show_inv = not main.show_inv
            elif event.key == pygame.K_F1:
                main.show_debug = not main.show_debug

    #Block selector
    mouse = pygame.mouse.get_pos()
    if not main.show_inv and not main.show_esc:
        grid_size = 16 * scale

        block_x = grid_size * ((mouse[0] - main.OX) // grid_size) + main.OX
        block_y = grid_size * ((mouse[1] - main.OY) // grid_size) + main.OY

        if point_distance((surf.get_width() / 2, surf.get_height() / 2), (mouse[0], mouse[1])) < main.reach:
            main.block_in_reach = True
            sel_col = (255,255,0)
        else:
            main.block_in_reach = False
            sel_col = (255, 0, 0)

        if main.break_progress > 0:
            break_sprite = pygame.transform.scale(pygame.image.load(f"game/assets/blocks/destroy/destroy_stage_{clamp(round((10*main.break_progress)/100)-1, 0, 9)}.png"), (64, 64))
            surface.blit(break_sprite, (block_x, block_y))
        pygame.draw.rect(surface, sel_col, (block_x, block_y, (16 * scale), (16 * scale)), 3)
        surf.blit(surface, (0,0))

    #change cursor
    x = int(((mouse[0] - main.OX) % 4096) // 64)
    y = int(((mouse[1] - main.OY) % 4096) // 64)
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

    #hotbar
    surf.blit(main.img_hotbar, (704, 1016))
    surf.blit(main.img_hotbar_sel, (704+(64*main.hotbar_slot), 1016))

    for i in range(8):
        if main.inventory[i][0] != 0:
            text = main.fnt_cons20.render(f"{main.inventory[i][1]}", True, (255, 255, 255))
            surf.blit(main.item_data[main.inventory[i][0]]["Texture"], (712 + 64 * i, 1024))
            surf.blit(text, (714 + 64 * i, 1055))

    for event in events:
        if event.type == pygame.MOUSEWHEEL:
            main.hotbar_slot -= event.y
            if main.hotbar_slot < 0:
                main.hotbar_slot = 7
            elif main.hotbar_slot > 7:
                main.hotbar_slot = 0
            main.action_title = [main.fnt_cons20.render(main.item_data[main.inventory[main.hotbar_slot][0]]["Name"], True, (230, 230, 230, clamp(main.action_title[1], 0, 255))), 700]
    if main.inventory[main.hotbar_slot][0] < 1000:
        main.block_in_hand = main.inventory[main.hotbar_slot][0]
    else:
        main.block_in_hand = 0

    if main.action_title[1] >= 2:
        text = main.action_title[0].copy()
        text.set_alpha(main.action_title[1])
        surf.blit(text, (surf.get_width() / 2 - main.action_title[0].get_width() / 2, 950))
        main.action_title[1] -= 5

    #container ui's
    if main.container_open[0]:
        cont_x = 632
        cont_y = 150
        match main.container_open[1]:
            case 15:
                pygame.draw.rect(main.surface, (64, 64, 64), (cont_x, cont_y, 656, 336), 0, 12)
                surf.blit(main.img_double_arrow, (cont_x+320, cont_y+120))
                slot = 0
                for x in range(3):
                    for y in range(3):
                        btn = button_exact(cont_x+50+x*70, cont_y+50+y*70, 64, 64, main.img_slot, (255, 255, 255, 50), 0, main.surface, events, "L", "T")
                        if btn == "left":
                            if main.workbench_storage[slot][0] == main.inv_mouse[0]:
                                main.workbench_storage[slot][1] += main.inv_mouse[1]
                                main.inv_mouse = [0, 0]
                            else:
                                temp = main.inv_mouse
                                main.inv_mouse = main.workbench_storage[slot]
                                main.workbench_storage[slot] = temp
                        elif btn == "right":
                            if main.workbench_storage[slot][0] == 0 or main.workbench_storage[slot][0] == main.inv_mouse[0]:
                                main.workbench_storage[slot] = [main.inv_mouse[0], main.workbench_storage[slot][1]+1]
                                main.inv_mouse[1] -= 1
                                if main.inv_mouse[1] <= 0:
                                    main.inv_mouse = [0, 0]
                            elif main.inv_mouse == [0, 0] and main.workbench_storage[slot] != [0, 0]:
                                main.inv_mouse = [main.workbench_storage[slot][0], math.ceil(main.workbench_storage[slot][1] /2)]
                                main.workbench_storage[slot][1] = math.floor(main.workbench_storage[slot][1] / 2)

                        if main.workbench_storage[slot][0] != 0:
                            text = main.fnt_cons20.render(f"{main.workbench_storage[slot][1]}", True, (255, 255, 255))
                            surf.blit(main.item_data[main.workbench_storage[slot][0]]["Texture"], (cont_x + x*70+58, cont_y + y*70+58))
                            surf.blit(text, (cont_x + x*70+60, cont_y + y*70+89))

                        slot += 1
                btn = button_exact(cont_x+444, cont_y+120, 64, 64, main.img_slot, (255, 255, 255, 50), 0, main.surface, events, "L", "T")




    #Inventory
    if main.show_inv:
        if main.gamemode == 1:
            pygame.draw.rect(main.surface, (64, 64, 64), (460, 190, 1000, 700), 0, 12)
            block_id = 0
            for y in range(5):
                for x in range(10):

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
        elif main.gamemode == 0:
            inv_x = 632
            inv_y = 600

            for i in range(8):
                if button(704 + i*64, 1016, 64, 64, main.img_empty, (255, 255, 255, 50), 0, main.surface, events, "L", "T"):
                    temp = main.inv_mouse
                    main.inv_mouse = main.inventory[i]
                    main.inventory[i] = temp

            slot = 8
            pygame.draw.rect(main.surface, (64, 64, 64), (inv_x, inv_y, 656, 336), 0, 12)
            for y in range(4):
                for x in range(8):
                    btn = button_exact(inv_x + (x*80)+16, inv_y + (y*80)+16, 64, 64, main.img_slot, (255, 255, 255, 50), 0, main.surface, events, "L", "T")
                    if btn == "left":
                        if main.inv_mouse[0] == main.inventory[slot][0]:
                            if main.inventory[slot][1] + main.inv_mouse[1] <= 256:
                                main.inventory[slot][1] += main.inv_mouse[1]
                                main.inv_mouse = [0, 0]
                            else:
                                main.inv_mouse[1] -= 256 - main.inventory[slot][1]
                                main.inventory[slot][1] = 256
                        else:
                            temp = main.inv_mouse
                            main.inv_mouse = main.inventory[slot]
                            main.inventory[slot] = temp
                    elif btn == "right":
                        if main.inv_mouse == [0, 0] and main.inventory[slot] != [0, 0]:
                            main.inv_mouse = [main.inventory[slot][0], math.ceil(main.inventory[slot][1] /2)]
                            main.inventory[slot][1] = math.floor(main.inventory[slot][1] / 2)
                        else:
                            if main.inventory[slot] == [0, 0] or main.inventory[slot][0] == main.inv_mouse[0]:
                                if main.inventory[slot][1] + 1 <= 256:
                                    main.inventory[slot][0] = main.inv_mouse[0]
                                    main.inventory[slot][1] += 1
                                    main.inv_mouse[1] -= 1

                    if main.inventory[slot][0] != 0:
                        text = main.fnt_cons20.render(f"{main.inventory[slot][1]}", True, (255, 255, 255))
                        surf.blit(main.item_data[main.inventory[slot][0]]["Texture"], (inv_x + 80 * x + 24, inv_y + 80 * y + 24))
                        surf.blit(text, (inv_x + 80 * x + 26, inv_y + 80 * y + 55))
                    slot += 1

            if main.inv_mouse[1] <= 0:
                main.inv_mouse[0] = 0

            if main.inv_mouse[0] != 0:
                text = main.fnt_cons20.render(f"{main.inv_mouse[1]}", True, (255, 255, 255))
                surf.blit(main.item_data[main.inv_mouse[0]]["Texture"], (mouse[0]-24, mouse[1]-24))
                surf.blit(text, (mouse[0]-22, mouse[1]+7))

    #ui elements added by mods
    if main.mods_active:
        for mod in main.loaded_mods:
            with zipfile.ZipFile(f"{main.MODPATH}/{mod}", 'r') as zip_ref:
                if "scripts/ui.py" in zip_ref.namelist():
                    with zip_ref.open("scripts/ui.py") as file:
                        exec(file.read())


    #Debug Infos
    if main.show_debug:
        pygame.draw.rect(main.surface, (250, 1, 209), (main.OX, main.OY, 4096, 4096), 3)
        mx = int(((mouse[0] - main.OX) % 4096) // 64)
        my = int(((mouse[1] - main.OY) % 4096) // 64)
        debug_txt = (f"FPS: {main.clock.get_fps():.2f}\n"
                     f"OriginX: {main.OX}, OriginX: {main.OY}\n"
                     f"MouseX: {mouse[0]}\nMoseY: {mouse[1]}\n"
                     f"MouseChunk: {mouse_get_chunk()}\n"
                     f"BlockHover ID: {main.loaded_chunks[mouse_get_chunk()][0][mx][my]},  X: {mx},  Y: {my}\n"
                     f"MainChunk: {main.loaded_chunks[4][1]}\n"
                     f"Rendering Chunks: {len(main.chunk_render_queue) > 0} "
                     f"({', '.join(str(chunk) for chunk, *_ in main.chunk_render_queue)})\n"
                     f"{f"Rendering Chunk: {main.chunk_render_queue[0][0]} - {((4096 - len(main.chunk_render_queue[0][1])) * 100) / 4096:.0f}%\n" if main.chunk_render_queue else ""}"
                     f"Buffered Chunks: {len(main.chunk_buffer)}\n"
                     )
        text_render_multiline(10, 10, main.main_font, debug_txt, True, (255, 255, 255), surf, "L", "T")

