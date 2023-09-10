# prototype 5
# file for testing images and chunk generation

import pygame as pyg
import os, random
import ground_generation as gnd


pyg.init()  # initiates pygame
pyg.display.set_caption("solaris")

WINDOW_SIZE = (1400, 750)

screen = pyg.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pyg.Surface((300, 200))
# used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
moving_up = False
moving_down = False

acceleration = 0.1
scroll = [0, 0]
dev_m = True #------


CHUNK_SIZE = 8
TILE_SIZE = 16


SKY_COLOUR = (10, 10, 10)  # (146, 244, 255)
SKY_COLOUR1 = (59, 135, 164)


BG_COLOUR = (14, 14, 15)  # (26, 135, 122)  # (19, 127, 115)  # old(15, 76, 73)
BG_COLOUR2 = (26, 135, 122)

game_map = {}

CWD = os.getcwd()

astroid_1_img = pyg.image.load("solaris/assets/rock.png").convert()
astroid_1_img.set_colorkey((0, 0, 0))
# astroid_2_img = pyg.image.load("solaris/assets/dirt.png").convert()
# astroid_3_img = pyg.image.load("solaris/assets/dirt.png").convert()

player_img = pyg.image.load("solaris/assets/player.png").convert()
player_img.set_colorkey((0, 0, 0))

tile_index = {1: astroid_1_img, 2: astroid_1_img}


player_flipx = False
player_flipy = False

grass_sound_timer = 0

player_rect = pyg.Rect(100, 100, 13, 13)

background_objects = []  # [[0.5,[1,0,30,3]],[1,[7,10,30,100]]]

clock = pyg.time.Clock()
time_deltatime = clock.tick(30)


def draw_space(tile_rects):
    for y in range(4):
        for x in range(4):
            # get 
            chunk_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * TILE_SIZE)))
            chunk_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * TILE_SIZE)))

            target_chunk = str(chunk_x) + "," + str(chunk_y)

            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_space(
                    chunk_x, chunk_y, 0, CHUNK_SIZE
                )

            for tile in game_map[target_chunk]:
                display.blit(
                    tile_index[tile[1]],
                    (
                        tile[0][0] * TILE_SIZE - scroll[0],
                        tile[0][1] * TILE_SIZE - scroll[1],
                    ),
                )

                if tile[1] in [1, 2]:
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

    for background_object in background_objects:
        obj_rect = pyg.Rect(
            background_object[1][0] - scroll[0] * background_object[0],
            background_object[1][1] - scroll[1] * background_object[0],
            background_object[1][2],
            background_object[1][3],
        )
        if background_object[0] == 0.5:
            pyg.draw.rect(display, SKY_COLOUR1, obj_rect)

        if background_object[0] == 1:
            pyg.draw.rect(display, BG_COLOUR2, obj_rect)

        else:
            pyg.draw.rect(display, BG_COLOUR, obj_rect)


def add_text(text1, x, y, size):
    font = pyg.font.Font("freesansbold.ttf", size)
    text = font.render(text1, True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)
    display.blit(text, textRect)


def destroy_astroid():
    pass


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)

    return hit_list


def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)

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


running = True

while running:  # game loop
    display.fill(SKY_COLOUR)  # clear screen by filling it with blue

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

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
            if event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                moving_right = True

            if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                moving_left = True

            if event.key == pyg.K_UP or event.key == pyg.K_w:
                moving_up = True

            if event.key == pyg.K_DOWN or event.key == pyg.K_s:
                moving_down = True

        if event.type == pyg.KEYUP:
            if event.key == pyg.K_g:
                print(game_map)
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
        player_movement[0] += acceleration * time_deltatime

    if moving_left == True:
        player_movement[0] -= acceleration * time_deltatime

    if moving_up == True:
        player_movement[1] -= acceleration * time_deltatime

    if moving_down == True:
        player_movement[1] += acceleration * time_deltatime
        
    # flip image in direction of movement
    if player_movement[0] > 0:
        player_flipx = False

    if player_movement[0] < 0:
        player_flipx = True

    if player_movement[1] > 0:
        player_flipy = True

    if player_movement[1] < 0:
        player_flipy = False

    if dev_m ==True:
        add_text(f"{clock.get_fps()}", 350, 330, 10)
        add_text(f"{player_movement}", 350, 370, 10)
        add_text(f"{player_rect}", 350, 350, 10)

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    # draw player
    display.blit(
        pyg.transform.flip(player_img, player_flipx, player_flipy),
        (player_rect.x - scroll[0], player_rect.y - scroll[1]),
    )

    screen.blit(pyg.transform.scale(display, WINDOW_SIZE), (0, 0))
    pyg.display.update()
    time_deltatime = clock.tick(30)

pyg.quit()
