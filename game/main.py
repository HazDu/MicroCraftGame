from tkinter import messagebox
import pygame
import zipfile
from utils.ui import *
import sys
import platform
from utils.block_ids import *
from utils.item_ids import *
from utils.cursor import *
from scenes.menu import *
from scenes.game import *
from utils.recipes import *
pygame.init()

#screen setup
surface = pygame.display.set_mode((1920, 1080), pygame.SRCALPHA, 32, 0)
pygame.display.set_caption("Microcraft")
sys.setrecursionlimit(100000)
pygame.display.set_icon(surface)

#load images
logo = pygame.image.load('game/assets/ui/Microcraft.png').convert_alpha()
trashbin = pygame.image.load('game/assets/ui/trashbin.png').convert_alpha()
explorer = pygame.image.load('game/assets/ui/explorer.png').convert_alpha()
def_img = pygame.image.load("game/assets/ui/pack.png").convert_alpha()
img_empty = pygame.Surface((1, 1), pygame.SRCALPHA, 32)
img_mod_loaded = pygame.image.load("game/assets/ui/mod_loaded.png").convert_alpha()
img_mod_unloaded = pygame.image.load("game/assets/ui/mod_unloaded.png").convert_alpha()
img_hotbar = pygame.transform.scale(pygame.image.load("game/assets/ui/hotbar.png"), (512, 64)).convert_alpha()
img_hotbar_sel = pygame.transform.scale(pygame.image.load("game/assets/ui/hotbar_selector.png"), (64, 64)).convert_alpha()
img_slot = pygame.transform.scale(pygame.image.load("game/assets/ui/slot.png"), (64, 64)).convert_alpha()
img_double_arrow = pygame.transform.scale(pygame.image.load("game/assets/ui/double_arrow.png"), (64, 64)).convert_alpha()
img_button = pygame.image.load("game/assets/ui/button.png").convert_alpha()

#custom cursors
cur_square = []
cur_hammer = []
cur_pointer = []
cur_star = []
cur_circle = []
cur_loading = []
cursor_custom()
cur = cur_square

#load block and item data
block_data = load_blocks()
item_data = load_items()
recipe_data = load_recipes()
pygame.display.set_icon(block_data[18]["Texture"])

#Variables
SYSTEM = platform.system()
if SYSTEM == "Windows":
    GAMEPATH = os.path.join(os.path.expanduser("~"), "Documents", "MicroCraft")  # game files path
elif SYSTEM == "Linux":
    GAMEPATH = os.path.join(os.path.expanduser("~"), "MicroCraft")
else:
    messagebox.showerror("Error", "Your OS is not compatible with this game! (Imagine using Mac eew.)")
    pygame.quit()
MODPATH = f"{GAMEPATH}/mods"
clock = pygame.time.Clock()
block_surface = [pygame.Surface((4096, 4096), pygame.SRCALPHA) for _ in range(9)]
os.makedirs(GAMEPATH, exist_ok=True)
subdir = f"{GAMEPATH}/saves"
os.makedirs(subdir, exist_ok=True)
subdir = f"{GAMEPATH}/mods"
os.makedirs(subdir, exist_ok=True)
main_font = pygame.font.SysFont('impact', 30)
fnt_cons20 =  pygame.font.SysFont('consolas', 20)
OX = 0 #origin
OY = 0
SCALE = 4
current_scene = 0
world_name = "Err"
#chunk = []
loaded_chunks = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
block_in_reach = False
reach = 300
selected_block = (0, 0)
block_in_hand = 1
gamemode = 0
show_esc = False
show_inv = False
show_debug = False
menu_create_input_box = [0, ""]
menu_create_worldname_input = ""
menu_create_seed_input = ""
menu_create_worldtype = 0
paused = False
loaded_mods = []
mods_active = False
loading_info = ["", ""]
loading_timeout = 0
img_save_timeout = 0
tree_queue = [[],[],[],[],[],[],[],[],[]]
chunk_render_queue = []
mod_reinit = [False, ""]
menu_scroll = 0
break_progress = 0
break_speed = 1
hotbar_slot = 0
sky_color = (200, 250, 255)
item_entities = []
inventory = [[0,0] for _ in range(40)]
inv_mouse = [0, 0]
chunk_buffer = []
container_open = [False, 0]
action_title = [img_empty, 0]
workbench_storage = [[0,0] for _ in range(10)]
growing_saplings = []

#load settings
if os.path.exists(f"{GAMEPATH}/settings.json"):
    with open(f"{GAMEPATH}/settings.json", "r") as file:
        read_data = json.load(file)
    if read_data["CurrentTexturepack"] != "none":
        texturepack_load(read_data["CurrentTexturepack"])
    if len(read_data["LoadedMods"]) > 0:
        loaded_mods = read_data["LoadedMods"]
        for mod in loaded_mods:
            if not os.path.exists(f"{MODPATH}/{mod}"):
                loaded_mods.remove(mod)
                with open(f"{GAMEPATH}/settings.json", "r") as f:
                    rd = json.load(f)
                    rd["LoadedMods"] = loaded_mods
                with open(f"{GAMEPATH}/settings.json", "w")  as f:
                    json.dump(rd, f, indent=2)

        if len(read_data["LoadedMods"]) > 0:
            mods_active = True
else:
    with open(f"{GAMEPATH}/settings.json", "w") as file:
        data = {
            "CurrentTexturepack": "none",
            "LoadedMods": []
        }
        json.dump(data, file, indent=2)

if mods_active:
    for mod in loaded_mods:
        print(MODPATH)
        with zipfile.ZipFile(f"{MODPATH}/{mod}", 'r') as zip_ref:
            if "scripts/init.py" in zip_ref.namelist():
                with zip_ref.open("scripts/init.py") as file:
                    exec(file.read())
RUNNING = True
while RUNNING:
    EVENTS = pygame.event.get()
    for event in EVENTS:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4:
                RUNNING = False
        if event.type == pygame.MOUSEWHEEL:
            menu_scroll += event.y*30
        if event.type == pygame.QUIT:
            RUNNING = False

    cur = cur_square
    surface.fill(sky_color)

    if mods_active:
        for mod in loaded_mods:
            with zipfile.ZipFile(f"{main.MODPATH}/{mod}", 'r') as zip_ref:
                if "scripts/main_loop.py" in zip_ref.namelist():
                    with zip_ref.open("scripts/main_loop.py") as file:
                        exec(file.read())

    if len(loaded_mods) > 0:
        mods_active = True
    else:
        mods_active = False

    if mod_reinit[0]:
        with zipfile.ZipFile(f"{main.MODPATH}/{mod_reinit[1]}", 'r') as zip_ref:
            with zip_ref.open("scripts/init.py") as file:
                exec(file.read())
        mod_reinit[0] = False

    match current_scene:
        case 0:
            scene_menu(EVENTS)
        case 1:
            scene_menu_select(EVENTS)
        case 2:
            scene_game_create()
        case 3:
            #scene_game_load()
            print("ERR: Scene can not be accessed.")
        case 4:
            scene_game(EVENTS)
        case 5:
            scene_menu_texturepacks(EVENTS)
        case 6:
            scene_loading(loading_info[0], loading_info[1])
        case 7:
            scene_menu_mods(EVENTS)
        case 8:
            scene_menu_create()

    if show_esc or show_inv:
        paused = True
    else:
        paused = False

    pygame.mouse.set_cursor(cur[0], cur[1], cur[2], cur[3])
    clock.tick(60)
    pygame.display.flip()



pygame.quit()