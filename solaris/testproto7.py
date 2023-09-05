# import modules for gui
import pygame
import random
import time
import math
import ground_generation as gnd
import draw_player

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH = 1500
HEIGHT = 800

# Ground dimensions
BLOCK_SIZE = 25
CHUNK_SIZE = 8

# Player dimensions
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 99

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


GROUND_ROWS = HEIGHT // BLOCK_SIZE
GROUND_COLS = WIDTH // BLOCK_SIZE
GROUND_BOTTOM_HALF = (GROUND_ROWS // 2) + 15  # Bottom half of the ground


# Colors (RGB)
#       (red,blue,green)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (125, 125, 125)
BROWN = (88, 69, 55)
RED = (255, 0, 0)


# Create window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pyrraria")

# images

grass_img = pygame.image.load("assets/grass.png")
dirt_img = pygame.image.load("assets/dirt.png")
plant_img = pygame.image.load("assets/plant.png").convert()
plant_img.set_colorkey((255, 255, 255))

player_img = pygame.image.load("assets/player.png").convert()
player_img.set_colorkey((255, 255, 255))

tile_index = {1: grass_img, 2: dirt_img, 3: plant_img}


clock = pygame.time.Clock()


player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

background_objects = []

seed = random.randint(1, 20000)


# Generate the final ground
def generate_final_ground():
    ground = gnd.generate_air()

    # ground = gnd.generate_uneven_ground(ground)

    ground = gnd.generate_screen_ground(
        2 * WIDTH,
        GROUND_BOTTOM_HALF,
        scale=25.67,
        octaves=10,
        persistence=0.7,
        lacunarity=0.2,
        seed=seed,
        scale=25.67
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


def get_block_center_position(click_x, click_y, blockSize):
    grid_x = click_x // blockSize
    grid_y = click_y // blockSize

    center_x = grid_x * blockSize + (blockSize)
    center_y = grid_y * blockSize + (blockSize)

    return center_x, center_y


def draw_red(red_x, red_y):
    pygame.draw.rect(
        window,
        RED,
        (
            red_x,
            red_y,
            BLOCK_SIZE,
            BLOCK_SIZE,
        ),
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

            elif ground[row][col] == 4:
                pygame.draw.rect(
                    window,
                    RED,
                    (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )


# Player movement
def move_player(ground):
    global player_x, player_y
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED

    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:
        player_x += PLAYER_SPEED

    if keys[pygame.K_UP] and player_y > 0:
        player_y -= 5

    if keys[pygame.K_DOWN] and player_y < HEIGHT - PLAYER_HEIGHT:
        player_y += 5

    # if keys[pygame.K_v]:
    #     ground[int(red_x // BLOCK_SIZE)][int(red_y // BLOCK_SIZE)]

    # player_pos[0], player_pos[1] = player_x, player_y
    # player_block[0], player_block[1] = player_x, player_y


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


# Game loop
def game_loop():
    global player_y  # Declare player_y as global
    global player_x

    ground = generate_final_ground()
    # ground = generate_caves(ground)  # Add this line to generate caves

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(BLACK)

        red_x, red_y = get_block_center_position(
            (player_x), (player_y + 0.5 * PLAYER_HEIGHT), BLOCK_SIZE
        )
        move_player(ground)

        # Draw the player and ground
        draw_ground(ground)

        draw_player.draw_player1(
            window, BLUE, player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT
        )

        draw_red(red_x, red_y)

        pygame.display.flip()

        clock.tick(60)
    else:
        print("exit")


# Run the game loop
game_loop()

# Quit the game
pygame.quit()
