import random
import noise
import random
import numpy as np

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
seed1 = random.randint(100, 1000)
CHUNK_SIZE1 = 25


#============================ solaris astroid generation ==============================
#dict based

def get_pos(world):
    for x in world:
        for y in x:
            print(y)



def generate_space_V1(x, y, offset, CHUNK_SIZE):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing
            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)
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



# ================= Generate gnd old  =================================

def generate_screen_ground(
    width1, height1, scale1, octaves1, persistence1, lacunarity1, seed1
):
    # this func uses perlin noise to generate the ground
    # perlin noise is just random but with some continuity

    ground = []
    for y in range(height1 + 1):
        ground_row = []
        for x in range(width1):
            # bool that is true if y greater than height limit
            height_under_limit = y >= int(height1 * 0.5)

            # func used to generate 2d perlin noise
            noise_value = noise.pnoise2(
                x / scale1,
                y / scale1,
                octaves=octaves1,  # no of layers
                persistence=persistence1,  #
                lacunarity=lacunarity1,
                repeatx=width1,
                repeaty=height1,
                base=seed1,
            )

            if y == int(height1 * 0.5) and noise_value < 0.8:
                ground_row.append(GRASS_BLOCK)  # Topmost layer is always green
            else:
                ground_row.append(EMPTY_BLOCK)
            if height_under_limit and noise_value < (
                0.6 - (y - int(height1 * 0.5)) * 0.186
            ):
                ground_row.append(GRASS_BLOCK)  # Green layer

            elif height_under_limit and noise_value < (
                0.77 - (y - int(height1 * 0.5)) * 0.0467
            ):
                if noise_value < (0.4 + (y - GROUND_BOTTOM_HALF) * 0.05):
                    if noise_value < (
                        0.8 + (y - GROUND_BOTTOM_HALF) * 0.005
                        or (
                            ground[y + 1][x] == STONE_BLOCK
                            and ground[y - 1][x] == GRASS_BLOCK
                        )
                    ):
                        ground_row.append(DIRT_BLOCK)  # Dirt
                    else:
                        ground_row.append(STONE_BLOCK)  # Stone block
                else:
                    adjacent_empty = 0
                    if x > 0 and ground_row[x - 1] == EMPTY_BLOCK:
                        adjacent_empty += 1  # Check left

                    if x < len(ground_row) - 1 and ground_row[x + 1] == EMPTY_BLOCK:
                        adjacent_empty += 1  # Check right

                    if adjacent_empty >= 3 or y <= int(height1 * 0.5) + 2:
                        ground_row.append(0)  # Empty space
                    else:
                        ground_row.append(STONE_BLOCK)  # Stone (fallback)
            else:
                ground_row.append(0)  # False represents empty space
        ground.append(ground_row)
    return ground


def generate_ground_chunk(
    x, y, CHUNK_SIZE, width, height, scale, octaves, persistence, lacunarity, seed
):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing

            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)

            if target_y > 8 - height:
                tile_type = DIRT_BLOCK  # dirt

            elif target_y == 8 - height:
                tile_type = GRASS_BLOCK  # grass

            elif target_y == 8 - height - 1:
                if random.randint(1, 5) == 1:
                    tile_type = PLANT  # plant
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data

'''
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
'''


"""
# =============================================================================================
# =============================================================================================
# ================= Generate random ground v3.2 (dict based) =================================


def adj_empty_dict(x, y, height, ground_dict, max_lim, min_lim):
    adjacent_empty = 0

    if x > min_lim and ground_dict[(x - 1, y)] == EMPTY_BLOCK:
        adjacent_empty += 1  # Check left

    if x < max_lim - 1 and ground_dict[(x + 1, y)] == EMPTY_BLOCK:
        adjacent_empty += 1  # Check right

    if adjacent_empty >= 3 or y <= int(height * 0.5) + 2:
        ground_dict[(x, y)] = 0  # Empty space


def chunk_processing_dict(
    x,
    y,
    ground,
    CHUNK_SIZE,
    width,
    height,
    scale,
    octaves,
    persistence,
    lacunarity,
    seed,
):
    for y in range(height + 1):
        ground_row = []
        ground_row = ground[y]

        for x in range(width):
            noise_2d = noise.pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,  # no of layers
                persistence=persistence,  #
                lacunarity=lacunarity,
                repeatx=width,
                repeaty=height,
                base=seed,
            )
            if ground[y][x] == DIRT_BLOCK:
                if noise_2d < (0.77 - (y - int(height * 0.5)) * 0.0467):
                    ground_row.append(DIRT_BLOCK)
                else:
                    ground_row.append(STONE_BLOCK)

            else:
                pass
                # ground_row


def generate_ground_chunk_dict(
    x, y, CHUNK_SIZE, width, height, scale, octaves, persistence, lacunarity, seed
):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing

            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)

            if target_y > 8 - height:
                tile_type = DIRT_BLOCK  # dirt

            elif target_y == 8 - height:
                tile_type = GRASS_BLOCK  # grass

            elif target_y == 8 - height - 1:
                if random.randint(1, 5) == 1:
                    tile_type = PLANT  # plant
            if tile_type != 0:
                pass
                # chunk_data[] = ([[target_x, target_y], tile_type]) #replace

    return chunk_data


def generate_air_dict():
    global GROUND_BOTTOM_HALF

    ground = []
    for row in range(1, GROUND_BOTTOM_HALF):
        ground_row = []
        for col in range(GROUND_COLS):
            ground_row.append(0)
        ground.append(ground_row)
    return ground

"""

"""
#ground generation testing
def generate_ground(width, height, scale, octaves, persistence, lacunarity, seed):
    ground = []
    for y in range(height + 1):
        ground_row = []
        for x in range(width):
            height_under_limit = y >= int(height * 0.5)
            noise_value = noise.pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=width,
                repeaty=height,
                base=seed,
            )

            if y == int(height * 0.5) and noise_value < 0.8:
                ground_row.append(1)  # Topmost layer is always green
            elif height_under_limit and noise_value < (
                0.9 - (y - int(height * 0.5)) * 0.2
            ):
                ground_row.append(1)  # Green layer
            elif height_under_limit and noise_value < (
                0.67 - (y - int(height * 0.5)) * 0.046
            ):
                if noise_value < (0.4 + (y - int(height * 0.5)) * 0.05):
                    if noise_value < (0.8 + (y - int(height * 0.5)) * 0.005):
                        ground_row.append(2)  # Dirt
                    else:
                        ground_row.append(3)  # Stone block
                else:
                    adjacent_empty = 0
                    if x > 0 and ground_row[x - 1] == 0:
                        adjacent_empty += 1  # Check left
                    if x < len(ground_row) - 1 and ground_row[x + 1] == 0:
                        adjacent_empty += 1  # Check right

                    if adjacent_empty >= 3 or y <= int(height * 0.5) + 2:
                        ground_row.append(0)  # Empty space
                    else:
                        ground_row.append(3)  # Stone (fallback)
            else:
                ground_row.append(0)  # False represents empty space
        ground.append(ground_row)

    return ground"""
