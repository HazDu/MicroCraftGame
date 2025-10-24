import pygame
import __main__ as main
from scenes.game import *


def scene_loading(path, typee):

    main.surface.fill((0, 0, 0))

    txt = main.main_font.render("LOADING WORLD...", True, (255, 255, 255))
    x = main.surface.get_width() / 2 - txt.get_width() / 2
    y = main.surface.get_height() / 2 - txt.get_height() / 2
    main.surface.blit(txt, (x, y))
    main.loading_timeout += 1

    main.OX = -1120
    main.OY = -1476
    if main.gamemode == 0:
        main.break_speed = 1
    else:
        main.break_speed = 99999
    main.inventory = [[0, 0] for _ in range(40)]
    main.inv_mouse = [0, 0]
    main.workbench_storage = [[0, 0] for _ in range(10)]
    main.growing_saplings = []
    main.container_savedata = {"Chunks": []}

    if main.loading_timeout >= 2:
        if typee == "create":
            scene_game_create()
        elif typee == "load":
            scene_game_load(path)


