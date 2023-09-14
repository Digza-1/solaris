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

# block values
EMPTY_BLOCK = 0
ROCK_GREY = 2
ROCK_RED = 3
ROCK_BLUE = 1

GREY_OFFSET = 0
RED_OFFSET = 0
BLUE_OFFSET = 0

GREY_THRESHOLD = 0.2
RED_THRESHOLD = 0.6
BLUE_THRESHOLD = 0.3

seed = random.randint(-1000,1000)

noise_generator = opensimplex.OpenSimplex(seed=seed)

# ============================ solaris astroid generation ==============================
# dict based


def get_pos(x, y, scroll, CHUNK_SIZE):
    target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * 16)))
    target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * 16)))




def generate_space(x, y, CHUNK_SIZE):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing

            # openSimplex noise used for generating space
            noise_val = int(noise_generator.noise2(target_x * 0.1, target_y * 0.1) * 5)

            
            # to choose what block must be there
            if GREY_THRESHOLD > GREY_OFFSET - noise_val + random.randrange(1, 4):
                tile_type = 2

            if GREY_THRESHOLD > BLUE_OFFSET - noise_val + random.randint(1, 4):
                tile_type = 1

            if RED_THRESHOLD > RED_OFFSET - noise_val + random.randint(1, 4):
                tile_type = 3

            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data

'''
def generate_space(x, y, offset, CHUNK_SIZE):
    chunk_data = []
    
    for y_pos in range(y, y + CHUNK_SIZE):
        for x_pos in range(x, x + CHUNK_SIZE):
            tile_type = 0  # nothing

            # Use OpenSimplex noise for 2D terrain generation
            noise_val = int(noise_generator.noise2(x_pos * 0.1, y_pos * 0.1) * 5)

            if _THRESHOLD > offset - noise_val + random.randint(1, 4):
                tile_type = 2

            if tile_type != 0:
                chunk_data.append([[x_pos, y_pos], tile_type])

    return chunk_data

'''

# print(generate_space(0, 0, 0, 25))

# ================= Generate gnd old  =================================


def generate_space_old1(x, y, offset, CHUNK_SIZE):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing

            height = 0
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
