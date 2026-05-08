import zipfile
import pygame
import random
import math
import numpy as np
import copy
import ast
from game.utils.ui import *
from game.utils.block_interactions import *
from game.utils.util_functs import *
from game.utils.generator import *
import __main__ as main

TOOL_TIER_SPEED = {
    1: 1.6,  # stone
    2: 2.2,  # iron
    3: 2.8,  # gold
    4: 3.4,  # diamond
}
HAND_BREAK_MULTIPLIER = 0.35
WRONG_TOOL_MULTIPLIER = 0.2


def is_tool_item(item_id):
    return item_id in main.item_data and "ToolType" in main.item_data[item_id]


def get_slot_tool_data(slot_index):
    item_id = main.inventory[slot_index][0]
    if item_id == 0 or item_id not in main.item_data:
        return None
    item = main.item_data[item_id]
    if "ToolType" not in item:
        return None
    return item


def calc_break_speed_multiplier(block_id, slot_index):
    block_tool = main.block_data[block_id].get("BreakingTool")
    tool_item = get_slot_tool_data(slot_index)

    if tool_item is None:
        return HAND_BREAK_MULTIPLIER

    if block_tool is None:
        return HAND_BREAK_MULTIPLIER

    if tool_item["ToolType"] != block_tool:
        return WRONG_TOOL_MULTIPLIER

    return TOOL_TIER_SPEED.get(tool_item.get("Tier", 1), 1.0)


def damage_tool_in_slot(slot_index):
    tool_item = get_slot_tool_data(slot_index)
    if tool_item is None:
        return

    max_dur = tool_item.get("MaxDurability", 0)
    if max_dur <= 0:
        return

    main.inventory_durability[slot_index] += 1
    if main.inventory_durability[slot_index] >= max_dur:
        main.inventory[slot_index] = [0, 0]
        main.inventory_durability[slot_index] = 0
        if main.hotbar_slot == slot_index:
            main.block_in_hand = 0

#classes
class Player:
    def __init__(self):
        self.speed = 6
        self.x = 0
        self.y = 0
        self.jump_vel = 0.0
        self.jump_strength = 14.0
        self.gravity = 1
        self.max_fall_speed = 26.0
        self.sprite = pygame.transform.scale(pygame.image.load(resource_path("game/assets/entities/T-Player.png")), (64, 64))
        self.hitbox = {
            "top": 32,
            "left": 17,
            "bottom": -32,
            "right": -17,
        }

    def _get_player_rect_world(self):
        sprite_half_w = self.sprite.get_width() / 2
        sprite_half_h = self.sprite.get_height() / 2

        center_x = main.surface.get_width() / 2
        center_y = main.surface.get_height() / 2

        screen_left = center_x - sprite_half_w + self.hitbox["left"]
        screen_right = center_x + sprite_half_w + self.hitbox["right"]
        screen_top = center_y - sprite_half_h + 4
        screen_bottom = center_y + sprite_half_h - 2

        world_left = round(screen_left - main.OX)
        world_right = round(screen_right - main.OX)
        world_top = round(screen_top - main.OY)
        world_bottom = round(screen_bottom - main.OY)

        return pygame.Rect(world_left, world_top, world_right - world_left, world_bottom - world_top)

    def _get_block_id(self, tile_x, tile_y):
        chunk_x = math.floor(tile_x / 64)
        chunk_y = math.floor(tile_y / 64)

        if not (-1 <= chunk_x <= 1 and -1 <= chunk_y <= 1):
            return 0

        local_x = tile_x % 64
        local_y = tile_y % 64
        chunk = (chunk_y + 1) * 3 + (chunk_x + 1)

        return main.loaded_chunks[chunk][0][local_x][local_y]

    def _is_collidable_tile(self, tile_x, tile_y):
        block_id = self._get_block_id(tile_x, tile_y)
        return main.block_data[block_id]["Collidable"]

    def _move_rect_x(self, rect, dx):
        if dx == 0:
            return rect, 0

        moved = rect.move(dx, 0)
        left_tile = moved.left // 64
        right_tile = (moved.right - 1) // 64
        top_tile = moved.top // 64
        bottom_tile = (moved.bottom - 1) // 64

        x_range = range(left_tile, right_tile + 1)
        if dx < 0:
            x_range = range(right_tile, left_tile - 1, -1)

        for tile_x in x_range:
            for tile_y in range(top_tile, bottom_tile + 1):
                if not self._is_collidable_tile(tile_x, tile_y):
                    continue

                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if moved.colliderect(tile_rect):
                    if dx > 0:
                        moved.right = min(moved.right, tile_rect.left)
                    else:
                        moved.left = max(moved.left, tile_rect.right)

        return moved, moved.x - rect.x

    def _move_rect_y(self, rect, dy):
        if dy == 0:
            return rect, 0

        moved = rect.move(0, dy)
        left_tile = moved.left // 64
        right_tile = (moved.right - 1) // 64
        top_tile = moved.top // 64
        bottom_tile = (moved.bottom - 1) // 64

        y_range = range(top_tile, bottom_tile + 1)
        if dy < 0:
            y_range = range(bottom_tile, top_tile - 1, -1)

        for tile_y in y_range:
            for tile_x in range(left_tile, right_tile + 1):
                if not self._is_collidable_tile(tile_x, tile_y):
                    continue

                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if moved.colliderect(tile_rect):
                    if dy > 0:
                        moved.bottom = min(moved.bottom, tile_rect.top)
                    else:
                        moved.top = max(moved.top, tile_rect.bottom)

        return moved, moved.y - rect.y

    def _is_on_ground(self, rect):
        check_rect = rect.move(0, 1)
        left_tile = check_rect.left // 64
        right_tile = (check_rect.right - 1) // 64
        top_tile = check_rect.top // 64
        bottom_tile = (check_rect.bottom - 1) // 64

        for tile_y in range(top_tile, bottom_tile + 1):
            for tile_x in range(left_tile, right_tile + 1):
                if not self._is_collidable_tile(tile_x, tile_y):
                    continue
                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if check_rect.colliderect(tile_rect):
                    return True
        return False

    def _inside_block(self, rect, block_id):
        left_tile = rect.left // 64
        right_tile = (rect.right - 1) // 64
        top_tile = rect.top // 64
        bottom_tile = (rect.bottom - 1) // 64

        for tile_y in range(top_tile, bottom_tile + 1):
            for tile_x in range(left_tile, right_tile + 1):
                if self._get_block_id(tile_x, tile_y) != block_id:
                    continue
                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if rect.colliderect(tile_rect):
                    return True
        return False

    def player_default(self):
        if not main.show_inv and not main.show_esc:
            keys = pygame.key.get_pressed()

            self.x = main.OX - (main.surface.get_width() / 2)
            self.y = main.OY - (main.surface.get_height() / 2)
            player_rect = self._get_player_rect_world()

            move_x = 0
            if keys[pygame.K_a]:
                move_x -= self.speed
            if keys[pygame.K_d]:
                move_x += self.speed

            if move_x != 0:
                player_rect, moved_x = self._move_rect_x(player_rect, move_x)
                main.OX -= moved_x

            inside_ladder = self._inside_block(player_rect, 34)
            on_ground = self._is_on_ground(player_rect)

            if inside_ladder and keys[pygame.K_SPACE]:
                player_rect, moved_y = self._move_rect_y(player_rect, -self.speed)
                main.OY -= moved_y
                if moved_y == 0:
                    self.jump_vel = 0
            else:
                jump_pressed = False
                for event in main.EVENTS:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        jump_pressed = True
                        break

                if jump_pressed and (on_ground or main.gamemode == 1):
                    self.jump_vel = -self.jump_strength

                self.jump_vel = min(self.jump_vel + self.gravity, self.max_fall_speed)
                wanted_move_y = int(round(self.jump_vel))

                if wanted_move_y != 0:
                    player_rect, moved_y = self._move_rect_y(player_rect, wanted_move_y)
                    main.OY -= moved_y
                else:
                    moved_y = 0

                if moved_y != wanted_move_y:
                    self.jump_vel = 0
                elif self._is_on_ground(player_rect) and self.jump_vel > 0:
                    self.jump_vel = 0

            self.x = main.OX - (main.surface.get_width() / 2)
            self.y = main.OY - (main.surface.get_height() / 2)

        main.surface.blit(self.sprite, (main.surface.get_width() / 2 - 32, main.surface.get_height() / 2 - 32))

class Item:
    def __init__(self):
        self.item_id = 0
        self.amount = 0
        self.x = 0
        self.y = 0
        self.lifetime = 0
        self.rot = 0
    def item_default(self):
        draw_coords = world_coords_to_screen_coords(self.x, self.y)
        if -32 < draw_coords[0] < 1952 and -32 < draw_coords[1] < 1112:
            img = pygame.transform.rotozoom(main.item_data[self.item_id]["Texture"], round(self.rot), 0.66666)
            if self.lifetime > 1500:
                img = tint_image(img, (255, 0, 0, 50))

            rect = img.get_rect()
            rect.center = draw_coords[0], draw_coords[1]
            main.surface.blit(img, rect)
            self.lifetime += 1
            self.rot += 0.5

        #print(f"self: {self.x} {self.y} player: {player.x} {player.y}")
        if 10 < point_distance((self.x, self.y), (player.x*-1, player.y*-1)) < 120 and any(sub[0] == 0 for sub in main.inventory):
            self.x, self.y = move_towarts((player.x*-1, player.y*-1), (self.x, self.y), 12)
        elif point_distance((self.x, self.y), (player.x*-1, player.y*-1)) <= 10:
            item_stored = False
            for i in range(len(main.inventory)):
                if is_tool_item(self.item_id):
                    continue
                if main.inventory[i][0] == self.item_id and main.inventory[i][1]+self.amount <= 256:
                    main.inventory[i][1] += self.amount
                    self.lifetime = 99999
                    item_stored = True
                    break
            if not item_stored:
                for i in range(len(main.inventory)):
                    if main.inventory[i][0] == 0:
                        main.inventory[i][0] = self.item_id
                        main.inventory[i][1] += self.amount
                        main.inventory_durability[i] = 0
                        self.lifetime = 99999
                        item_stored = True
                        break

class Pig:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = 64
        self.height = 64
        self.hitbox = {
            "left": 8,
            "right": -8,
            "top": 6,
            "bottom": -2,
        }
        self.speed = 1
        self.vx = 0
        self.vy = 0
        self.gravity = 0.7
        self.max_fall_speed = 16
        self.direction = random.choice([-1, 1])
        self.walk_timer = random.randint(60, 180)
        self.idle_timer = random.randint(0, 45)
        self.jump_strength = 12
        self.jump_cooldown = random.randint(50, 150)
        self.health = 5
        self.flash_timer = 0
        self.max_flash_timer = 8
        self._sprite_right = None
        self._sprite_left = None
        self._sprite_source = None

    def _refresh_sprite_cache(self):
        source_texture = pygame.image.load(resource_path('game/assets/entities/pig.png')).convert_alpha()
        if self._sprite_source is source_texture and self._sprite_right is not None:
            return
        self._sprite_source = source_texture
        self._sprite_right = pygame.transform.scale(source_texture, (self.width, self.height))
        self._sprite_left = pygame.transform.flip(self._sprite_right, True, False)

    def _get_sprite(self):
        self._refresh_sprite_cache()
        if self.direction > 0:
            return self._sprite_left
        return self._sprite_right

    def _get_rect(self):
        return pygame.Rect(
            int(self.x + self.hitbox["left"]),
            int(self.y + self.hitbox["top"]),
            self.width + self.hitbox["right"] - self.hitbox["left"],
            self.height + self.hitbox["bottom"] - self.hitbox["top"],
        )

    def _get_center(self):
        return self.x + (self.width / 2), self.y + (self.height / 2)

    def try_hit(self):
        self.health -= 1
        self.flash_timer = self.max_flash_timer
        return self.health <= 0

    def _get_block_id(self, tile_x, tile_y):
        chunk_x = math.floor(tile_x / 64)
        chunk_y = math.floor(tile_y / 64)
        if not (-1 <= chunk_x <= 1 and -1 <= chunk_y <= 1):
            return 0

        local_x = tile_x % 64
        local_y = tile_y % 64
        chunk = (chunk_y + 1) * 3 + (chunk_x + 1)
        return main.loaded_chunks[chunk][0][local_x][local_y]

    def _is_collidable_tile(self, tile_x, tile_y):
        block_id = self._get_block_id(tile_x, tile_y)
        return main.block_data[block_id]["Collidable"]

    def _move_rect_x(self, rect, dx):
        if dx == 0:
            return rect, 0

        moved = rect.move(dx, 0)
        left_tile = moved.left // 64
        right_tile = (moved.right - 1) // 64
        top_tile = moved.top // 64
        bottom_tile = (moved.bottom - 1) // 64

        x_range = range(left_tile, right_tile + 1)
        if dx < 0:
            x_range = range(right_tile, left_tile - 1, -1)

        for tile_x in x_range:
            for tile_y in range(top_tile, bottom_tile + 1):
                if not self._is_collidable_tile(tile_x, tile_y):
                    continue
                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if moved.colliderect(tile_rect):
                    if dx > 0:
                        moved.right = min(moved.right, tile_rect.left)
                    else:
                        moved.left = max(moved.left, tile_rect.right)

        return moved, moved.x - rect.x

    def _move_rect_y(self, rect, dy):
        if dy == 0:
            return rect, 0

        moved = rect.move(0, dy)
        left_tile = moved.left // 64
        right_tile = (moved.right - 1) // 64
        top_tile = moved.top // 64
        bottom_tile = (moved.bottom - 1) // 64

        y_range = range(top_tile, bottom_tile + 1)
        if dy < 0:
            y_range = range(bottom_tile, top_tile - 1, -1)

        for tile_y in y_range:
            for tile_x in range(left_tile, right_tile + 1):
                if not self._is_collidable_tile(tile_x, tile_y):
                    continue
                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if moved.colliderect(tile_rect):
                    if dy > 0:
                        moved.bottom = min(moved.bottom, tile_rect.top)
                    else:
                        moved.top = max(moved.top, tile_rect.bottom)

        return moved, moved.y - rect.y

    def _is_on_ground(self, rect):
        check_rect = rect.move(0, 1)
        left_tile = check_rect.left // 64
        right_tile = (check_rect.right - 1) // 64
        top_tile = check_rect.top // 64
        bottom_tile = (check_rect.bottom - 1) // 64

        for tile_y in range(top_tile, bottom_tile + 1):
            for tile_x in range(left_tile, right_tile + 1):
                if not self._is_collidable_tile(tile_x, tile_y):
                    continue
                tile_rect = pygame.Rect(tile_x * 64, tile_y * 64, 64, 64)
                if check_rect.colliderect(tile_rect):
                    return True
        return False

    def pig_default(self, active=True):
        if active:
            rect = self._get_rect()
            on_ground = self._is_on_ground(rect)

            if self.idle_timer > 0:
                self.idle_timer -= 1
                self.vx = 0
            else:
                self.vx = self.direction * self.speed
                self.walk_timer -= 1

                # Randomly turn around while walking, even with free path.
                if random.randint(1, 220) == 1:
                    self.direction *= -1
                    self.vx = self.direction * self.speed

                if self.walk_timer <= 0:
                    if random.randint(1, 100) <= 45:
                        self.idle_timer = random.randint(100, 500)
                        self.walk_timer = random.randint(100, 500)
                        self.vx = 0
                    else:
                        if random.randint(1, 100) <= 40:
                            self.direction *= -1
                        self.walk_timer = random.randint(90, 220)
                        self.vx = self.direction * self.speed

            if self.jump_cooldown > 0:
                self.jump_cooldown -= 1

            if on_ground and self.jump_cooldown <= 0 and random.randint(1, 180) == 1:
                self.vy = -self.jump_strength
                self.jump_cooldown = random.randint(90, 220)

            rect, moved_x = self._move_rect_x(rect, int(self.vx))
            if self.vx != 0 and moved_x == 0:
                self.walk_timer = random.randint(45, 130)
                # On wall collision, jump forward instead of turning around.
                if on_ground and self.jump_cooldown <= 0:
                    self.vy = -self.jump_strength
                    self.jump_cooldown = random.randint(90, 220)
                else:
                    self.vx = 0

            self.vy = min(self.vy + self.gravity, self.max_fall_speed)
            wanted_move_y = int(round(self.vy))
            rect, moved_y = self._move_rect_y(rect, wanted_move_y)
            if moved_y != wanted_move_y:
                self.vy = 0
            elif self._is_on_ground(rect) and self.vy > 0:
                self.vy = 0

            self.x = rect.x - self.hitbox["left"]
            self.y = rect.y - self.hitbox["top"]

        if self.flash_timer > 0:
            self.flash_timer -= 1

        draw_coords = world_coords_to_screen_coords(self.x, self.y)
        if -self.width < draw_coords[0] < main.surface.get_width() and -self.height < draw_coords[1] < main.surface.get_height():
            sprite = self._get_sprite()
            if self.flash_timer > 0:
                sprite = tint_image(sprite, (255, 0, 0, 140))
            main.surface.blit(sprite, draw_coords)


class Cow(Pig):
    def _refresh_sprite_cache(self):
        source_texture = main.img_cow
        if self._sprite_source is source_texture and self._sprite_right is not None:
            return
        self._sprite_source = source_texture
        self._sprite_right = pygame.transform.scale(source_texture, (self.width, self.height))
        self._sprite_left = pygame.transform.flip(self._sprite_right, True, False)

    def cow_default(self, active=True):
        self.pig_default(active=active)


class Sheep(Pig):
    def _refresh_sprite_cache(self):
        source_texture = main.img_sheep
        if self._sprite_source is source_texture and self._sprite_right is not None:
            return
        self._sprite_source = source_texture
        self._sprite_right = pygame.transform.scale(source_texture, (self.width, self.height))
        self._sprite_left = pygame.transform.flip(self._sprite_right, True, False)

    def sheep_default(self, active=True):
        self.pig_default(active=active)


def pig_in_loaded_chunks(pig):
    pig_chunk_x = math.floor(pig.x / 4096)
    pig_chunk_y = math.floor(pig.y / 4096)
    return -1 <= pig_chunk_x <= 1 and -1 <= pig_chunk_y <= 1


def remove_unloaded_pigs():
    main.pig_entities = [pig for pig in main.pig_entities if pig_in_loaded_chunks(pig)]


def cow_in_loaded_chunks(cow):
    cow_chunk_x = math.floor(cow.x / 4096)
    cow_chunk_y = math.floor(cow.y / 4096)
    return -1 <= cow_chunk_x <= 1 and -1 <= cow_chunk_y <= 1


def remove_unloaded_cows():
    main.cow_entities = [cow for cow in main.cow_entities if cow_in_loaded_chunks(cow)]


def sheep_in_loaded_chunks(sheep):
    sheep_chunk_x = math.floor(sheep.x / 4096)
    sheep_chunk_y = math.floor(sheep.y / 4096)
    return -1 <= sheep_chunk_x <= 1 and -1 <= sheep_chunk_y <= 1


def remove_unloaded_sheep():
    main.sheep_entities = [sheep for sheep in main.sheep_entities if sheep_in_loaded_chunks(sheep)]


def is_cursor_in_interact_range(mouse_pos):
    if main.show_inv or main.show_esc or main.paused:
        return False
    player_center = (main.surface.get_width() / 2, main.surface.get_height() / 2)
    return point_distance(player_center, mouse_pos) < main.reach


def find_clicked_pig(mouse_world_pos):
    clicked = []
    for pig in main.pig_entities:
        if pig._get_rect().collidepoint(mouse_world_pos):
            pig_center = pig._get_center()
            clicked.append((point_distance(mouse_world_pos, pig_center), pig))

    if len(clicked) == 0:
        return None

    clicked.sort(key=lambda entry: entry[0])
    return clicked[0][1]


def find_clicked_cow(mouse_world_pos):
    clicked = []
    for cow in main.cow_entities:
        if cow._get_rect().collidepoint(mouse_world_pos):
            cow_center = cow._get_center()
            clicked.append((point_distance(mouse_world_pos, cow_center), cow))

    if len(clicked) == 0:
        return None

    clicked.sort(key=lambda entry: entry[0])
    return clicked[0][1]


def find_clicked_sheep(mouse_world_pos):
    clicked = []
    for sheep in main.sheep_entities:
        if sheep._get_rect().collidepoint(mouse_world_pos):
            sheep_center = sheep._get_center()
            clicked.append((point_distance(mouse_world_pos, sheep_center), sheep))

    if len(clicked) == 0:
        return None

    clicked.sort(key=lambda entry: entry[0])
    return clicked[0][1]


def find_chunk_spawn_position(chunk_index):
    chunk_blocks = main.loaded_chunks[chunk_index][0]
    spawn_candidates = []
    for x in range(64):
        for y in range(1, 63):
            if main.block_data[chunk_blocks[x][y]]["Collidable"]:
                continue
            if main.block_data[chunk_blocks[x][y + 1]]["Collidable"]:
                spawn_candidates.append((x, y))
                break
    if len(spawn_candidates) == 0:
        return None
    return random.choice(spawn_candidates)


def try_spawn_pig_in_chunk(chunk_index, force=False):
    if len(main.pig_entities) >= 8:
        return False
    if chunk_index == 4:
        return False
    if not force and random.randint(1, 100) > 80:
        return False

    spawn_pos = find_chunk_spawn_position(chunk_index)
    if spawn_pos is None:
        return False

    main_chunk_coords = main.loaded_chunks[4][1]
    chunk_coords = main.loaded_chunks[chunk_index][1]
    rel_chunk_x = chunk_coords[0] - main_chunk_coords[0]
    rel_chunk_y = chunk_coords[1] - main_chunk_coords[1]
    pig_world_x = rel_chunk_x * 4096 + spawn_pos[0] * 64
    pig_world_y = rel_chunk_y * 4096 + spawn_pos[1] * 64
    main.pig_entities.append(Pig(pig_world_x, pig_world_y))
    return True


def try_spawn_cow_in_chunk(chunk_index, force=False):
    if len(main.cow_entities) >= 8:
        return False
    if chunk_index == 4:
        return False
    if not force and random.randint(1, 100) > 80:
        return False

    spawn_pos = find_chunk_spawn_position(chunk_index)
    if spawn_pos is None:
        return False

    main_chunk_coords = main.loaded_chunks[4][1]
    chunk_coords = main.loaded_chunks[chunk_index][1]
    rel_chunk_x = chunk_coords[0] - main_chunk_coords[0]
    rel_chunk_y = chunk_coords[1] - main_chunk_coords[1]
    cow_world_x = rel_chunk_x * 4096 + spawn_pos[0] * 64
    cow_world_y = rel_chunk_y * 4096 + spawn_pos[1] * 64
    main.cow_entities.append(Cow(cow_world_x, cow_world_y))
    return True


def try_spawn_sheep_in_chunk(chunk_index, force=False):
    if len(main.sheep_entities) >= 8:
        return False
    if chunk_index == 4:
        return False
    if not force and random.randint(1, 100) > 80:
        return False

    spawn_pos = find_chunk_spawn_position(chunk_index)
    if spawn_pos is None:
        return False

    main_chunk_coords = main.loaded_chunks[4][1]
    chunk_coords = main.loaded_chunks[chunk_index][1]
    rel_chunk_x = chunk_coords[0] - main_chunk_coords[0]
    rel_chunk_y = chunk_coords[1] - main_chunk_coords[1]
    sheep_world_x = rel_chunk_x * 4096 + spawn_pos[0] * 64
    sheep_world_y = rel_chunk_y * 4096 + spawn_pos[1] * 64
    main.sheep_entities.append(Sheep(sheep_world_x, sheep_world_y))
    return True


def scene_game_create():
    main.pig_entities = []
    main.cow_entities = []
    main.sheep_entities = []
    main.loaded_chunks = [
                            [create_chunk(), [-1, -1]],
                            [create_chunk(), [0, -1]],
                            [create_chunk(), [1, -1]],
                            [create_chunk(), [-1, 0]],
                            [create_chunk(), [0, 0]],
                            [create_chunk(), [1, 0]],
                            [create_chunk(), [-1, 1]],
                            [create_chunk(), [0, 1]],
                            [create_chunk(), [1, 1]]
    ]

    for chunk in range(9):
       generate_chunk_type(chunk, main.menu_create_worldtype)

    for chunk in [3, 4, 5]:
        for tree in main.tree_queue[chunk]:
            generate_tree(tree[0], tree[1], chunk)

    for chunk in [1, 3, 5, 7]:
        try_spawn_pig_in_chunk(chunk)
        try_spawn_cow_in_chunk(chunk)
        try_spawn_sheep_in_chunk(chunk)

    for chunk in range(9):
        render_blocks(0, chunk)
    main.current_scene = 4

def scene_game_load(path):
    with open(path + "/infos.json", "r") as file:
        read = json.load(file)
    main_chunk = read["CurrentChunk"]
    main.OX = read["PlayerX"]
    main.OY = read["PlayerY"]
    main.gamemode = read["GameMode"]
    main.inventory = read["Inventory"]
    main.inventory_durability = read.get("InventoryDurability", [0 for _ in range(40)])
    if len(main.inventory_durability) < len(main.inventory):
        main.inventory_durability += [0 for _ in range(len(main.inventory) - len(main.inventory_durability))]
    main.growing_saplings = read["Saplings"]
    main.daylight_time = read["DayTime"]
    main.container_savedata = read["ContainerData"]

    i = 0
    for y in range(main_chunk[1] -1, main_chunk[1] +2):
        for x in range(main_chunk[0] -1, main_chunk[0] +2):
            with open(path + f"/chunkdata/[{x}, {y}].chunk", "r") as file:
                main.loaded_chunks[i][0] = ast.literal_eval(file.read())
            main.loaded_chunks[i][1] = [x, y]
            i += 1

    for a in range(9):
        main.block_surface[a].fill((200, 250, 255))
        render_blocks(0, a)
    main.pig_entities = []
    main.cow_entities = []
    main.sheep_entities = []
    for chunk in [1, 3, 5, 7]:
        try_spawn_pig_in_chunk(chunk)
        try_spawn_cow_in_chunk(chunk)
        try_spawn_sheep_in_chunk(chunk)

    if main.gamemode == 0:
        main.break_speed = 1
    else:
        main.break_speed = 99999

    main.current_scene = 4


player = Player()
def scene_game(events):
    chunk_draw_count = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if 6016 > ((x * 4096) + main.OX + 4096) > 0 and 5176 > ((y * 4096) + main.OY + 4096) > 0:
                main.surface.blit(main.block_surface[chunk_draw_count], (main.OX + (x * 4096), main.OY + (y * 4096)))
            chunk_draw_count += 1

    #block interacting
    mouse = pygame.mouse.get_pos()
    mouse_world = (mouse[0] - main.OX, mouse[1] - main.OY)
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_chunk = mouse_get_chunk()

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not is_cursor_in_interact_range(mouse):
                continue
            clicked_pig = find_clicked_pig(mouse_world)
            if clicked_pig is not None:
                pig_died = clicked_pig.try_hit()
                if pig_died and clicked_pig in main.pig_entities:
                    main.pig_entities.remove(clicked_pig)
                dropped_item = Item()
                dropped_item.item_id = 35
                dropped_item.amount = 1
                dropped_item.x, dropped_item.y = clicked_pig._get_center()
                main.item_entities.append(dropped_item)
                continue

            clicked_cow = find_clicked_cow(mouse_world)
            if clicked_cow is not None:
                cow_died = clicked_cow.try_hit()
                if cow_died and clicked_cow in main.cow_entities:
                    main.cow_entities.remove(clicked_cow)
                    dropped_item = Item()
                    dropped_item.item_id = 35
                    dropped_item.amount = 1
                    dropped_item.x, dropped_item.y = clicked_cow._get_center()
                    main.item_entities.append(dropped_item)
                continue

            clicked_sheep = find_clicked_sheep(mouse_world)
            if clicked_sheep is None:
                continue

            sheep_died = clicked_sheep.try_hit()
            if sheep_died and clicked_sheep in main.sheep_entities:
                main.sheep_entities.remove(clicked_sheep)
                dropped_item = Item()
                dropped_item.item_id = 35
                dropped_item.amount = 1
                dropped_item.x, dropped_item.y = clicked_sheep._get_center()
                main.item_entities.append(dropped_item)

    if main.block_in_reach and not main.paused:
        x = int(((mouse[0] - main.OX) % 4096) // 64)
        y = int(((mouse[1] - main.OY) % 4096) // 64)
        main.selected_block = (x, y)

        if mouse_buttons[0] and main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Hardness"] > 0:
            current_block_id = main.loaded_chunks[mouse_chunk][0][x][y]
            break_mult = calc_break_speed_multiplier(current_block_id, main.hotbar_slot)
            main.break_progress += 100 / main.block_data[current_block_id]["Hardness"] * main.break_speed * break_mult
            if main.break_progress >= 100 and main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Minable"]:
                if main.gamemode == 0:
                    damage_tool_in_slot(main.hotbar_slot)
                if main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][0] != -1 and main.gamemode == 0:
                    if isinstance(main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][1], int):
                        amount = main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][1]
                    else:
                        amount = random.randint(main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][1][0], main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][1][1])
                    if isinstance(main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][0], int):
                        item_id = main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][0]
                    else:
                        item_id = random.choice(main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Drop"][0])

                    if amount > 0:
                        new_item = Item()
                        new_item.item_id = item_id
                        new_item.x = mouse[0] - main.OX
                        new_item.y = mouse[1] - main.OY
                        new_item.amount = amount
                        main.item_entities.append(new_item)
                if main.loaded_chunks[mouse_chunk][0][x][y] in [16, 17]:
                    coords = get_coordinates_from_chunk(mouse_chunk)
                    for chunk in main.container_savedata["Chunks"]:
                        if chunk["Coordinates"][0] == coords[0] and chunk["Coordinates"][1] == coords[1]:
                            for block in chunk["Blocks"]:
                                if block["Coordinates"][0] == x and block["Coordinates"][1] == y:
                                    chunk["Blocks"].remove(block)
                main.loaded_chunks[mouse_chunk][0][x][y] = int(0)
                render_blocks([[x, y]], mouse_chunk)
                main.break_progress = 0
        else:
            main.break_progress = 0

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Interactable"]:
                        block_interact(main.loaded_chunks[mouse_chunk][0][x][y], x, y, mouse_chunk)
                    elif main.block_data[main.loaded_chunks[mouse_chunk][0][x][y]]["Replacable"] and main.block_in_hand != 0:
                        main.loaded_chunks[mouse_chunk][0][x][y] = int(main.block_in_hand)
                        if main.gamemode == 0:
                            main.inventory[main.hotbar_slot][1] -= 1
                        render_blocks([[x, y]], mouse_chunk)
                        if int(main.block_in_hand) == 42:
                            main.growing_saplings.append([x, y, main.loaded_chunks[mouse_chunk][1], random.randint(5000, 8000)])
                main.break_progress = 0
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                main.break_progress = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_F3] and keys[pygame.K_a]:
                re_render_loaded_chunks()

    for i in range(len(main.inventory)):
        if main.inventory[i][1] <= 0:
            main.inventory[i][0] = 0
            main.inventory_durability[i] = 0
            if main.hotbar_slot == i and i < 8:
                main.block_in_hand = 0

    #Player chunk teleport
    if player.x > 0:
        #tp player / item
        main.OX = int(-4095 + main.surface.get_width() / 2)
        for item in main.item_entities:
            item.x += 4095
        for pig in main.pig_entities:
            pig.x += 4095
        for cow in main.cow_entities:
            cow.x += 4095
        for sheep in main.sheep_entities:
            sheep.x += 4095

        #add chunks to render queue
        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [0, 1, 6, 7]:
                    i[0] += 1
                elif i[0] in [2, 8]:
                    main.chunk_render_queue.pop(index)

        #save old chunks
        for i in [2, 5, 8]:
            main.chunk_buffer.append(copy.deepcopy(main.loaded_chunks[i]))

        #move chunks
        for column in [2, 1]:
            for row in [0, 3, 6]:
                main.loaded_chunks[column + row] = copy.deepcopy(main.loaded_chunks[column + row - 1])
                main.block_surface[column + row] = copy.copy(main.block_surface[column + row - 1])

        #load and or generate chunks
        for i in [0, 3, 6]:
            chunk_coords = [main.loaded_chunks[i + 1][1][0] - 1, main.loaded_chunks[i + 1][1][1]]
            found = None
            for index, data in enumerate(main.chunk_buffer):
                if data[1] == chunk_coords:
                    found = index
                    break
            if found is not None:
                main.loaded_chunks[i] = main.chunk_buffer[found]
                main.chunk_buffer.pop(found)

            else:
                main.loaded_chunks[i][1][0] = main.loaded_chunks[i + 1][1][0]-1
                generate_chunk_type(i, 0)
                for tree in main.tree_queue[i]:
                    generate_tree(tree[0], tree[1], i)
            try_spawn_pig_in_chunk(i)
            try_spawn_cow_in_chunk(i)
            try_spawn_sheep_in_chunk(i)
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    elif player.x < -4095:
        main.OX = int(main.surface.get_width() / 2)
        for item in main.item_entities:
            item.x -= 4095
        for pig in main.pig_entities:
            pig.x -= 4095
        for cow in main.cow_entities:
            cow.x -= 4095
        for sheep in main.sheep_entities:
            sheep.x -= 4095

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [2, 1, 8, 7]:
                    i[0] -= 1
                elif i[0] in [0, 6]:
                    main.chunk_render_queue.pop(index)

        for i in [0, 3, 6]:
            main.chunk_buffer.append(copy.deepcopy(main.loaded_chunks[i]))

        for column in [0, 1]:
            for row in [0, 3, 6]:
                main.loaded_chunks[column + row] = copy.deepcopy(main.loaded_chunks[column + row + 1])
                main.block_surface[column + row] = copy.copy(main.block_surface[column + row + 1])

        for i in [2, 5, 8]:
            chunk_coords = [main.loaded_chunks[i - 1][1][0] + 1, main.loaded_chunks[i - 1][1][1]]
            found = None
            for index, data in enumerate(main.chunk_buffer):
                if data[1] == chunk_coords:
                    found = index
                    break
            if found is not None:
                main.loaded_chunks[i] = main.chunk_buffer[found]
                main.chunk_buffer.pop(found)
            else:
                main.loaded_chunks[i][1][0] = main.loaded_chunks[i - 1][1][0] + 1
                generate_chunk_type(i, 0)
                for tree in main.tree_queue[i]:
                    generate_tree(tree[0], tree[1], i)
            try_spawn_pig_in_chunk(i)
            try_spawn_cow_in_chunk(i)
            try_spawn_sheep_in_chunk(i)
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    elif player.y > 0:
        main.OY = int(-4095 + main.surface.get_height() / 2)
        for item in main.item_entities:
            item.y += 4095
        for pig in main.pig_entities:
            pig.y += 4095
        for cow in main.cow_entities:
            cow.y += 4095
        for sheep in main.sheep_entities:
            sheep.y += 4095

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [2, 0, 3, 5]:
                    i[0] += 3
                elif i[0] in [8, 6]:
                    main.chunk_render_queue.pop(index)

        for i in [6, 7, 8]:
            main.chunk_buffer.append(copy.deepcopy(main.loaded_chunks[i]))

        for row in [2, 1]:
            for col in [0, 1, 2]:
                dst = row * 3 + col
                src = (row - 1) * 3 + col
                main.loaded_chunks[dst] = copy.deepcopy(main.loaded_chunks[src])
                main.block_surface[dst] = copy.copy(main.block_surface[src])

        for i in [0, 1, 2]:
            chunk_coords = [main.loaded_chunks[i + 3][1][0], main.loaded_chunks[i + 3][1][1] - 1]
            found = None
            for index, data in enumerate(main.chunk_buffer):
                if data[1] == chunk_coords:
                    found = index
                    break
            if found is not None:
                main.loaded_chunks[i] = main.chunk_buffer[found]
                main.chunk_buffer.pop(found)
            else:
                main.loaded_chunks[i][1][1] = main.loaded_chunks[i + 3][1][1] - 1
                generate_chunk_type(i, 0)
            try_spawn_pig_in_chunk(i)
            try_spawn_cow_in_chunk(i)
            try_spawn_sheep_in_chunk(i)
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    elif player.y < -4095:
        main.OY = int(main.surface.get_height() / 2)
        for item in main.item_entities:
            item.y -= 4095
        for pig in main.pig_entities:
            pig.y -= 4095
        for cow in main.cow_entities:
            cow.y -= 4095
        for sheep in main.sheep_entities:
            sheep.y -= 4095

        if len(main.chunk_render_queue) > 0:
            for index in reversed(range(len(main.chunk_render_queue))):
                i = main.chunk_render_queue[index]
                if i[0] in [8, 6, 3, 5]:
                    i[0] -= 3
                elif i[0] in [0, 2]:
                    main.chunk_render_queue.pop(index)

        for i in [0, 1, 2]:
            main.chunk_buffer.append(copy.deepcopy(main.loaded_chunks[i]))

        for row in [0, 1]:
            for col in [0, 1, 2]:
                dst = row * 3 + col
                src = (row + 1) * 3 + col
                main.loaded_chunks[dst] = copy.deepcopy(main.loaded_chunks[src])
                main.block_surface[dst] = copy.copy(main.block_surface[src])

        for i in [6, 7, 8]:
            chunk_coords = [main.loaded_chunks[i - 3][1][0], main.loaded_chunks[i - 3][1][1] + 1]
            found = None
            for index, data in enumerate(main.chunk_buffer):
                if data[1] == chunk_coords:
                    found = index
                    break
            if found is not None:
                main.loaded_chunks[i] = main.chunk_buffer[found]
                main.chunk_buffer.pop(found)
            else:
                main.loaded_chunks[i][1][1] = main.loaded_chunks[i - 3][1][1] + 1
                generate_chunk_type(i, 0)
            try_spawn_pig_in_chunk(i)
            try_spawn_cow_in_chunk(i)
            try_spawn_sheep_in_chunk(i)
            render_chunk_clear(i)
            chunk_add_render_queue(i)

    remove_unloaded_pigs()
    remove_unloaded_cows()
    remove_unloaded_sheep()
    for pig in main.pig_entities:
        pig.pig_default(active=not main.paused)
    for cow in main.cow_entities:
        cow.cow_default(active=not main.paused)
    for sheep in main.sheep_entities:
        sheep.sheep_default(active=not main.paused)

    player.player_default()
    for item in main.item_entities:
        item.item_default()
        if item.lifetime > 1800:
            main.item_entities.remove(item)

    if main.container_current != [] and main.container_open[0] == False:
        data_found = False
        chunk_found = False
        for chunk in main.container_savedata["Chunks"]:
            if chunk["Coordinates"][0] == main.container_coords[0][0] and chunk["Coordinates"][1] == main.container_coords[0][1]:
                chunk_found = True
                for block in chunk["Blocks"]:
                    if block["Coordinates"][0] == main.container_coords[1][0] and block["Coordinates"][1] == main.container_coords[1][1]:
                        data_found = True
                        block["Data"] = main.container_current
                        main.container_current = []
                        break
                if not data_found:
                    chunk["Blocks"].append({"Coordinates": main.container_coords[1], "Data": main.container_current})
                    main.container_current = []
                    break
        if not chunk_found:
            main.container_savedata["Chunks"].append({"Coordinates": main.container_coords[0], "Blocks": [{"Coordinates": main.container_coords[1], "Data": main.container_current}]})
            main.container_current = []

    for chunk in main.container_savedata["Chunks"]:
        for block in chunk["Blocks"]:
            if len(block["Data"]) == 7 and (block["Data"][1][0] != 0 or block["Data"][3] > 0):
                if block["Data"][3] == 0:
                    block["Data"][1][1] -=1

                if block["Data"][1][0] != 0:
                    fuel = block["Data"][1][0]
                else:
                    fuel = block["Data"][6]

                match fuel:
                    case 9 | 10 | 15 | 17:
                        block["Data"][3] += 2
                    case 22 | 34:
                        block["Data"][3] += 6
                    case 1005:
                        block["Data"][3] += 1
                    case 28:
                        block["Data"][3] += 0.1

                if block["Data"][3] >= 1000:
                    block["Data"][3] = 0
                if block["Data"][0][0] != 0:
                    for recipe in main.recipe_data:
                        if recipe[0] == block["Data"][0][0]:
                            block["Data"][4] += 1
                            if block["Data"][4] >= 100:
                                block["Data"][2][0] = recipe[1]
                                block["Data"][2][1] += 1
                                block["Data"][0][1] -= 1
                                block["Data"][4] = 0


    for sapling in main.growing_saplings:
        if sapling[3] > 0:
            sapling[3] -= 1

        if sapling[2] == main.loaded_chunks[4][1] and sapling[3] <= 0:
            if main.loaded_chunks[4][0][sapling[0]][sapling[1]] == 42:
                generate_tree(sapling[0], sapling[1], 4)
            main.growing_saplings.remove(sapling)

    main.daylight_time += 1
    sky_result = current_skycolor(main.daylight_time, main.daytime_values[2], main.daytime_values[0], main.daytime_values[1])
    main.daylight_time = sky_result[0]
    main.sky_color = sky_result[1]

    if main.mods_active:
        for mod in main.loaded_mods:
            with zipfile.ZipFile(f"{main.MODPATH}/{mod}", 'r') as zip_ref:
                if "scripts/game_loop.py" in zip_ref.namelist():
                    with zip_ref.open("scripts/game_loop.py") as file:
                        exec(file.read())

    if len(main.chunk_render_queue) > 2:
        while main.chunk_render_queue[0] in main.chunk_render_queue[1:]:
            main.chunk_render_queue.pop(0)
    if len(main.chunk_render_queue) > 0:
        main.chunk_render_queue = render_chunk(main.chunk_render_queue, 15)
        if len(main.chunk_render_queue) > 9:
            main.chunk_render_queue.pop(0)


    ui(events, main.surface, main.SCALE)
    if main.img_save_timeout > 0:
        match main.img_save_timeout:
            case 2:
                save_world_icon()
            case 3:
                main.current_scene = 0
            case 6:
                save_world_icon()
        main.img_save_timeout += 1
        if main.img_save_timeout >= 7:
            main.img_save_timeout = 0
