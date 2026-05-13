import pygame
import __main__ as main

from game.utils.item_ids import load_items
from game.utils.recipes import load_recipes


WINDOW_W = 980
WINDOW_H = 680
BG_COLOR = (24, 24, 28)
PANEL_COLOR = (42, 42, 50)
SLOT_COLOR = (80, 80, 90)
SLOT_BORDER = (165, 165, 180)
TEXT_COLOR = (235, 235, 235)
MUTED_TEXT = (170, 170, 180)
ACCENT = (90, 160, 255)


def split_recipes(recipe_data):
    workbench = []
    furnace = []

    for recipe in recipe_data:
        if len(recipe) == 3 and isinstance(recipe[0], list) and len(recipe[0]) == 9:
            if recipe[1] != 0:
                workbench.append(
                    {
                        "type": "workbench",
                        "grid": recipe[0],
                        "out_id": recipe[1],
                        "out_count": recipe[2],
                    }
                )
        elif len(recipe) == 2 and isinstance(recipe[0], int):
            furnace.append(
                {
                    "type": "furnace",
                    "in_id": recipe[0],
                    "out_id": recipe[1],
                    "out_count": 1,
                }
            )
    return workbench + furnace


def draw_slot(screen, x, y, size, item_id, item_data):
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, SLOT_COLOR, rect, border_radius=8)
    pygame.draw.rect(screen, SLOT_BORDER, rect, width=2, border_radius=8)

    if item_id != 0 and item_id in item_data:
        tex = item_data[item_id]["Texture"]
        tx, ty = tex.get_size()
        screen.blit(tex, (x + (size - tx) // 2, y + (size - ty) // 2))


def draw_item_label(screen, font, x, y, item_id, item_data, prefix):
    if item_id in item_data:
        name = item_data[item_id]["Name"]
    else:
        name = "Unknown"
    text = font.render(f"{prefix}{name} (ID: {item_id})", True, MUTED_TEXT)
    screen.blit(text, (x, y))


def draw_workbench_layout(screen, fonts, recipe, item_data):
    title_font, body_font = fonts
    slot_size = 74
    start_x = 170
    start_y = 180

    title = title_font.render("Crafting Table Recipe", True, TEXT_COLOR)
    screen.blit(title, (80, 85))

    for row in range(3):
        for col in range(3):
            idx = row * 3 + col
            draw_slot(
                screen,
                start_x + col * (slot_size + 10),
                start_y + row * (slot_size + 10),
                slot_size,
                recipe["grid"][idx],
                item_data,
            )

    arrow = title_font.render("->", True, ACCENT)
    screen.blit(arrow, (470, 270))

    out_x = 580
    out_y = 260
    draw_slot(screen, out_x, out_y, slot_size, recipe["out_id"], item_data)
    out_text = body_font.render(f"x{recipe['out_count']}", True, TEXT_COLOR)
    screen.blit(out_text, (out_x + 80, out_y + 52))

    draw_item_label(screen, body_font, 80, 510, recipe["out_id"], item_data, "Result: ")


def draw_furnace_layout(screen, fonts, recipe, item_data):
    title_font, body_font = fonts
    slot_size = 74
    center_x = 490

    title = title_font.render("Furnace Recipe", True, TEXT_COLOR)
    screen.blit(title, (80, 85))

    in_x = center_x - 230
    in_y = 220
    fuel_x = in_x
    fuel_y = in_y + 130
    out_x = center_x + 140
    out_y = in_y + 65

    draw_slot(screen, in_x, in_y, slot_size, recipe["in_id"], item_data)
    draw_slot(screen, fuel_x, fuel_y, slot_size, 1005, item_data)
    draw_slot(screen, out_x, out_y, slot_size, recipe["out_id"], item_data)

    fire_text = body_font.render("Fuel", True, MUTED_TEXT)
    screen.blit(fire_text, (fuel_x + 14, fuel_y + 84))

    arrow = title_font.render("=>", True, ACCENT)
    screen.blit(arrow, (center_x + 20, in_y + 80))

    out_text = body_font.render(f"x{recipe['out_count']}", True, TEXT_COLOR)
    screen.blit(out_text, (out_x + 80, out_y + 52))

    draw_item_label(screen, body_font, 80, 500, recipe["in_id"], item_data, "Input: ")
    draw_item_label(screen, body_font, 80, 535, recipe["out_id"], item_data, "Result: ")


def main_viewer():
    pygame.init()
    pygame.display.set_caption("MicroCraft Recipe Viewer")
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    # load_items expects main.img_empty to exist on __main__
    main.img_empty = pygame.Surface((48, 48), pygame.SRCALPHA)
    item_data = load_items()
    recipes = split_recipes(load_recipes())

    if not recipes:
        raise RuntimeError("No recipes found.")

    title_font = pygame.font.SysFont("consolas", 34, bold=True)
    body_font = pygame.font.SysFont("consolas", 24)
    small_font = pygame.font.SysFont("consolas", 20)

    prev_btn = pygame.Rect(80, 610, 140, 44)
    next_btn = pygame.Rect(WINDOW_W - 220, 610, 140, 44)

    index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    index = (index + 1) % len(recipes)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    index = (index - 1) % len(recipes)
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if prev_btn.collidepoint(event.pos):
                    index = (index - 1) % len(recipes)
                elif next_btn.collidepoint(event.pos):
                    index = (index + 1) % len(recipes)

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PANEL_COLOR, (40, 40, WINDOW_W - 80, WINDOW_H - 120), border_radius=18)

        recipe = recipes[index]
        if recipe["type"] == "workbench":
            draw_workbench_layout(screen, (title_font, body_font), recipe, item_data)
        else:
            draw_furnace_layout(screen, (title_font, body_font), recipe, item_data)

        info = small_font.render(
            f"Recipe {index + 1}/{len(recipes)}  |  Type: {recipe['type']}", True, TEXT_COLOR
        )
        screen.blit(info, (80, 52))

        hint = small_font.render("Use <- / -> or click buttons", True, MUTED_TEXT)
        screen.blit(hint, (WINDOW_W // 2 - hint.get_width() // 2, 618))

        pygame.draw.rect(screen, SLOT_COLOR, prev_btn, border_radius=10)
        pygame.draw.rect(screen, SLOT_BORDER, prev_btn, width=2, border_radius=10)
        pygame.draw.rect(screen, SLOT_COLOR, next_btn, border_radius=10)
        pygame.draw.rect(screen, SLOT_BORDER, next_btn, width=2, border_radius=10)

        prev_txt = body_font.render("Prev", True, TEXT_COLOR)
        next_txt = body_font.render("Next", True, TEXT_COLOR)
        screen.blit(prev_txt, (prev_btn.x + 42, prev_btn.y + 8))
        screen.blit(next_txt, (next_btn.x + 42, next_btn.y + 8))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main_viewer()
