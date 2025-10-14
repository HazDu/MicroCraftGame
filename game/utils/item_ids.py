import pygame

def load_items():
    item_data = {
        0: {},
        1: {
            "Name": "Dirt",
            "filename": "dirt",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt.png').convert_alpha(), (48, 48)),
        },
        2: {
            "Name": "Grass Block",
            "filename": "grass_block_top",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass_block_top.png').convert_alpha(), (48, 48)),
        },
        3: {
            "Name": "Path",
            "filename": "dirt_path_top",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/dirt_path_top.png').convert_alpha(), (48, 48)),
        },
        4: {
            "Name": "Clean Stone",
            "filename": "stone",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone.png').convert_alpha(), (48, 48)),
        },
        5: {
            "Name": "Cobblestone",
            "filename": "cobblestone",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/cobblestone.png').convert_alpha(), (48, 48)),
        },
        6: {
            "Name": "Stone Bricks",
            "filename": "stone_bricks",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/stone_bricks.png').convert_alpha(), (48, 48)),
        },
        7: {
            "Name": "Bricks",
            "filename": "bricks",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bricks.png').convert_alpha(), (48, 48)),
        },
        8: {
            "Name": "Sand",
            "filename": "sand",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/sand.png').convert_alpha(), (48, 48)),
        },
        9: {
            "Name": "Oak Wood",
            "filename": "oak_planks",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_planks.png').convert_alpha(), (48, 48)),
        },
        10: {
            "Name": "Oak Log",
            "filename": "oak_log",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_log.png').convert_alpha(), (48, 48)),
        },
        11: {
            "Name": "Oak Leaves",
            "filename": "oak_leaves",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/oak_leaves.png').convert_alpha(), (48, 48)),
        },
        12: {
            "Name": "Bedrock",
            "filename": "bedrock",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/bedrock.png').convert_alpha(), (48, 48)),
        },
        13: {
            "Name": "Grass",
            "filename": "grass",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/grass.png').convert_alpha(), (48, 48)),
        },
        14: {
            "Name": "TNT",
            "filename": "tnt_side",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/tnt_side.png').convert_alpha(), (48, 48)),
        },
        15: {
            "Name": "Workbench",
            "filename": "crafting_table_front",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/crafting_table_front.png').convert_alpha(), (48, 48)),
        },
        16: {
            "Name": "Furnace",
            "filename": "furnace_front_on",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/furnace_front_on.png').convert_alpha(), (48, 48)),
        },
        17: {
            "Name": "Chest",
            "filename": "barrel_top",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/barrel_top.png').convert_alpha(), (48, 48)),
        },
        18: {
            "Name": "Magma Block",
            "filename": "magma",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/magma.png').convert_alpha(), (48, 48)),
        },
        19: {
            "Name": "Lantern",
            "filename": "jack_o_lantern",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/jack_o_lantern.png').convert_alpha(), (48, 48)),
        },
        20: {
            "Name": "Glowstone",
            "filename": "glowstone",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/glowstone.png').convert_alpha(), (48, 48)),
        },
        21: {
            "Name": "Glass",
            "filename": "glass",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/glass.png').convert_alpha(), (48, 48)),
        },
        22: {
            "Name": "Fence",
            "filename": "fence",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/fence.png').convert_alpha(), (48, 48)),
        },
        23: {
            "Name": "Iron Bars",
            "filename": "iron_bars",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_bars.png').convert_alpha(), (48, 48)),
        },
        24: {
            "Name": "Iron Block",
            "filename": "iron_block",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_block.png').convert_alpha(), (48, 48)),
        },
        25: {
            "Name": "Gold Block",
            "filename": "gold_block",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/gold_block.png').convert_alpha(), (48, 48)),
        },
        26: {
            "Name": "Diamond Block",
            "filename": "diamond_block",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/diamond_block.png').convert_alpha(), (48, 48)),
        },
        27: {
            "Name": "Emerald Block",
            "filename": "emerald_block",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/emerald_block.png').convert_alpha(), (48, 48)),
        },
        28: {
            "Name": "Coal Block",
            "filename": "coal_block",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/coal_block.png').convert_alpha(), (48, 48)),
        },
        29: {
            "Name": "Coal Ore",
            "filename": "coal_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/coal_ore.png').convert_alpha(), (48, 48)),
        },
        30: {
            "Name": "Iron Ore",
            "filename": "iron_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/iron_ore.png').convert_alpha(), (48, 48)),
        },
        31: {
            "Name": "Gold Ore",
            "filename": "gold_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/gold_ore.png').convert_alpha(), (48, 48)),
        },
        32: {
            "Name": "Diamond Ore",
            "filename": "diamond_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/diamond_ore.png').convert_alpha(), (48, 48)),
        },
        33: {
            "Name": "Emerald Ore",
            "filename": "emerald_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/emerald_ore.png').convert_alpha(), (48, 48)),
        },
        34: {
            "Name": "Ladder",
            "filename": "ladder",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/ladder.png').convert_alpha(), (48, 48)),
        },
        35: {
            "Name": "Rose",
            "filename": "poppy",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/poppy.png').convert_alpha(), (48, 48)),
        },
        36: {
            "Name": "Deepslate",
            "filename": "deepslate",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate.png').convert_alpha(), (48, 48)),
        },
        37: {
            "Name": "Deepslate Iron Ore",
            "filename": "deepslate_iron_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_iron_ore.png').convert_alpha(), (48, 48)),
        },
        38: {
            "Name": "Deepslate Gold Ore",
            "filename": "deepslate_gold_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_gold_ore.png').convert_alpha(), (48, 48)),
        },
        39: {
            "Name": "Deepslate Diamond Ore",
            "filename": "deepslate_diamond_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_diamond_ore.png').convert_alpha(), (48, 48)),
        },
        40: {
            "Name": "Deepslate Emerald Ore",
            "filename": "deepslate_emerald_ore",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/deepslate_emerald_ore.png').convert_alpha(), (48, 48)),
        },
        41: {
            "Name": "Sand",
            "filename": "sand",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/blocks/sand.png').convert_alpha(), (48, 48)),
        },
        1001: {
            "Name": "Iron Ingot",
            "filename": "iron_ingot",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/iron_ingot.png').convert_alpha(), (48, 48)),
        },
        1002: {
            "Name": "Gold Ingot",
            "filename": "gold_ingot",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/gold_ingot.png').convert_alpha(), (48, 48)),
        },
        1003: {
            "Name": "Diamond",
            "filename": "diamond",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/diamond.png').convert_alpha(), (48, 48)),
        },
        1004: {
            "Name": "Emerald",
            "filename": "emerald",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/emerald.png').convert_alpha(), (48, 48)),
        },
        1005: {
            "Name": "Coal",
            "filename": "coal",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/coal.png').convert_alpha(), (48, 48)),
        },
        1006: {
            "Name": "Raw Iron",
            "filename": "raw_iron",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/raw_iron.png').convert_alpha(), (48, 48)),
        },
        1007: {
            "Name": "Raw Gold",
            "filename": "raw_gold",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/raw_gold.png').convert_alpha(), (48, 48)),
        },
        1008: {
            "Name": "Stick",
            "filename": "stick",
            "Texture": pygame.transform.scale(pygame.image.load('game/assets/items/stick.png').convert_alpha(), (48, 48)),
        },
    }

    return item_data