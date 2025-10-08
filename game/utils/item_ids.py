import pygame

def load_items():
    item_data = {
        0: {},
        1: {
            "Name": "Dirt",
            "filename": "dirt",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt.png'), (32, 32)),
        },
        1001: {
            "Name": "Iron Ingot",
            "filename": "iron_ingot",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/iron_ingot.png'), (32, 32)),
        }
    }

    return item_data