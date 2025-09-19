import pygame
from utils.ui import *
import sys
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
logo = pygame.image.load('game/assets/ui/Microcraft.png')
trashbin = pygame.image.load('game/assets/ui/trashbin.png')

#custom cursors
cur_square = []
cur_hammer = []
cur_pointer = []
cur_star = []
cur_circle = []
cur_loading= []
cursor_custom()
cur = cur_square

#load block sprites
block_data = load_blocks()
pygame.display.set_icon(block_data[18]["Texture"])

#Variables
clock = pygame.time.Clock()
block_surface = [pygame.Surface((4096, 4096), pygame.SRCALPHA) for _ in range(9)]
GAMEPATH = os.path.join(os.path.expanduser("~"), "Documents", "MicroCraft") #game files path
os.makedirs(GAMEPATH, exist_ok=True)
main_font = pygame.font.SysFont('impact', 30)
OX = 0 #origin
OY = 0
SCALE = 4
current_scene = 0
world_name = "Err"
chunk = []
loaded_chunks = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
block_in_reach = False
selected_block = (0, 0)
block_in_hand = 1
show_esc = False
show_inv = False
show_debug = False
paused = False
loading_info = ["", ""]
loading_timeout = 0
img_save_timeout = 0

#load texturepack
if os.path.exists(f"{GAMEPATH}/settings.json"):
    with open(f"{GAMEPATH}/settings.json", "r") as file:
        read_data = json.load(file)
    if read_data["CurrentTexturepack"] != "none":
        texturepack_load(read_data["CurrentTexturepack"])
else:
    with open(f"{GAMEPATH}/settings.json", "w") as file:
        read_data = {"CurrentTexturepack": "none"}
        json.dump(read_data, file, indent=2)


RUNNING = True
while RUNNING:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4:
                RUNNING = False
        if event.type == pygame.QUIT:
            RUNNING = False

    cur = cur_square
    surface.fill((200, 250, 255))
    match current_scene:
        case 0:
            scene_menu(events)
        case 1:
            scene_menu_select(events)
        case 2:
            scene_game_create()
        case 3:
            #scene_game_load()
            print("ERR: Scene can not be accessed.")
        case 4:
            scene_game(events)
        case 5:
            scene_menu_texturepacks(events)
        case 6:
            scene_loading(loading_info[0], loading_info[1])

    if show_esc or show_inv:
        paused = True
    else:
        paused = False

    pygame.mouse.set_cursor(cur[0], cur[1], cur[2], cur[3])
    #pygame.mouse.set_cursor(cur)
    clock.tick(40)
    pygame.display.update()


pygame.quit()