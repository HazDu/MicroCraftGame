from tkinter import messagebox
import pygame
from utils.ui import *
import sys
import platform
from utils.block_ids import *
from utils.cursor import *
from scenes.menu import *
from scenes.game import *
#EVERYTHING IS SCALED BY 4
pygame.init()

#screen setup
surface = pygame.display.set_mode((1920, 1080), pygame.SRCALPHA, 32, 0)
pygame.display.set_caption("Microcraft")
sys.setrecursionlimit(100000)
pygame.display.set_icon(surface)

#load images
logo = pygame.image.load('game/assets/ui/Microcraft.png')
trashbin = pygame.image.load('game/assets/ui/trashbin.png')
explorer = pygame.image.load('game/assets/ui/explorer.png')
def_img = pygame.image.load("game/assets/ui/pack.png")
img_mod_loaded = pygame.image.load("game/assets/ui/mod_loaded.png")
img_mod_unloaded = pygame.image.load("game/assets/ui/mod_unloaded.png")

#custom cursors
cur_square = []
cur_hammer = []
cur_pointer = []
cur_star = []
cur_circle = []
cur_loading = []
cursor_custom()
cur = cur_square

#load block sprites
block_data = load_blocks()
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
OX = 0 #origin
OY = 0
SCALE = 4
current_scene = 0
world_name = "Err"
#chunk = []
loaded_chunks = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
block_in_reach = False
main.reach = 300
selected_block = (0, 0)
block_in_hand = 1
gamemode = 0
show_esc = False
show_inv = False
show_debug = False
menu_create_worldname_input_box = False
menu_create_seed_input_box = False
menu_create_worldname_input = ""
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
sky_color = (200, 250, 255)

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
    pygame.display.update()



pygame.quit()