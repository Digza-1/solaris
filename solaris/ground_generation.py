import random
import opensimplex


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


def insert_sql_settings(mydb, cursor, pl_id):
    print("creating settings ")
    q1_1 = f"""select speed,grey_threshold,red_threshold,blue_threshold,difficulty,costume
      from game_default_settings; """

    res1 = cursor.fetchone()
    (
        speed,
        grey_thershold,
        red_threshold,
        blue_thershold,
        difficulty,
        costume,
    ) = res1

    q1_2 = f"""insert into game_settings(player_id,speed,grey_threshold,red_threshold,blue_threshold,difficulty,costume)
    values ({pl_id},{speed},
    {grey_thershold},{red_threshold},
    {blue_thershold},{difficulty},
    {costume});"""
    cursor.execute(q1_2)
    mydb.commit()


def get_settings_sql_gnd(pl_id, wld_id):
    global player_id, world_id
    global seed, GREY_OFFSET, RED_OFFSET, BLUE_OFFSET
    global BLUE_THRESHOLD, RED_THRESHOLD, GREY_THRESHOLD, difficulty
    player_id = pl_id
    world_id = wld_id


    q1 = f"""select grey_threshold,red_threshold,blue_threshold,difficulty,costume
      from game_settings where player_id = {player_id} ;"""

    q3 = f"""select seed from game_worlds where player_id = {player_id} and world_id = {world_id}"""

    try:
        print("q1")
        cursor.execute(q1)
        res = cursor.fetchone()

        if res == None:
            insert_sql_settings(mydb, cursor, pl_id)
            cursor.execute(q1)
            res = cursor.fetchone()
        print(res)
        (
            BLUE_THRESHOLD,
            RED_THRESHOLD,
            GREY_THRESHOLD,
            difficulty,
            costume,
        ) = res
    except:
        insert_sql_settings(mydb, cursor, pl_id)

    gnd_gen_init(seed)


noise_generator = None


def gnd_gen_init(seed1):
    global noise_generator, seed
    print("seed = ", seed1)
    seed = seed1
    noise_generator = opensimplex.OpenSimplex(seed=seed1)


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
