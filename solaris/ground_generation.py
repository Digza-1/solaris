import random
import opensimplex
import mysql.connector

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

EMPTY_BLOCK = 0

# default values
GREY_OFFSET = 0
RED_OFFSET = 1
BLUE_OFFSET = 0

GREY_THRESHOLD = 0.25
RED_THRESHOLD = 0.01
BLUE_THRESHOLD = 0.1

seed = 15373  # random.randint(-1000, 1000)
far_limit = 10000000
sqlPass = "123"


def get_settings_sql_gnd(pl_id, wld_id):
    global player_id, world_id
    global seed, GREY_OFFSET, RED_OFFSET, BLUE_OFFSET
    global BLUE_THRESHOLD, RED_THRESHOLD, GREY_THRESHOLD, difficulty
    player_id = pl_id
    world_id = wld_id
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    cursor = mydb.cursor()

    q1 = f"""select seed,grey_threshold,red_threshold,blue_threshold,difficulty,costume
      from game_settings where player_id = {player_id} ;"""

    q2 = f"""select grey_threshold,red_threshold,blue_threshold,difficulty,costume
      from game_default_settings;"""
    try:
        print("q1")
        cursor.execute(q1)
        res = cursor.fetchone()
        print(res)
    except:
        print("q2")
        cursor.execute(q2)
        res = cursor.fetchone()
        print(res)
    (
        seed,
        BLUE_THRESHOLD,
        RED_THRESHOLD,
        GREY_THRESHOLD,
        difficulty,
        costume,
    ) = res


def update_variables(G_OFFSET1, R_OFFSET1, B_OFFSET1, G_THRESH1, R_THRESH1, B_THRESH1):
    global GREY_OFFSET, RED_OFFSET, BLUE_OFFSET, GREY_THRESHOLD, RED_THRESHOLD, BLUE_THRESHOLD
    print("before offests:", GREY_OFFSET, RED_OFFSET, BLUE_OFFSET)

    G_OFFSET1, R_OFFSET1, B_OFFSET1 = GREY_OFFSET, RED_OFFSET, BLUE_OFFSET
    G_THRESH1, R_THRESH1, B_THRESH1 = GREY_THRESHOLD, RED_THRESHOLD, BLUE_THRESHOLD
    print("new offests:", GREY_OFFSET, RED_OFFSET, BLUE_OFFSET)


noise_generator = opensimplex.OpenSimplex(seed=seed)

# ============================ solaris astroid space generation ==============================


def generate_space(x, y, CHUNK_SIZE):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # empty space

            # openSimplex noise used for generating space
            noise_val = int(noise_generator.noise2(target_x * 0.1, target_y * 0.1) * 5)

            total_offset = abs(x_pos / far_limit)
            rnd = random.randint(0, 10)

            # to choose what block must be there
            if (
                GREY_THRESHOLD
                > GREY_OFFSET - noise_val + total_offset + random.randrange(1, 4)
            ):
                if rnd < 5:
                    tile_type = 1
                elif rnd < 7:
                    tile_type = 3
                else:
                    tile_type = 2

            if (
                BLUE_THRESHOLD
                > BLUE_OFFSET - noise_val + total_offset + random.randrange(1, 4)
            ):
                tile_type = 5

            if RED_THRESHOLD > RED_OFFSET - noise_val + random.randrange(1, 4):
                tile_type = 3

            if tile_type != EMPTY_BLOCK:
                chunk_data.append([[target_x, target_y], tile_type])

    return chunk_data


# print(generate_space(0, 0, 0, 25))
