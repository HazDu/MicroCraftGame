import pygame

def load_items():
    item_data = {
        0: {},
        1: {
            "Name": "Dirt",
            "filename": "dirt",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt.png'), (48, 48)),
        },
        2: {
            "Name": "Grass Block",
            "filename": "grass_block_top",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass_block_top.png'), (48, 48)),
        },
        3: {
            "Name": "Path",
            "filename": "dirt_path_top",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt_path_top.png'), (48, 48)),
        },
        4: {
            "Name": "Clean Stone",
            "filename": "stone",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone.png'), (48, 48)),
        },
        5: {
            "Name": "Cobblestone",
            "filename": "cobblestone",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/cobblestone.png'), (48, 48)),
        },
        6: {
            "Name": "Stone Bricks",
            "filename": "stone_bricks",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone_bricks.png'), (48, 48)),
        },
        7: {
            "Name": "Bricks",
            "filename": "bricks",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bricks.png'), (48, 48)),
        },
        8: {
            "Name": "Sand",
            "filename": "sand",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/sand.png'), (48, 48)),
        },
        9: {
            "Name": "Oak Wood",
            "filename": "oak_planks",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_planks.png'), (48, 48)),
        },
        10: {
            "Name": "Oak Log",
            "filename": "oak_log",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_log.png'), (48, 48)),
        },
        1001: {
            "Name": "Iron Ingot",
            "filename": "iron_ingot",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/iron_ingot.png'), (32, 32)),
        }
    }

    return item_data