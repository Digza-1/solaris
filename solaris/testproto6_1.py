# trying to merge proto5 into gamescript


# import modules for gui
import pygame
import random
import time

import ground_generation as gnd

from pygame.locals import *

# Initialize Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)
# Window dimensions
WIDTH = 1500
HEIGHT = 800

# Colors (RGB)
#       (red,blue,green)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (125, 125, 125)
BROWN = (88, 69, 55)
RED = (255, 0, 0)

# Player dimensions
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 99

# Ground dimensions
BLOCK_SIZE = 25
GROUND_ROWS = HEIGHT // BLOCK_SIZE
GROUND_COLS = WIDTH // BLOCK_SIZE
GROUND_BOTTOM_HALF = (GROUND_ROWS // 2) + 15  # Bottom half of the ground

CHUNK_SIZE = 16

# Create window
display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("pyrraria")
window = pygame.Surface(
    (300, 200)
)  # used as the surface for rendering, which is scaled



clock = pygame.time.Clock()

# Player starting position

player_x = WIDTH // 2 - PLAYER_WIDTH // 2
player_y = HEIGHT // 2 - PLAYER_HEIGHT + 11

player_pos = [player_x, player_y]
player_block = [player_x // BLOCK_SIZE, player_y // BLOCK_SIZE]

moving_right = False
moving_left = False

vertical_momentum = 0
air_timer = 0

player_action = "idle"
player_frame = 0
player_flip = False

true_scroll = [0, 0]
PLAYER_SPEED = 12

player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

background_objects = []

seed = random.randint(1, 20000)


grass_img = pygame.image.load("assets/grass.png")
dirt_img = pygame.image.load("assets/dirt.png")
plant_img = pygame.image.load("assets/plant.png").convert()
plant_img.set_colorkey((255, 255, 255))

player_img = pygame.image.load("assets/player.png").convert()
player_img.set_colorkey((255, 255, 255))

BLOCK_INDEX = {1: grass_img, 2: dirt_img, 3: plant_img}

game_map = {}


# Generate the final ground
def generate_final_ground():
    ground = gnd.generate_air()

    # ground = gnd.generate_uneven_ground(ground)

    ground = gnd.generate_ground(
        2 * WIDTH,
        GROUND_BOTTOM_HALF,
        scale=25.67,
        octaves=10,
        persistence=0.7,
        lacunarity=0.2,
        seed=seed,
    )

    # ground = gnd.generate_ground_layers(ground)

    # ground = gnd.generate_empty_spaces(ground)

    # ground = gnd.generate_trees(ground)

    return ground


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


# Check for collisions
def check_collisions(player_rect, blocks_to_check):
    colliding_list = []
    for block in blocks_to_check:
        if player_rect.colliderect(block):
            colliding_list.append(block)

    return colliding_list


# Draw the player
def draw_player():
    global player_img
    # pygame.draw.rect(window, BLUE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # pygame.draw.rect(
    #     window, RED, (player_block[0], player_block[1], BLOCK_SIZE, BLOCK_SIZE)
    # )
    window.blit(
        pygame.transform.flip(player_img, player_flip, False),
        (player_rect.x , player_rect.y ),
    )



# Draw the ground
def draw_ground(ground):
    for row in range(len(ground)):
        for col in range(len(ground[row])):
            if ground[row][col] == 1:
                pygame.draw.rect(
                    window,
                    GREEN,
                    (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )
            elif ground[row][col] == 2:
                pygame.draw.rect(
                    window,
                    GREY,
                    (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )
            elif ground[row][col] == 3:
                pygame.draw.rect(
                    window,
                    BROWN,
                    (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )


def draw_background():
    global scroll
    for background_object in background_objects:
        obj_rect = pygame.Rect(
            background_object[1][0] - scroll[0] * background_object[0],
            background_object[1][1] - scroll[1] * background_object[0],
            background_object[1][2],
            background_object[1][3],
        )
        if background_object[0] == 0.5:
            pygame.draw.rect(window, (20, 170, 150), obj_rect)
        else:
            pygame.draw.rect(window, (15, 76, 73), obj_rect)


def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False, "right": False, "left": False}
    rect.x += movement[0]
    collision_list = check_collisions(rect, tiles)

    for tile in collision_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True

        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True

    rect.y += movement[1]
    collision_list = check_collisions(rect, tiles)

    for tile in collision_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True

        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True

    return rect, collision_types


def playermovement(scroll):
    global vertical_momentum, player_movement, player_action, player_frame, player_rect
    global game_map, BLOCK_INDEX, air_timer
    tile_rects = []
    for y in range(3):
        for x in range(4):
            target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
            target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))

            target_chunk = str(target_x) + ";" + str(target_y)

            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_chunk_V1(
                    target_x, target_y, CHUNK_SIZE
                )

            for tile in game_map[target_chunk]:
                window.blit(
                    BLOCK_INDEX[tile[1]],
                    (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]),
                )

                if tile[1] in [1, 2]:
                    tile_rects.append(
                        pygame.Rect(tile[0][0] * 16, tile[0][1] * 16, 16, 16)
                    )

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
        player_action, player_frame = change_action(player_action, player_frame, "idle")

    if player_movement[0] > 0:
        player_flip = False
        player_action, player_frame = change_action(player_action, player_frame, "run")

    if player_movement[0] < 0:
        player_flip = True
        player_action, player_frame = change_action(player_action, player_frame, "run")

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

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

    # if player_frame >= len(animation_database[player_action]):
    #     player_frame = 0

    # player_img_id = animation_database[player_action][player_frame]
    # player_img = animation_frames[player_img_id]


# Game loop
def game_loop():
    global player_y  # Declare player_y as global
    global player_x

    # ground = generate_final_ground()
    # ground = generate_caves(ground)  # Add this line to generate caves

    running = True

    while running:
        window.fill(BLACK)
        window.fill((146, 244, 255))  # clear screen by filling it with blue

        # if grass_sound_timer > 0:
        #     grass_sound_timer -= 1

        true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20
        true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        playermovement(scroll)

        # Draw the player and ground

        # draw_ground(ground)

        
        draw_player()
        display.blit(pygame.transform.scale(window, (WIDTH,HEIGHT)), (0, 0))
        
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
    else:
        print("exit")


# Run the game loop
game_loop()

# Quit the game
pygame.quit()
