import random
import json
import zipfile
import io
import pygame
import math
import os
import glob
import shutil
from utils.block_ids import *
import datetime
import subprocess
from game.scenes.game import *
from game.scenes.loading import *
from game.utils.util_functs import *
import __main__ as main

world_name_input = ""

def scene_menu(events):
    global world_name_input
    background_fill_texture(main.block_data[1]["Texture"], 2, main.surface)
    mouse = pygame.mouse.get_pos()
    logo_x = main.surface.get_width() / 2 - main.logo.get_width() / 2
    main.surface.blit(main.logo, (logo_x, 180))

    if button(main.surface.get_width() / 2, 500, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Play", main.surface, events, "M", "T"):
        main.current_scene = 1
        main.menu_scroll = 0
        world_name_input = ""

    if button(main.surface.get_width() / 2, 600, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Texturepacks", main.surface, events, "M", "T"):
        main.current_scene = 5
        main.menu_scroll = 0

    if button(main.surface.get_width() / 2, 700, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Mods", main.surface, events, "M", "T"):
        main.current_scene = 7
        main.menu_scroll = 0

    if button(main.surface.get_width() / 2, 800, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Exit", main.surface, events, "M", "T"):
        main.RUNNING = False

def scene_menu_select(events):
    background_fill_texture(main.block_data[1]["Texture"], 2, main.surface)
    global world_name_input
    main.show_esc = False

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalnum():
                world_name_input += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                world_name_input = world_name_input[:-1]

    if button(660, 100, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), f"Create World", main.surface, events, "M","T"):
        main.current_scene = 8
        inventory = [[0,0] for _ in range(40)]
    if button(1260, 100, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Main Menu", main.surface, events, "M", "T"):
        main.current_scene = 0

    if button(380, 90, 64, 64, main.explorer, (255, 255, 255, 100), 0, main.surface, events,"M", "T"):
        if main.SYSTEM == "Windows":
            os.startfile(f"{main.GAMEPATH}/saves")
        else:
            subprocess.Popen(['xdg-open', f"{main.GAMEPATH}/saves"])


    y = main.menu_scroll
    dirs = [dir for dir in os.listdir(f"{main.GAMEPATH}/saves") if os.path.isdir(os.path.join(main.GAMEPATH, "saves", dir))]
    texture = pygame.Surface((1, 1), pygame.SRCALPHA)
    texture.fill((20, 20, 20, 150))
    for i in dirs:
        if -30 <= y < 1100:
            if button(200, 200 + y, 1250, 128, texture, (160, 160, 160, 100), 0, main.surface, events, "L", "T"):
                if os.path.exists(f"{main.GAMEPATH}/saves/{i}/infos.json"):
                    main.world_name = i
                    main.OX = 0
                    main.OY = 0
                    main.current_scene = 6
                    main.loading_timeout = 0
                    main.loading_info = [os.path.join(main.GAMEPATH, "saves", i), "load"]


            if button(1500, 232 + y, 64, 64, main.trashbin, (255, 255, 255, 60), 0, main.surface, events, "L", "T"):
                shutil.rmtree(os.path.join(main.GAMEPATH, "saves", i))

            if os.path.exists(f"{main.GAMEPATH}/saves/{i}/icon.png"):
                icon = pygame.image.load(f"{main.GAMEPATH}/saves/{i}/icon.png")
            else:
                icon = main.def_img
            icon = pygame.transform.scale(icon, (128, 128))
            main.surface.blit(icon, (200, 200 + y))

            if os.path.exists(f"{main.GAMEPATH}/saves/{i}/infos.json"):
                with open(f"{main.GAMEPATH}/saves/{i}/infos.json", "r") as file:
                    infos = json.loads(file.read())
            else:
                infos = {
                    "Name": "infos.json is missing!",
                    "SaveDate": "none"
                }
            size_bytes = 0
            if os.path.exists(f"{main.GAMEPATH}/saves/{i}"):
                for filename in os.listdir(f"{main.GAMEPATH}/saves/{i}"):
                    fp = os.path.join(main.GAMEPATH, "saves", i, filename)
                    if os.path.isfile(fp):
                        size_bytes += os.path.getsize(fp)
                for filename in os.listdir(f"{main.GAMEPATH}/saves/{i}/chunkdata"):
                    fp = os.path.join(main.GAMEPATH, "saves", i, "chunkdata", filename)
                    if os.path.isfile(fp):
                        size_bytes += os.path.getsize(fp)
            details = f"{infos["Name"]}\nCreated: {infos["SaveDate"]}, File size: {size_bytes / 1024:.2f}KB"
            text_render_multiline(340, 200 + y, main.main_font, details, True, (255, 255, 255), main.surface, "L", "T")

        y += 150
        main.menu_scroll = clamp(main.menu_scroll, (len(dirs)-1)*150*-1, 0)

def scene_menu_create():
    background_fill_texture(main.block_data[1]["Texture"], 2, main.surface)

    if button(660, 100, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), f"{"Enter Name..." if not main.menu_create_worldname_input else ""}{main.menu_create_worldname_input}", main.surface, main.EVENTS, "L", "T"):
        main.menu_create_input_box[0] = 1
        main.menu_create_input_box[1] = ""

    for event in main.EVENTS:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                main.menu_create_input_box[1] = main.menu_create_input_box[1][:-1]
            elif event.unicode.isalnum():
                main.menu_create_input_box[1] += event.unicode

    if main.menu_create_input_box[0] == 1:
        main.menu_create_worldname_input = main.menu_create_input_box[1]
    elif main.menu_create_input_box[0] == 2:
        main.menu_create_seed_input = main.menu_create_input_box[1]

    if button(660, 200, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), f"Gamemode: {main.gamemode} (in progress)", main.surface, main.EVENTS, "L", "T"):
        main.gamemode += 1
        if main.gamemode >= 2:
            main.gamemode = 0

    if button(660, 300, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), f"{"Enter Seed..." if not main.menu_create_seed_input else ""}{main.menu_create_seed_input}", main.surface, main.EVENTS, "L", "T"):
        main.menu_create_input_box[0] = 2
        main.menu_create_input_box[1] = ""

    if button(660, 400, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), f"Worldtype: {main.menu_create_worldtype} (in progress)", main.surface, main.EVENTS, "L", "T"):
        main.menu_create_worldtype += 1
        if main.menu_create_worldtype >= 2:
            main.menu_create_worldtype = 0

    if button(660, 500, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Create World", main.surface, main.EVENTS, "L", "T"):
        if main.menu_create_worldname_input != "":
            path = os.path.join(main.GAMEPATH,"saves", main.menu_create_worldname_input)
            os.makedirs(path, exist_ok=True)
            os.makedirs(os.path.join(path, "chunkdata"), exist_ok=True)
            inventory = [0 for _ in range(40)]
            with open(f"{path}/infos.json", "w") as file:
                infos = {
                    "Name": main.menu_create_worldname_input,
                    "SaveDate": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
                    "GameMode": main.gamemode,
                    "Inventory": main.inventory
                }
                file.write(json.dumps(infos))

            main.world_name = main.menu_create_worldname_input
            main.current_scene = 6
            main.loading_timeout = 0
            main.loading_info = ["", "create"]
            random.seed(main.menu_create_seed_input)

def scene_menu_texturepacks(events):
    background_fill_texture(main.block_data[1]["Texture"], 2, main.surface)
    if button(660, 100, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Clear Texturepack", main.surface, events, "M", "T"):
        main.block_data = load_blocks()
        with open(f"{main.GAMEPATH}/settings.json", "r") as file:
            read_data = json.load(file)
        read_data["CurrentTexturepack"] = "none"
        with open(f"{main.GAMEPATH}/settings.json", "w") as file:
            json.dump(read_data, file, indent=2)

    if button(1260, 100, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Main Menu", main.surface, events, "M", "T"):
        main.current_scene = 0

    texturepack_folder = f"{os.getenv('APPDATA')}/.minecraft/resourcepacks"
    if button(380, 90, 64, 64, main.explorer, (255, 255, 255, 100), 0, main.surface, events,"M", "T"):
        if main.SYSTEM == "Windows":
            os.startfile(texturepack_folder)
        else:
            subprocess.Popen(['xdg-open', texturepack_folder])

    y = main.menu_scroll
    dirs = [dir for dir in os.listdir(texturepack_folder) if os.path.isdir(os.path.join(texturepack_folder, dir))]
    texture = pygame.Surface((1, 1), pygame.SRCALPHA)
    texture.fill((20, 20, 20, 150))
    for i in dirs:
        if -30 <= y < 1100:
            if button(200, 200 + y, 1200, 128, texture, (160, 160, 160, 100), 0, main.surface, events, "L", "T"):
                texturepack_load(f"{texturepack_folder}/{i}")

            if os.path.exists(f"{texturepack_folder}/{i}/pack.png"):
                icon = pygame.image.load(f"{texturepack_folder}/{i}/pack.png")
                icon = pygame.transform.scale(icon, (128, 128))
            else:
                icon = main.def_img
            main.surface.blit(icon, (200, 200 + y))

            with open(f"{texturepack_folder}/{i}/pack.mcmeta", "r") as file:
                contents = json.loads(file.read())

            details = f"{i}\n{contents["pack"]["description"]}"
            text_render_multiline(340, 200 + y, main.main_font, details, True, (255, 255, 255), main.surface, "L", "T")

        y += 150
        main.menu_scroll = clamp(main.menu_scroll, (len(dirs)-1)*150*-1, 0)

def scene_menu_mods(events):
    background_fill_texture(main.block_data[1]["Texture"], 2, main.surface)

    if button(1260, 100, 400, 50, main.block_data[4]["Texture"], (37, 124, 211, 100), "Main Menu", main.surface, events, "M", "T"):
        main.current_scene = 0

    if button(380, 90, 64, 64, main.explorer, (255, 255, 255, 100), 0, main.surface, events, "M", "T"):
        if main.SYSTEM == "Windows":
            os.startfile(main.MODPATH)
        else:
            subprocess.Popen(['xdg-open', main.MODPATH])

    y = main.menu_scroll
    dirs = [file for file in os.listdir(main.MODPATH) if file.endswith('.zip') and os.path.isfile(os.path.join(main.MODPATH, file))]

    texture = pygame.Surface((1, 1), pygame.SRCALPHA)
    texture.fill((20, 20, 20, 150))
    for i in dirs:
        if -30 <= y < 1100:
            if button(200, 200 + y, 1200, 128, texture, (160, 160, 160, 100), 0, main.surface, events, "L", "T"):
                if str(i) in main.loaded_mods:
                    main.loaded_mods.remove(str(i))
                else:
                    main.loaded_mods.append(str(i))

                with open(f"{main.GAMEPATH}/settings.json", "r") as file:
                    read_data = json.load(file)
                read_data["LoadedMods"] = main.loaded_mods
                with open(f"{main.GAMEPATH}/settings.json", "w") as file:
                    json.dump(read_data, file, indent=2)
                if str(i) in main.loaded_mods:
                    for mod in main.loaded_mods:
                        with zipfile.ZipFile(f"{main.MODPATH}/{mod}", 'r') as zip_ref:
                            if "scripts/load.py" in zip_ref.namelist():
                                with zip_ref.open("scripts/load.py") as file:
                                    exec(file.read())

            if str(i) in main.loaded_mods:
                status_img = main.img_mod_loaded
            else:
                status_img = main.img_mod_unloaded
            status_img = pygame.transform.scale(status_img, (64, 64))
            main.surface.blit(status_img, (100, 232 + y))

            with zipfile.ZipFile(f"{main.MODPATH}/{i}", 'r') as zip_ref:
                if "icon.png" in zip_ref.namelist():
                    with zip_ref.open("icon.png") as img_file:
                        icon = pygame.image.load(io.BytesIO(img_file.read()))
                        icon = pygame.transform.scale(icon, (128, 128))
                else:
                    icon = main.def_img
                main.surface.blit(icon, (200, 200 + y))

                with zip_ref.open("info.json") as file:
                    contents = json.load(file)

                details = f"{contents["Name"]}\n{contents["Description"]}\nBy: {contents["Author"]}"
                text_render_multiline(340, 200 + y, main.main_font, details, True, (255, 255, 255), main.surface, "L", "T")

        y += 150
        main.menu_scroll = clamp(main.menu_scroll, (len(dirs)-1)*150*-1, 0)