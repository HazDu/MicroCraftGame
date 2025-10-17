import pygame

def load_blocks():
    air_block = pygame.Surface((64, 64), pygame.SRCALPHA)
    air_block.fill((0, 0, 0, 0))

    block_data = {
        0: {
            "Texture": air_block,
            "Collidable": False,
            "Minable": False,
            "Replacable": True,
            "Interactable": False,
            "InvShow": True,
            "filename": "air_block",
            "Hardness": 0,
            "Drop": [-1, 0]
        },
        1: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "dirt",
            "Hardness": 10,
            "Drop": [1, 1]
        },
        2: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass_block_top.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "grass_block_top",
            "Hardness": 10,
            "Drop": [2, 1]
        },
        3: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt_path_top.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "dirt_path_top",
            "Hardness": 10,
            "Drop": [3, 1]
        },
        4: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "stone",
            "Hardness": 30,
            "Drop": [5, 1]
        },
        5: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/cobblestone.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "cobblestone",
            "Hardness": 30,
            "Drop": [5, 1]
        },
        6: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone_bricks.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "stone_bricks",
            "Hardness": 30,
            "Drop": [6, 1]
        },
        7: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bricks.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "bricks",
            "Hardness": 30,
            "Drop": [7, 1]
        },
        8: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/sand.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "sand",
            "Hardness": 10,
            "Drop": [8, 1]
        },
        9: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_planks.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "oak_planks",
            "Hardness": 20,
            "Drop": [9, 1]
        },
        10: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_log.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "oak_log",
            "Hardness": 20,
            "Drop": [10, 1]
        },
        11: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_leaves.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": True,
            "Interactable": False,
            "InvShow": True,
            "filename": "oak_leaves",
            "Hardness": 5,
            "Drop": [[1008, 42], [0, 1]]
        },
        12: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bedrock.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": False,
            "Replacable": False,
            "Interactable": False,
            "InvShow": False,
            "filename": "bedrock",
            "Hardness": 0,
            "Drop": [-1, 0]
        },
        13: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": True,
            "Interactable": False,
            "InvShow": False,
            "filename": "grass",
            "Hardness": 5,
            "Drop": [-1, 0]
        },
        14: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/tnt_side.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "tnt_side",
            "Hardness": 5,
            "Drop": [14, 1]
        },
        15: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/crafting_table_front.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "crafting_table_front",
            "Hardness": 20,
            "Drop": [15, 1]
        },
        16: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/furnace_front_on.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "furnace_front_on",
            "Hardness": 30,
            "Drop": [16, 1]
        },
        17: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/barrel_top.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": True,
            "InvShow": True,
            "filename": "barrel_top",
            "Hardness": 20,
            "Drop": [17, 1]
        },
        18: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/magma.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "magma",
            "Hardness": 30,
            "Drop": [18, 1]
        },
        19: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/jack_o_lantern.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "jack_o_lantern",
            "Hardness": 20,
            "Drop": [19, 1]
        },
        20: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/glowstone.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "glowstone",
            "Hardness": 10,
            "Drop": [20, 1]
        },
        21: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/glass.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "glass",
            "Hardness": 10,
            "Drop": [-1, 0]
        },
        22: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/fence.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "fence",
            "Hardness": 20,
            "Drop": [22, 1]
        },
        23: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_bars.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "iron_bars",
            "Hardness": 30,
            "Drop": [1001, 1]
        },
        24: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_block.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "iron_block",
            "Hardness": 30,
            "Drop": [1001, 9]
        },
        25: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/gold_block.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "gold_block",
            "Hardness": 40,
            "Drop": [1002, 9]
        },
        26: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/diamond_block.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "diamond_block",
            "Hardness": 50,
            "Drop": [1003, 9]
        },
        27: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/emerald_block.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "emerald_block",
            "Hardness": 60,
            "Drop": [1004, 9]
        },
        28: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/coal_block.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "coal_block",
            "Hardness": 30,
            "Drop": [1005, 9]
        },
        29: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/coal_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "coal_ore",
            "Hardness": 50,
            "Drop": [1005, [2, 5]]
        },
        30: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "iron_ore",
            "Hardness": 50,
            "Drop": [1006, [1, 2]]
        },
        31: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/gold_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "gold_ore",
            "Hardness": 50,
            "Drop": [1007, 1]
        },
        32: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/diamond_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "diamond_ore",
            "Hardness": 50,
            "Drop": [1003, 1]
        },
        33: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/emerald_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "emerald_ore",
            "Hardness": 50,
            "Drop": [[1004, 5], 1]
        },
        34: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/ladder.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "ladder",
            "Hardness": 20,
            "Drop": [34, 1]
        },
        35: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/poppy.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": True,
            "Interactable": False,
            "InvShow": True,
            "filename": "poppy",
            "Hardness": 5,
            "Drop": [35, 1]
        },
        36: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "deepslate",
            "Hardness": 40,
            "Drop": [36, 1]
        },
        37: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_iron_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "deepslate_iron_ore",
            "Hardness": 60,
            "Drop": [1006, [4, 6]]
        },
        38: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_gold_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "deepslate_gold_ore",
            "Hardness": 60,
            "Drop": [1007, [1, 3]]
        },
        39: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_diamond_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "deepslate_diamond_ore",
            "Hardness": 60,
            "Drop": [1003, [2, 4]]
        },
        40: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_emerald_ore.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "deepslate_emerald_ore",
            "Hardness": 60,
            "Drop": [1004, 1]
        },
        41: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/smooth_stone.png').convert_alpha(), (64, 64)),
            "Collidable": True,
            "Minable": True,
            "Replacable": False,
            "Interactable": False,
            "InvShow": True,
            "filename": "smooth_stone",
            "Hardness": 60,
            "Drop": [1004, 1]
        },
        42: {
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_sapling.png').convert_alpha(), (64, 64)),
            "Collidable": False,
            "Minable": True,
            "Replacable": True,
            "Interactable": True,
            "InvShow": True,
            "filename": "oak_sapling",
            "Hardness": 5,
            "Drop": [42, 1]
        },
    }

    return block_data