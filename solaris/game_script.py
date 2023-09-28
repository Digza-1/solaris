# game script contains game code

import pygame as pyg
import mysql.connector
import solaris.ground_generation as gnd
import random


pyg.init()  # initiates pygame
pyg.display.set_caption("solaris")

WINDOW_SIZE = (1400, 750)

screen = pyg.display.set_mode(WINDOW_SIZE)
display = pyg.Surface((300, 200), 0, 32)# used as the low scaled surface for rendering 
surface0 = pyg.Surface(WINDOW_SIZE, pyg.SRCALPHA)

moving_right = False
moving_left = False
moving_up = False
moving_down = False
player_health = 100
pause = False

speed = 0.1
scroll = [0, 0]
dev_m = False  # --------------------
cliping = True
CHUNK_SIZE = 8
TILE_SIZE = 16
objective_pos = None

SKY_COLOUR = (10, 10, 10)  # (146, 244, 255)
SKY_COLOUR1 = (59, 135, 164)

BG_COLOUR = (14, 14, 15)  # (26, 135, 122)  # (19, 127, 115)  # old(15, 76, 73)
BG_COLOUR2 = (26, 135, 122)

game_map = {}

astroid_grey_img = pyg.image.load("solaris/assets/rock.png").convert()
astroid_grey_img.set_colorkey((0, 0, 0))

astroid_grey2_img = pyg.image.load("solaris/assets/rock2.png").convert()
astroid_grey2_img.set_colorkey((0, 0, 0))

astroid_red_img = pyg.image.load("solaris/assets/rock3.png").convert()
astroid_red_img.set_colorkey((0, 0, 0))

astroid_red2_img = pyg.image.load("solaris/assets/rock5.png").convert()
astroid_red2_img.set_colorkey((0, 0, 0))

astroid_blue_img = pyg.image.load("solaris/assets/rock6.png").convert()
astroid_blue_img.set_colorkey((0, 0, 0))


player_img1 = pyg.image.load("solaris/assets/player.png").convert()
player_img1.set_colorkey((0, 0, 0))

player_img2 = pyg.image.load("solaris/assets/player.png").convert()
player_img2.set_colorkey((0, 0, 0))

player_img3 = pyg.image.load("solaris/assets/player.png").convert()
player_img3.set_colorkey((0, 0, 0))

tile_index = {
    1: astroid_grey_img,
    4: astroid_grey2_img,
    2: astroid_red2_img,
    3: astroid_red_img,
    5: astroid_blue_img,
}

player_costume_index = {1: player_img1, 2: player_img2, 3: player_img3}

player_flipx = False
player_flipy = False

player_rect = pyg.Rect(100, 100, 13, 13)


clock = pyg.time.Clock()
time_deltatime = clock.tick(30)

sqlPass = "CH3-CH2-CH2-CH3"

world_id = 0
player_id = 0


def get_settings_sql():
    mydb = mysql.connector.connect(
        ost="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    cursor = mydb.cursor()

    q = f"""select (seed,speed,grey_thershold,red_thershold,blue_thershold,difficulty,
    costume) from project_solaris where world_id = {world_id} and player_id = {player_id} ;"""

    cursor.execute(q)
    res = cursor.fetchone()


def draw_space(tile_rects):
    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            # get
            chunk_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * TILE_SIZE)))
            chunk_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * TILE_SIZE)))

            world_x = x + scroll[0]
            world_y = y + scroll[1]

            target_chunk = str(chunk_x) + "," + str(chunk_y)

            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_space(
                    chunk_x, chunk_y, CHUNK_SIZE
                )

            for tile in game_map[target_chunk]:
                if len(tile) > 0:
                    display.blit(
                        tile_index[tile[1]],
                        (
                            tile[0][0] * TILE_SIZE - scroll[0],
                            tile[0][1] * TILE_SIZE - scroll[1],
                        ),
                    )

                if tile[1] in [1, 2, 3]:
                    tile_rects.append(
                        pyg.Rect(
                            tile[0][0] * TILE_SIZE,
                            tile[0][1] * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE,
                        )
                    )


def draw_bg():
    pyg.draw.rect(display, BG_COLOUR, pyg.Rect(0, 120, 300, 80))


def draw_pause():
    pyg.draw.rect(surface0, (128, 128, 128, 80), [0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]])

    pyg.draw.rect(
        surface0,
        (255, 169, 78, 170),
        [
            WINDOW_SIZE[0] // 4 - 11,
            WINDOW_SIZE[1] // 4 - 11,
            WINDOW_SIZE[0] // 2 + 22,
            WINDOW_SIZE[1] // 2 + 22,
        ],
    )
    pyg.draw.rect(
        surface0,
        (0, 0, 0, 180),
        [
            WINDOW_SIZE[0] // 4 - 8,
            WINDOW_SIZE[1] // 4 - 8,
            WINDOW_SIZE[0] // 2 + 16,
            WINDOW_SIZE[1] // 2 + 16,
        ],
    )
    pyg.draw.rect(
        surface0,
        (255, 169, 78, 170),
        [
            WINDOW_SIZE[0] // 4 - 4,
            WINDOW_SIZE[1] // 4 - 4,
            WINDOW_SIZE[0] // 2 + 8,
            WINDOW_SIZE[1] // 2 + 8,
        ],
    )
    pyg.draw.rect(
        surface0,
        (0, 0, 0, 180),
        [
            WINDOW_SIZE[0] // 4,
            WINDOW_SIZE[1] // 4,
            WINDOW_SIZE[0] // 2,
            WINDOW_SIZE[1] // 2,
        ],
    )

    screen.blit(surface0, (0, 0))


def add_text(text1, x, y, size):
    font = pyg.font.Font("freesansbold.ttf", size)
    text = font.render(text1, True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)
    display.blit(text, textRect)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list

def objective_reached():
    px_reached = round(round(player_rect.x) // objective_pos[0])
    py_reached = round(round(player_rect.x) // objective_pos[1])

    if px_reached and py_reached:
        print("objective reached")
        add_text("objective reached", WINDOW_SIZE//2, 150,10)

def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)

    if cliping == True:
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types["right"] = True

            elif movement[0] < 0:
                rect.left = tile.right
                collision_types["left"] = True

        rect.y += movement[1]
        hit_list = collision_test(rect, tiles)

        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types["bottom"] = True

            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types["top"] = True

    return rect, collision_types


def anti_clip(rect, movement, tiles):
    # prevents player from going into the blocks
    for tile in tiles:
        if rect.colliderect(tile):
            movement[0] += TILE_SIZE + 5

    return rect


running = True

while running:  # game loop
    display.fill(SKY_COLOUR)  # clear screen by filling it with black

    # to keep track of absolute x,y positions
    scroll[0] += (player_rect.x - scroll[0] - 152) / 20
    scroll[1] += (player_rect.y - scroll[1] - 106) / 20

    scroll = scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    draw_bg()

    tile_rects = []
    draw_space(tile_rects)

    # ========================================= events =======================================
    for event in pyg.event.get():  # event loop
        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.KEYDOWN:
            if not pause:
                if event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                    moving_right = True

                if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                    moving_left = True

                if event.key == pyg.K_UP or event.key == pyg.K_w:
                    moving_up = True

                if event.key == pyg.K_DOWN or event.key == pyg.K_s:
                    moving_down = True

        if event.type == pyg.KEYUP:
            if event.key == pyg.K_ESCAPE:
                if pause:
                    pause = False
                else:
                    pause = True
                    moving_right = False
                    moving_left = False
                    moving_up = False
                    moving_down = False

            if event.key == pyg.K_0:
                player_rect.x += 10000

            if event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                moving_right = False

            if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                moving_left = False

            if event.key == pyg.K_UP or event.key == pyg.K_w:
                moving_up = False

            if event.key == pyg.K_DOWN or event.key == pyg.K_s:
                moving_down = False

    # ================================== movement =========================================
    # movement stuff
    player_movement = [0, 0]

    if moving_right == True:
        player_movement[0] += speed * time_deltatime

    if moving_left == True:
        player_movement[0] -= speed * time_deltatime

    if moving_up == True:
        player_movement[1] -= speed * time_deltatime

    if moving_down == True:
        player_movement[1] += speed * time_deltatime

    # flip image in direction of movement
    if player_movement[0] > 0:
        player_flipx = False

    if player_movement[0] < 0:
        player_flipx = True

    if player_movement[1] > 0:
        player_flipy = True

    if player_movement[1] < 0:
        player_flipy = False

    if dev_m == True:
        add_text(f"{round(clock.get_fps())}", 350, 330, 10)
        add_text(f"{player_movement}", 350, 383, 10)

    add_text(f"Health: {player_health} %", 350, 370, 10)
    add_text(f"x: {player_rect.x}   ,y: {player_rect.y}", 350, 350, 10)
    add_text(f"objective: {objective_pos}",  120, 370, 10)
    player_rect = anti_clip(player_rect, player_movement, tile_rects)

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    # draw player
    display.blit(
        pyg.transform.flip(player_img1, player_flipx, player_flipy),
        (player_rect.x - scroll[0], player_rect.y - scroll[1]),
    )

    screen.blit(pyg.transform.scale(display, WINDOW_SIZE), (0, 0))

    if pause:
        draw_pause()
    pyg.display.update()
    time_deltatime = clock.tick(30)

pyg.quit()
