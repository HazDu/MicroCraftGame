import pygame
import numpy as np
import math
import os
import json
import zipfile
import __main__ as main

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def point_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.hypot(x2 - x1, y2 - y1)

def move_towarts(pos_goal, pos_at, distance):
    goal_vec = pygame.math.Vector2(pos_goal)
    at_vec = pygame.math.Vector2(pos_at)


    direction = goal_vec - at_vec
    length = direction.length()

    if length == 0:
        return at_vec.x, at_vec.y
    if distance >= length:
        return goal_vec.x, goal_vec.y

    direction = direction.normalize()
    new_pos = at_vec + direction * distance

    return new_pos.x, new_pos.y

def tint_image(surface, tint_color):
    intensity = tint_color[3] / 255.0

    tinted = surface.copy()

    rgb_array = pygame.surfarray.pixels3d(tinted)
    alpha_array = pygame.surfarray.pixels_alpha(tinted)

    tint_rgb = np.array(tint_color[:3], dtype=np.uint8)

    mask = alpha_array > 0

    for c in range(3):
        original = rgb_array[:, :, c]
        blended = (original * (1 - intensity) + tint_rgb[c] * intensity).astype(np.uint8)
        original[mask] = blended[mask]

    return tinted

def image_is_transparent(surface):
    alpha_array = pygame.surfarray.pixels_alpha(surface)
    return (alpha_array < 255).any()

def lerp_color(c1, c2, factor):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3))

def current_skycolor(time, trans_length, day_length, night_length):
    schedule_length = day_length + night_length + trans_length*2
    if time > schedule_length:
        time = 0

    if time <= day_length:
        return [time, main.sky_colors[0]]
    elif day_length < time <= day_length + trans_length/2:
        factor = (time - day_length) / ((day_length + trans_length/2) - day_length)
        col = lerp_color(main.sky_colors[0], main.sky_colors[2], factor)
        return [time, col]
    elif day_length + trans_length/2 < time <= day_length + trans_length:
        factor = (time - (day_length + trans_length/2)) / ((day_length + trans_length) - (day_length + trans_length/2))
        col = lerp_color(main.sky_colors[2], main.sky_colors[1], factor)
        return [time, col]
    elif day_length + trans_length < time <= day_length + trans_length + night_length:
        return [time, main.sky_colors[1]]
    elif day_length + trans_length + night_length < time <= day_length + trans_length + night_length + trans_length/2:
        factor = (time - (day_length + trans_length + night_length)) / ((day_length + trans_length + night_length + trans_length/2) - (day_length + trans_length + night_length))
        col = lerp_color(main.sky_colors[1], main.sky_colors[2], factor)
        return [time, col]
    else:
        factor = (time - (day_length + trans_length + night_length + trans_length/2)) / ((day_length + trans_length*2 + night_length) - (day_length + trans_length + night_length + trans_length/2))
        col = lerp_color(main.sky_colors[2], main.sky_colors[0], factor)
        return [time, col]

def button(x, y, width, height, sprite, tint_col, text, surface, events, x_align, y_align):
    btn_pressed = False
    mouse_pos = pygame.mouse.get_pos()

    #Set minimal width / height if a text is given
    if text != 0:
        text = str(text)
        font = pygame.font.SysFont('impact', 30)
        text = font.render(text, True, (255, 255, 255))
        width = max(width, text.get_width() + 10)
        height = max(height, text.get_height())

    sprite = pygame.transform.scale(sprite, (width, height))

    #set alignment
    match x_align: # L (left), M (middle), R (right)
        case "M": x -= width / 2
        case "R": x -= width
    match y_align: # T (top), M (middle), B (bottom)
        case "M": y -= height / 2
        case "B": y -= height

    #draw Button and check for Clicks
    if x <= mouse_pos[0] <= x+width and y <= mouse_pos[1] <= y+height:
        main.cur = main.cur_pointer
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_pressed = True
        tinted_image = tint_image(sprite, tint_col)
        surface.blit(tinted_image, (x, y))
    else:
        surface.blit(sprite, (x, y))

    #draw Text if Text is given
    if text != 0:
        text_x_align = x - (text.get_width() / 2)
        text_y_align = y - (text.get_height() / 2)
        surface.blit(text, (text_x_align + (width / 2), text_y_align + (height / 2)))

    #Return if the Button is pressed
    return btn_pressed

def button_exact(x, y, width, height, sprite, tint_col, text, surface, events, x_align, y_align):
    if button(x, y, width, height, sprite, tint_col, text, surface, events, x_align, y_align):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return "left"
                elif event.button == 3:
                    return "right"
    return 0


def background_fill_texture(sprite, scale, surface):
    import math
    x = 0
    y = 0
    spr_w = sprite.get_width()
    spr_h = sprite.get_height()
    sprite = pygame.transform.scale(sprite, (spr_w * scale, spr_h * scale))

    for _ in range(math.ceil(surface.get_height() / (spr_h * scale))):
        for _ in range(math.ceil(surface.get_width() / (spr_w * scale))):
            surface.blit(sprite, (x, y))
            x += spr_w * scale
        y += spr_h * scale
        x = 0

def text_render_multiline(x, y, font, text, antialiasing, color, surface, x_align, y_align):
    lines = text.split("\n")

    for line in lines:
        render_line = font.render(line, antialiasing, color)

        # set alignment
        match x_align:  # L (left), M (middle), R (right)
            case "M": xa = x - render_line.get_width() / 2
            case "R": xa = x - render_line.get_width()
            case _: xa = x
        match y_align:  # T (top), M (middle), B (bottom)
            case "M": ya = y - render_line.get_height() / 2
            case "B": ya = y - render_line.get_height()
            case _: ya = y

        surface.blit(render_line, (xa, ya))
        y += render_line.get_height()

def render_blocks(changed_blocks, chunk):
    if changed_blocks == 0:
        main.block_surface[chunk].fill((0, 0, 0, 0))
        for y in range(64):
            for x in range(64):
                coords = [(x * 64), (y * 64)]
                sprite = main.block_data[main.loaded_chunks[chunk][0][x][y]]["Texture"]
                main.block_surface[chunk].blit(sprite, (coords[0], coords[1]))
    else:
        for block in changed_blocks:
            coords = [(block[0] * 64), (block[1] * 64)]
            sprite = main.block_data[main.loaded_chunks[chunk][0][block[0]][block[1]]]["Texture"]
            if image_is_transparent(sprite):
                clear = pygame.Surface((64, 64), pygame.SRCALPHA)
                clear.fill((0, 0, 0, 0))
                main.block_surface[chunk].blit(clear, (coords[0], coords[1]), special_flags=pygame.BLEND_RGBA_MULT)
            main.block_surface[chunk].blit(sprite, (coords[0], coords[1]))

def render_chunk_clear(chunk):
    main.block_surface[chunk].fill((0, 0, 0, 0))

def chunk_add_render_queue(chunk):
    coords = [[x, y] for x in range(64) for y in range(64)]
    main.chunk_render_queue.append([chunk, coords])

def render_chunk(queue, render_speed): #queue = [[chunk, [[0, 0],[0, 1]]], [chunk, [[0, 0],[0, 1]]]]
        size = clamp(render_speed, 1, 4096)
        chunk = queue[0][0]
        blocks = queue[0][1][:size]
        queue[0][1] = queue[0][1][size:]

        render_blocks(blocks, chunk)

        if queue[0][1] == []:
            queue.pop(0)

        return queue

def re_render_loaded_chunks():
    for i in [4, 3, 5, 1, 7, 0, 2, 6, 8]:
        render_chunk_clear(i)
        chunk_add_render_queue(i)

def mouse_get_chunk():
    mouse = pygame.mouse.get_pos()
    x = mouse[0] - main.OX
    y = mouse[1] - main.OY
    chunk = 4
    if x < 0:
        if y < 0:
            chunk = 0
        elif y > 4096:
            chunk = 6
        else:
            chunk = 3

    elif x > 4096:
        if y < 0:
            chunk = 2
        elif y > 4096:
            chunk = 8
        else:
            chunk = 5
    else:
        if y < 0:
            chunk = 1
        elif y > 4096:
            chunk = 7

    return int(chunk)

def save_world():
    path = os.path.join(main.GAMEPATH, "saves", main.world_name, "chunkdata")
    for chunk in main.loaded_chunks:
        with open(f"{path}/{chunk[1]}.chunk", "w") as file:
            file.write(str(chunk[0]))
    for chunk in main.chunk_buffer:
        with open(f"{path}/{chunk[1]}.chunk", "w") as file:
            file.write(str(chunk[0]))

    path = os.path.join(main.GAMEPATH, "saves", main.world_name)
    with open(f"{path}/infos.json", "r") as file:
        read_data = json.load(file)
    read_data["PlayerX"] = main.OX
    read_data["PlayerY"] = main.OY
    read_data["CurrentChunk"] = main.loaded_chunks[4][1]
    read_data["Inventory"] = main.inventory
    read_data["Gamemode"] = main.gamemode
    read_data["Saplings"] = main.growing_saplings
    read_data["DayTime"] = main.daylight_time
    read_data["ContainerData"] = main.container_savedata
    with open(f"{path}/infos.json", "w") as file:
        json.dump(read_data, file, indent=2)

def texturepack_load(path):
    blocks_path = f"{path}/assets/minecraft/textures/block"
    for i in range(1, len(main.block_data)):
        if os.path.exists(f"{blocks_path}/{main.block_data[i]["filename"]}.png"):
            main.block_data[i]["Texture"] = pygame.image.load(f"{blocks_path}/{main.block_data[i]["filename"]}.png").convert_alpha()
            width, height = main.block_data[i]["Texture"].get_size()
            if height > width:
                cropped = pygame.Surface((width, width), pygame.SRCALPHA)
                cropped.blit(main.block_data[i]["Texture"], (0,0))
                main.block_data[i]["Texture"] = cropped
            if i == 11:
                main.block_data[i]["Texture"] = tint_image(main.block_data[i]["Texture"], (34, 118, 0, 200))
            elif i == 2 or i == 13:
                main.block_data[i]["Texture"] = tint_image(main.block_data[i]["Texture"], (34, 117, 0, 130))

            main.block_data[i]["Texture"] = pygame.transform.scale(main.block_data[i]["Texture"], (64, 64))

    with open(f"{main.GAMEPATH}/settings.json", "r") as file:
        read_data = json.load(file)
    read_data["CurrentTexturepack"] = path
    with open(f"{main.GAMEPATH}/settings.json", "w") as file:
        json.dump(read_data, file, indent=2)

def save_world_icon():
    sv_img = pygame.Surface((128, 128))
    scr = pygame.transform.scale(main.surface, (240, 128))
    sv_img.blit(scr, (-56, 0))
    pygame.image.save(sv_img, f"{main.GAMEPATH}/saves/{main.world_name}/icon.png")

def get_chunk_from_coordinates(x, y):
    #DEPRICATED
    chunk = -1

    if x < 0:
        if y < 0:
            chunk = 0
        elif y > 0:
            chunk = 6
        elif y == 0:
            chunk = 3
    elif x > 0:
        if y < 0:
            chunk = 2
        elif y > 0:
            chunk = 8
        elif y == 0:
            chunk = 5
    elif x == 0:
        if y < 0:
            chunk = 1
        elif y > 0:
            chunk = 7
        elif y == 0:
            chunk = 4

    return chunk

def get_coordinates_from_chunk(chunk):
    coords = main.loaded_chunks[4][1]

    match chunk:
        case 0:
            coords = [main.loaded_chunks[4][1][0] -1, main.loaded_chunks[4][1][1] -1]
        case 1:
            coords = [main.loaded_chunks[4][1][0], main.loaded_chunks[4][1][1] -1]
        case 2:
            coords = [main.loaded_chunks[4][1][0] +1, main.loaded_chunks[4][1][1] -1]
        case 3:
            coords = [main.loaded_chunks[4][1][0] -1, main.loaded_chunks[4][1][1]]
        case 5:
            coords = [main.loaded_chunks[4][1][0] +1, main.loaded_chunks[4][1][1]]
        case 6:
            coords = [main.loaded_chunks[4][1][0] -1, main.loaded_chunks[4][1][1] +1]
        case 7:
            coords = [main.loaded_chunks[4][1][0], main.loaded_chunks[4][1][1] +1]
        case 8:
            coords = [main.loaded_chunks[4][1][0] +1, main.loaded_chunks[4][1][1] +1]

    return coords



def change_block_over_border(chunk, _x, _y):
    chunk_checked = chunk
    if _x < 0:
        _x = 64 + _x
        if _y < 0:
            _y = 64 + _y
            chunk_checked = chunk - 4
        elif _y > 63:
            _y = _y - 64
            chunk_checked = chunk + 2
        else:
            chunk_checked = chunk - 1
    elif _x > 63:
        _x = _x - 64
        if _y < 0:
            _y = 64 + _y
            chunk_checked = chunk - 2
        elif _y > 63:
            _y = _y - 64
            chunk_checked = chunk + 4
        else:
            chunk_checked = chunk + 1
    else:
        if _y < 0:
            _y = 64 + _y
            chunk_checked = chunk - 3
        elif _y > 63:
            _y = _y - 64
            chunk_checked = chunk + 3

    return [chunk_checked, _x, _y]

def world_coords_to_screen_coords(wx, wy):
    screen_curr_x = main.OX*-1
    screen_curr_y = main.OY*-1

    sx, sy = wx - screen_curr_x, wy - screen_curr_y

    return [sx, sy]

#functions for modders
def mod_init_trigger(mod):
    main.mod_reinit = [True, mod]