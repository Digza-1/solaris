# trying to merge gamescript into proto5

import pygame, sys, os, random, noise
import ground_generation as gnd
import draw_player as draw_p

clock = pygame.time.Clock()

from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiates pygame
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("Proto 5")

WIDTH, HEIGHT = 1500, 800
WINDOW_SIZE = (WIDTH, HEIGHT)


screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface(
    (300, 200)
)  # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0

scroll_type = 1  # (contant) max follow, min follow
true_scroll = [0, 0]

CHUNK_SIZE = 8

game_map = {}

scale = 10
octaves = 8
persistence = 1.1
lacunarity = 1.1
seed = random.randint(100, 1000000)


grass_img = pygame.image.load("assets/grass.png")
dirt_img = pygame.image.load("assets/dirt.png")
stone_img = pygame.image.load("assets/dirt.png")

plant_img = pygame.image.load("assets/plant.png").convert()
plant_img.set_colorkey((255, 255, 255))

player_img = pygame.image.load("assets/player.png")

block_index = {1: grass_img, 2: dirt_img, 3: stone_img, 5: plant_img}

# jump_sound = pygame.mixer.Sound("jump.wav")
# grass_sounds = [pygame.mixer.Sound("grass_0.wav"), pygame.mixer.Sound("grass_1.wav")]
# grass_sounds[0].set_volume(0.2)
# grass_sounds[1].set_volume(0.2)

player_action = "idle"
player_frame = 0
player_flip = False

grass_sound_timer = 0

player_rect = pygame.Rect(100, 100, 5, 13)

background_objects = []


def collision_test(rect, blocks):
    hit_list = []
    for block in blocks:
        if rect.colliderect(block):
            hit_list.append(block)

    return hit_list


# =======================movement=========================================================================
def move(rect, movement, blocks):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, blocks)

    for block in hit_list:
        if movement[0] > 0:
            rect.right = block.left
            collision_types["right"] = True

        elif movement[0] < 0:
            rect.left = block.right
            collision_types["left"] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, blocks)

    for block in hit_list:
        if movement[1] > 0:
            rect.bottom = block.top
            collision_types["bottom"] = True

        elif movement[1] < 0:
            rect.top = block.bottom
            collision_types["top"] = True

    return rect, collision_types


def draw_background():
    global CHUNK_SIZE, width, height, scale, octaves, persistence, lacunarity, seed
    global block_rects
    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))

    for background_object in background_objects:
        obj_rect = pygame.Rect(
            background_object[1][0] - scroll[0] * background_object[0],
            background_object[1][1] - scroll[1] * background_object[0],
            background_object[1][2],
            background_object[1][3],
        )
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (20, 170, 150), obj_rect)
        else:
            pygame.draw.rect(display, (15, 76, 73), obj_rect)

    block_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))

            target_chunk = str(target_x) + ";" + str(target_y)

            # ==========================genrate ground=================================================================
            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_ground_chunk(
                    x,
                    y,
                    CHUNK_SIZE,
                    WIDTH,
                    HEIGHT,
                    scale,
                    octaves,
                    persistence,
                    lacunarity,
                    seed,
                )

            for block in game_map[target_chunk]:
                display.blit(
                    block_index[block[1]],
                    (block[0][0] * 16 - scroll[0], block[0][1] * 16 - scroll[1]),
                )

                if block[1] in [1, 2]:
                    block_rects.append(
                        pygame.Rect(block[0][0] * 16, block[0][1] * 16, 16, 16)
                    )


def scrolling(player_rect, scroll_type):
    global true_scroll
    if scroll_type == 1:
        # contant max scroll
        true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

    return scroll


def player_move():
    global vertical_momentum, player_rect, player_action, player_frame, air_timer, player_flip

    player_movement = [0, 0]

    if moving_right == True:
        player_movement[0] += 2

    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2

    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action, player_frame = draw_p.change_action(
            player_action, player_frame, "idle"
        )

    if player_movement[0] > 0:
        player_flip = False
        player_action, player_frame = draw_p.change_action(
            player_action, player_frame, "run"
        )

    if player_movement[0] < 0:
        player_flip = True
        player_action, player_frame = draw_p.change_action(
            player_action, player_frame, "run"
        )

    player_rect, collisions = move(player_rect, player_movement, block_rects)

    if collisions["bottom"] == True:
        air_timer = 0
        vertical_momentum = 0

        # if player_movement[0] != 0:
        #     if grass_sound_timer == 0:
        #         grass_sound_timer = 30
        #         random.choice(grass_sounds).play() #sounds later
    else:
        air_timer += 1

    player_frame += 1


running = True

while running:  # game loop
    display.fill((146, 244, 255))  # clear screen by filling it with blue

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    scroll = scrolling(player_rect, scroll_type=scroll_type)

    draw_background()

    player_move()

    # if player_frame >= len(animation_database[player_action]):
    #     player_frame = 0

    # player_img_id = animation_database[player_action][player_frame]
    # player_img = animation_frames[player_img_id]

    display.blit(
        pygame.transform.flip(player_img, player_flip, False),
        (player_rect.x - scroll[0], player_rect.y - scroll[1]),
    )

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)

            if event.key == K_RIGHT:
                moving_right = True

            if event.key == K_LEFT:
                moving_left = True

            if event.key == K_UP:
                if air_timer < 6:
                    # jump_sound.play()  #sound later
                    vertical_momentum = -5

        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False

            if event.key == K_LEFT:
                moving_left = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
