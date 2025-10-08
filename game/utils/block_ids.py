import pygame

def load_blocks():
    air_block = pygame.Surface((64, 64), pygame.SRCALPHA)
    air_block.fill((200, 250, 255))

    block_data = {
        0: {
            "Texture": air_block,
            "Collidable": False,
            "Minable": False,
            "Replacable": True,
            "Interactable": False,
            "InvShow": True,
            "filename": "air_block",
            "Hardness": 0
        },
        1: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "dirt",
            "Hardness": 10
        },
        2: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass_block_top.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "grass_block_top",
            "Hardness": 10
        },
        3: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt_path_top.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "dirt_path_top",
            "Hardness": 10
        },
        4: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "stone",
            "Hardness": 30
        },
        5: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/cobblestone.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "cobblestone",
            "Hardness": 30
        },
        6: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone_bricks.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "stone_bricks",
            "Hardness": 30
        },
        7: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bricks.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "bricks",
            "Hardness": 30
        },
        8: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/sand.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "sand",
            "Hardness": 10
        },
        9: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_planks.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "oak_planks",
            "Hardness": 20
        },
        10: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_log.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "oak_log",
            "Hardness": 20
        },
        11: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_leaves.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": True,
            "Interactable": False,
            "InvShow": True,
            "filename": "oak_leaves",
            "Hardness": 5
        },
        12: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bedrock.png'), (64, 64)),
            "Collidable": True,
            "Minable": False,
            "Replacable": False,
            "Interactable": False,
            "InvShow": False,
            "filename": "bedrock",
            "Hardness": 0
        },
        13: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": True,
            "Interactable": False,
            "InvShow": False,
            "filename": "grass",
            "Hardness": 5
        },
        14: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/tnt_side.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "tnt_side",
            "Hardness": 5
        },
        15: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/crafting_table_front.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "crafting_table_front",
            "Hardness": 20
        },
        16: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/furnace_front_on.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "furnace_front_on",
            "Hardness": 30
        },
        17: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/barrel_top.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "barrel_top",
            "Hardness": 20
        },
        18: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/magma.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "magma",
            "Hardness": 30
        },
        19: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/jack_o_lantern.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "jack_o_lantern",
            "Hardness": 20
        },
        20: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/glowstone.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "glowstone",
            "Hardness": 10
        },
        21: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/glass.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "glass",
            "Hardness": 10
        },
        22: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/fence.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "fence",
            "Hardness": 20
        },
        23: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_bars.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "iron_bars",
            "Hardness": 30
        },
        24: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_block.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "iron_block",
            "Hardness": 30
        },
        25: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/gold_block.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "gold_block",
            "Hardness": 40
        },
        26: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/diamond_block.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "diamond_block",
            "Hardness": 50
        },
        27: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/emerald_block.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "emerald_block",
            "Hardness": 60
        },
        28: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/coal_block.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "coal_block",
            "Hardness": 30
        },
        29: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/coal_ore.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "coal_ore",
            "Hardness": 50
        },
        30: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_ore.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "iron_ore",
            "Hardness": 50
        },
        31: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/gold_ore.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "gold_ore",
            "Hardness": 50
        },
        32: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/diamond_ore.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "diamond_ore",
            "Hardness": 50
        },
        33: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/emerald_ore.png'), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "emerald_ore",
            "Hardness": 50
        },
        34: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/ladder.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "ladder",
            "Hardness": 20
        },
        35: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/poppy.png'), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": True,
            "Interactable": False,
            "InvShow": True,
            "filename": "poppy",
            "Hardness": 5
        },
    }

    return block_data