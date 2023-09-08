# prototype 5
# file for testing images and chunk generation

import pygame, os, random, noise
import ground_generation as gnd

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()  # initiates pygame
pygame.display.set_caption("Proto 5")

WINDOW_SIZE = (1400, 750)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pygame.Surface((300, 200))
# used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
moving_up = False
moving_down = False

vertical_momentum = 0
horizontal_momentum = 0

air_timer = 0

scroll = [0, 0]

CHUNK_SIZE = 8


SKY_COLOUR = (10, 10, 10)  # (146, 244, 255)
SKY_COLOUR1 = (59, 135, 164)

BG_COLOUR = (14, 14, 15)  # (26, 135, 122)  # (19, 127, 115)  # old(15, 76, 73)


game_map = {}


grass_img = pygame.image.load("solaris/assets/grass.png")
dirt_img = pygame.image.load("solaris/assets/dirt.png")
plant_img = pygame.image.load("solaris/assets/plant.png").convert()
plant_img.set_colorkey((255, 255, 255))

player_img = pygame.image.load("solaris/assets/player.png").convert()
player_img.set_colorkey((0, 0, 0))

tile_index = {1: grass_img, 2: dirt_img, 3: plant_img}


player_flipx = False
player_flipy = False

grass_sound_timer = 0

player_rect = pygame.Rect(100, 100, 5, 13)

background_objects = []


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

    scroll[0] += (player_rect.x - scroll[0] - 152) / 20
    scroll[1] += (player_rect.y - scroll[1] - 106) / 20
    scroll = scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, BG_COLOUR, pygame.Rect(0, 120, 300, 80))

    for background_object in background_objects:
        obj_rect = pygame.Rect(
            background_object[1][0] - scroll[0] * background_object[0],
            background_object[1][1] - scroll[1] * background_object[0],
            background_object[1][2],
            background_object[1][3],
        )
        if background_object[0] == 0.5:
            pygame.draw.rect(display, SKY_COLOUR1, obj_rect)
        else:
            pygame.draw.rect(display, BG_COLOUR, obj_rect)

    tile_rects = []

    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))

            target_chunk = str(target_x) + ";" + str(target_y)

            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_space_V2(
                    target_x, target_y, 0, CHUNK_SIZE
                )

            for tile in game_map[target_chunk]:
                display.blit(
                    tile_index[tile[1]],
                    (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]),
                )

                if tile[1] in [1, 2]:
                    tile_rects.append(
                        pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16)
                    )
    # ========================================= events =======================================
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = True
                horizontal_momentum += 2

            if event.key == K_LEFT or event.key == K_a:
                moving_left = True
                horizontal_momentum -= 2

            if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                moving_up = True
                vertical_momentum -= 2

            if event.key == K_DOWN or event.key == K_s:
                moving_down = True
                vertical_momentum += 2

        if event.type == KEYUP:
            if event.key == K_g:
                print(game_map)
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False

            if event.key == K_LEFT or event.key == K_a:
                moving_left = False

            if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                moving_up = False

            if event.key == K_DOWN or event.key == K_s:
                moving_down = False

    # ================================== movement =========================================
    # movement stuff
    player_movement = [0, 0]
    if vertical_momentum >= 2:
        vertical_momentum = 2

    if horizontal_momentum >= 2:
        horizontal_momentum = 2

    if vertical_momentum <= -2:
        vertical_momentum = 2

    if horizontal_momentum <= -2:
        horizontal_momentum = 2

    if moving_right == True:
        player_movement[0] += 2

    if moving_left == True:
        player_movement[0] -= 2

    if moving_up == True:
        player_movement[1] -= 2

    if moving_down == True:
        player_movement[1] += 2

    player_movement[0] += horizontal_momentum
    player_movement[1] += vertical_momentum

    if player_movement[0] == 0:
        vertical_momentum = 0

    if player_movement[1] == 0:
        horizontal_momentum = 0

    if player_movement[0] > 0:
        player_flipx = False

    if player_movement[0] < 0:
        player_flipx = True

    if player_movement[1] > 0:
        player_flipy = True

    if player_movement[1] < 0:
        player_flipy = False

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions["bottom"] == True:
        vertical_momentum = 0

    display.blit(
        pygame.transform.flip(player_img, player_flipx, player_flipy),
        (player_rect.x - scroll[0], player_rect.y - scroll[1]),
    )

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
