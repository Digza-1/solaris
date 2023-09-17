import random
import opensimplex

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (125, 125, 125)
BROWN = (88, 69, 55)
RED = (255, 0, 0)

EMPTY_BLOCK = 0

# default values
GREY_OFFSET = 0
RED_OFFSET = 1
BLUE_OFFSET = 0

GREY_THRESHOLD = 0.25
RED_THRESHOLD = 0.01
BLUE_THRESHOLD = 0.1


def update_variables(G_OFFSET1, R_OFFSET1, B_OFFSET1, G_THRESH1, R_THRESH1, B_THRESH1):
    global GREY_OFFSET, RED_OFFSET, BLUE_OFFSET, GREY_THRESHOLD, RED_THRESHOLD, BLUE_THRESHOLD
    print('before offests:',GREY_OFFSET, RED_OFFSET, BLUE_OFFSET)

    G_OFFSET1, R_OFFSET1, B_OFFSET1 = GREY_OFFSET, RED_OFFSET, BLUE_OFFSET
    G_THRESH1, R_THRESH1, B_THRESH1 = GREY_THRESHOLD, RED_THRESHOLD, BLUE_THRESHOLD
    print('new offests:',GREY_OFFSET, RED_OFFSET, BLUE_OFFSET)


seed = random.randint(-1000, 1000)

noise_generator = opensimplex.OpenSimplex(seed=seed)

# ============================ solaris astroid space generation ==============================

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

            rnd = random.randint(0, 10)

            # to choose what block must be there
            if GREY_THRESHOLD > GREY_OFFSET - noise_val + random.randrange(1, 4):
                if rnd < 5:
                    tile_type = 1
                elif rnd < 7:
                    tile_type = 3
                else:
                    tile_type = 2

            if BLUE_THRESHOLD > BLUE_OFFSET - noise_val + random.randint(1, 4):
                tile_type = 5

            if RED_THRESHOLD > RED_OFFSET - noise_val + random.randint(1, 4):
                tile_type = 3

            if tile_type != EMPTY_BLOCK:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data
# print(generate_space(0, 0, 0, 25))