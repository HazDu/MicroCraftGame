import random
import math
import __main__ as main

from game.utils.util_functs import *

def generate_chunk_type(chunk, worldtype):
    match worldtype:
        case 0:
            generate_chunk_2d_flat(chunk)
        case 1:
            generate_chunk_2d_hill(chunk)
        case 2:
            generate_chunk_random(chunk)
        case _:
            generate_chunk(chunk)

def generate_tree(x, y, chunk):
    # Ensure trees only generate when the trunk base is directly above grass.
    ground_x = x
    ground_y = y + 1
    ground_checked = change_block_over_border(chunk, ground_x, ground_y)
    ground_chunk = ground_checked[0]
    ground_x = ground_checked[1]
    ground_y = ground_checked[2]
    if ground_chunk == -1:
        return
    if main.loaded_chunks[ground_chunk][0][ground_x][ground_y] != 2:
        return

    blocks = [
        [[-1, -4], 11], [[0, -4], 11], [[1, -4], 11],
        [[-2, -3], 11], [[-1, -3], 11], [[0, -3], 10], [[1, -3], 11], [[2, -3], 11],
        [[-2, -2], 11], [[-1, -2], 11], [[0, -2], 10], [[1, -2], 11], [[2, -2], 11],
        [[0, -1], 10],
        [[0, 0], 10],
    ]
    for block in blocks:
        _x = x + block[0][0]
        _y = y + block[0][1]

        chunk_checked = change_block_over_border(chunk, _x, _y)
        _x = chunk_checked[1]
        _y = chunk_checked[2]
        chunk_checked = chunk_checked[0]

        if chunk_checked != -1:
            if main.block_data[main.loaded_chunks[chunk_checked][0][_x][_y]]["Replacable"]:
                main.loaded_chunks[chunk_checked][0][_x][_y] = block[1]
                render_blocks([[_x, _y]], chunk_checked)

def create_chunk():
    return [[0 for _ in range(64)] for _ in range(64)]

def generate_chunk(chunk):
    main.loaded_chunks[chunk][0] = [[4 for _ in range(64)] for _ in range(64)]

def generate_chunk_random(chunk):
    main.loaded_chunks[chunk][0] = [[(random.randint(1, main.block_count-1)) for _ in range(64)] for _ in range(64)]

def _seed_to_int(seed_value):
    text = str(seed_value)
    if text == "":
        text = "default"
    h = 2166136261
    for ch in text:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h

def _mix32(value):
    n = value & 0xFFFFFFFF
    n ^= (n >> 16)
    n = (n * 0x7FEB352D) & 0xFFFFFFFF
    n ^= (n >> 15)
    n = (n * 0x846CA68B) & 0xFFFFFFFF
    n ^= (n >> 16)
    return n

def _rand01_at(index):
    seed_int = _seed_to_int(getattr(main, "world_seed", ""))
    mixed = _mix32(index + seed_int)
    return mixed / 4294967295.0

def _value_noise_1d(world_x, period, salt):
    fx = world_x / period
    ix = math.floor(fx)
    t = fx - ix
    # Smooth interpolation keeps slopes continuous between sample points.
    t = t * t * (3 - (2 * t))
    a = _rand01_at((ix * 7349) + salt)
    b = _rand01_at(((ix + 1) * 7349) + salt)
    return (a * (1 - t)) + (b * t)

def _surface_height_from_world_x(world_x):
    # Seeded value-noise octaves for varied but seamless terrain per world seed.
    n1 = _value_noise_1d(world_x, 64.0, 101)
    n2 = _value_noise_1d(world_x, 28.0, 211)
    n3 = _value_noise_1d(world_x, 14.0, 307)
    height = 32 + ((n1 - 0.5) * 18.0) + ((n2 - 0.5) * 11.0) + ((n3 - 0.5) * 5.0)
    return max(16, min(50, int(round(height))))

def _should_place_tree(world_x):
    # Seeded sparse placement based on world x.
    return _rand01_at((world_x * 9151) + 733) < (1 / 19)

def _sand_depth_at_world_x(world_x):
    # Build deterministic, seam-safe half-oval sand patches in world space.
    # Returned depth includes the surface block and extends downward only.
    max_depth = 0
    band_size = 72
    band = math.floor(world_x / band_size)
    for candidate_band in range(band - 1, band + 2):
        chance_roll = _rand01_at((candidate_band * 3253) + 401)
        if chance_roll >= 0.46:
            continue

        center_roll = _rand01_at((candidate_band * 3253) + 402)
        radius_roll = _rand01_at((candidate_band * 3253) + 403)
        depth_roll = _rand01_at((candidate_band * 3253) + 404)
        center_x = (candidate_band * band_size) + int(center_roll * band_size)
        radius = 10 + int(radius_roll * 18)  # 10..27
        depth_max = 3 + int(depth_roll * 7)  # 3..9
        dx = abs(world_x - center_x)
        if dx > radius:
            continue

        # Half-ellipse profile: full curve would continue upward; we only keep
        # the downward half by applying this as replacement depth into terrain.
        profile = math.sqrt(1 - ((dx / radius) ** 2))
        depth = int(round(depth_max * profile))
        if depth > max_depth:
            max_depth = depth
    return max_depth

def generate_chunk_2d_flat(chunk):
    if main.loaded_chunks[chunk][1][1] == 0:
        contents = []
        chunk_world_x = main.loaded_chunks[chunk][1][0]
        for x in range(64):
            row = []
            for y in range(64):
                if y == 32:
                    row.append(2)
                elif 58 > y > 32:
                    row.append(1)
                elif y >= 58:
                    row.append(random.choice([1, 4]))
                elif y < 32:
                    row.append(0)
            contents.append(row)

        for x in range(64):
            world_x = (chunk_world_x * 64) + x
            surface_y = 32
            sand_depth = _sand_depth_at_world_x(world_x)
            if sand_depth > 0:
                for depth in range(sand_depth):
                    y = surface_y + depth
                    if 0 <= y < 64 and contents[x][y] in (1, 2):
                        contents[x][y] = 8

            if contents[x][surface_y] == 2 and random.randint(0, 16) == 0:
                main.tree_queue[chunk].append([x, surface_y - 1])
        main.loaded_chunks[chunk][0] = contents
    elif 3 > main.loaded_chunks[chunk][1][1] >= 1:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if y < 58 or main.loaded_chunks[chunk][1][1] == 1:
                    if random.randint(0, 100) <= 5:
                        row.append(random.randint(29, 33))
                    else:
                        row.append(4)
                else:
                    row.append(random.choice([4, 36]))
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents
    elif main.loaded_chunks[chunk][1][1] >= 3:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if random.randint(0, 100) <= 10:
                    row.append(random.randint(37, 40))
                else:
                    row.append(36)
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents

def generate_chunk_2d_hill(chunk):
    if main.loaded_chunks[chunk][1][1] == 0:
        contents = []
        chunk_world_x = main.loaded_chunks[chunk][1][0]
        surface_heights = []
        for x in range(64):
            row = []
            world_x = (chunk_world_x * 64) + x
            surface_y = _surface_height_from_world_x(world_x)
            surface_heights.append(surface_y)
            for y in range(64):
                if y == surface_y:
                    row.append(2)
                elif 58 > y > surface_y:
                    row.append(1)
                elif y >= 58:
                    row.append(random.choice([1, 4]))
                elif y < surface_y:
                    row.append(0)
            contents.append(row)

        for x in range(64):
            world_x = (chunk_world_x * 64) + x
            surface_y = surface_heights[x]
            sand_depth = _sand_depth_at_world_x(world_x)
            if sand_depth > 0:
                for depth in range(sand_depth):
                    y = surface_y + depth
                    if 0 <= y < 64 and contents[x][y] in (1, 2):
                        contents[x][y] = 8

            if contents[x][surface_y] == 2 and _should_place_tree(world_x):
                main.tree_queue[chunk].append([x, surface_y - 1])
        main.loaded_chunks[chunk][0] = contents
    elif 3 > main.loaded_chunks[chunk][1][1] >= 1:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if y < 58 or main.loaded_chunks[chunk][1][1] == 1:
                    if random.randint(0, 100) <= 5:
                        row.append(random.randint(29, 33))
                    else:
                        row.append(4)
                else:
                    row.append(random.choice([4, 36]))
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents
    elif main.loaded_chunks[chunk][1][1] >= 3:
        contents = []
        for x in range(64):
            row = []
            for y in range(64):
                if random.randint(0, 100) <= 10:
                    row.append(random.randint(37, 40))
                else:
                    row.append(36)
            contents.append(row)
        main.loaded_chunks[chunk][0] = contents
