import random
import opensimplex

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (125, 125, 125)
BROWN = (88, 69, 55)
RED = (255, 0, 0)

# Player Properties
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 99
PLAYER_SPEED = 6
player_direction = 0

# Ground dimensions
GROUND_SIZE = 20
GROUND_ROWS = HEIGHT // GROUND_SIZE
GROUND_COLS = WIDTH // GROUND_SIZE
GROUND_BOTTOM_HALF = int(GROUND_ROWS * 0.6)  # Bottom half of the ground

# Player starting position
player_x = int(WIDTH * 0.5 - PLAYER_WIDTH * 0.5)
player_y = HEIGHT - PLAYER_HEIGHT


# block values
EMPTY_BLOCK = 0
GRASS_BLOCK = 1
DIRT_BLOCK = 2
STONE_BLOCK = 3
PLANT = 5

repeatx1 = 99999
repeaty1 = 99999
scale1 = 25.67
octaves1 = 10
persistence1 = 0.7
lacunarity1 = 0.2
seed1 = random.randint(-1000, 1000)
CHUNK_SIZE1 = 25

noise_generator = opensimplex.OpenSimplex(seed=seed1)
# ============================ solaris astroid generation ==============================
# dict based


def get_pos(x, y, scroll, CHUNK_SIZE):
    target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
    target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))


lim1 = 0.4  # temp
lim2 = 0.2


def generate_space(x, y, offset, CHUNK_SIZE):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing

            # Use OpenSimplex noise for 2D terrain generation
            noise_val = int(noise_generator.noise2(target_x * 0.1, target_y * 0.1) * 5)

            # if lim1 > offset - noise_val:
            #     tile_type = 2

            if lim2 > offset - noise_val + random.randint(1, 4):
                tile_type = 2

            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data


# print(generate_space(0, 0, 0, 25))

# ================= Generate gnd old  =================================


def generate_space_old1(x, y, offset, CHUNK_SIZE):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing

            height = 0  # int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)

            if target_y > offset - height:
                tile_type = 2  # dirt

            elif target_y == offset - height:
                tile_type = 1  # grass

            elif target_y == offset - height + random.randint(1, 4):
                tile_type = 3  # stone

            elif target_y == offset - height - 1:
                if random.randint(1, 5) == 1:
                    tile_type = 3  # plant

            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data


"""===============old=============="""

"""
# Generate larger diagonal caves in the ground
def generate_caves(ground):
    global GROUND_COLS
    for row in range(GROUND_BOTTOM_HALF, GROUND_ROWS):
        for col in range(GROUND_COLS):
            if random.random() < 0.7:
                # Check if the position is within the cave diagonal pattern
                if col < row or col >= GROUND_COLS - row or random.random() < 0.3:
                    ground[row][col] = 0  # Empty space (cave)

    return ground
"""
