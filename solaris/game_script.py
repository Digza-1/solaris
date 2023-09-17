# prototype 5
# file for testing images and chunk generation

import pygame as pyg
import mysql.connector
import ground_generation as gnd


pyg.init()  # initiates pygame
pyg.display.set_caption("solaris")

WINDOW_SIZE = (1400, 750)

screen = pyg.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
display = pyg.Surface((300, 200))
# used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
moving_up = False
moving_down = False

speed = 0.1
scroll = [0, 0]
dev_m = False  # --------------------

CHUNK_SIZE = 8
TILE_SIZE = 16

SKY_COLOUR = (10, 10, 10)  # (146, 244, 255)
SKY_COLOUR1 = (59, 135, 164)

BG_COLOUR = (14, 14, 15)  # (26, 135, 122)  # (19, 127, 115)  # old(15, 76, 73)
BG_COLOUR2 = (26, 135, 122)

game_map = {}

astroid_grey_img = pyg.image.load("solaris/assets/rock.png").convert()
astroid_grey_img.set_colorkey((0, 0, 0))

astroid_grey2_img = pyg.image.load("solaris/assets/rock2.png").convert()
astroid_grey2_img.set_colorkey((0, 0, 0))

astroid_red_img = pyg.image.load("solaris/assets/rock3.png").convert()
astroid_red_img.set_colorkey((0, 0, 0))

astroid_red2_img = pyg.image.load("solaris/assets/rock5.png").convert()
astroid_red2_img.set_colorkey((0, 0, 0))

astroid_blue_img = pyg.image.load("solaris/assets/rock4.png").convert()
astroid_blue_img.set_colorkey((0, 0, 0))


player_img1 = pyg.image.load("solaris/assets/player.png").convert()
player_img1.set_colorkey((0, 0, 0))

player_img2 = pyg.image.load("solaris/assets/player.png").convert()
player_img2.set_colorkey((0, 0, 0))

player_img3 = pyg.image.load("solaris/assets/player.png").convert()
player_img3.set_colorkey((0, 0, 0))

tile_index = {1: astroid_grey_img,4: astroid_grey2_img, 2: astroid_red2_img, 3: astroid_red_img, 5: astroid_blue_img}

player_costume_index = {1: player_img1, 2: player_img2, 3: player_img3}

player_flipx = False
player_flipy = False

player_rect = pyg.Rect(100, 100, 13, 13)


clock = pyg.time.Clock()
time_deltatime = clock.tick(30)

sqlPass = "CH3-CH2-CH2-CH3"

world_id = 0
player_id = 0

def get_settings_sql():
    mydb = mysql.connector.connect(
        ost="localhost", user="root", passwd=sqlPass, database="project_solaris"
    )
    cursor = mydb.cursor()

    q = f'''select (seed,speed,grey_thershold,red_thershold,blue_thershold,difficulty,
    costume) from project_solaris where world_id = {world_id} and player_id = {player_id} ;'''

    cursor.execute(q)
    res = cursor.fetchone()


def draw_space(tile_rects):
    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            # get
            chunk_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * TILE_SIZE)))
            chunk_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * TILE_SIZE)))

            world_x = x + scroll[0]
            world_y = y + scroll[1]

            target_chunk = str(chunk_x) + "," + str(chunk_y)

            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_space(
                    chunk_x, chunk_y, CHUNK_SIZE
                )

            for tile in game_map[target_chunk]:
                if len(tile) > 0 :
                    display.blit(
                        tile_index[tile[1]],
                        (
                            tile[0][0] * TILE_SIZE - scroll[0],
                            tile[0][1] * TILE_SIZE - scroll[1],
                        ),
                    )

                if tile[1] in [1, 2, 3]:
                    tile_rects.append(
                        pyg.Rect(
                            tile[0][0] * TILE_SIZE,
                            tile[0][1] * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE,
                        )
                    )


"""
def draw_space(tile_rects):
    x = scroll[0] + player_rect.x
    y = scroll[1] + player_rect.y

    chunk_x = int(round((x - TILE_SIZE) / (CHUNK_SIZE * TILE_SIZE)))
    chunk_y = int(round((y - TILE_SIZE) / (CHUNK_SIZE * TILE_SIZE)))

    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = chunk_x * CHUNK_SIZE + x_pos
            target_y = chunk_y * CHUNK_SIZE + y_pos
            target_chunk = f"{chunk_x},{chunk_y}"

            if target_chunk not in game_map:
                game_map[target_chunk] = gnd.generate_space(
                    chunk_x, chunk_y, 0, CHUNK_SIZE
                )

            for tile in game_map[target_chunk]:
                display.blit(
                    tile_index[tile[1]],
                    (
                        tile[0][0] * TILE_SIZE - scroll[0],
                        tile[0][1] * TILE_SIZE - scroll[1],
                    ),
                )

                if tile[1] in [1, 2]:
                    tile_rects.append(
                        pyg.Rect(
                            tile[0][0] * TILE_SIZE,
                            tile[0][1] * TILE_SIZE,
                            TILE_SIZE,
                            TILE_SIZE,
                        )
                    )

"""


def draw_bg():
    pyg.draw.rect(display, BG_COLOUR, pyg.Rect(0, 120, 300, 80))



def add_text(text1, x, y, size):
    font = pyg.font.Font("freesansbold.ttf", size)
    text = font.render(text1, True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2)
    display.blit(text, textRect)


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


def get_block(mx, my, scroll, CHUNK_SIZE, TILE_SIZE):
    # to convert mouse coords to world coordinates
    world_x = mx + scroll[0]
    world_y = my + scroll[1]

    # to calculate the chunk and tile coordinates
    chunk_x = world_x // (CHUNK_SIZE * TILE_SIZE)
    chunk_y = world_y // (CHUNK_SIZE * TILE_SIZE)
    tile_x = (world_x // TILE_SIZE) % CHUNK_SIZE
    tile_y = (world_y // TILE_SIZE) % CHUNK_SIZE

    print("Chunk Coordinates (chunk_x, chunk_y):", chunk_x, chunk_y)
    print("Tile Coordinates (tile_x, tile_y):", tile_x, tile_y)


def destroy_block(game_map, mx, my, scroll, CHUNK_SIZE, TILE_SIZE):
    # Convert mouse coordinates to world coordinates
    world_x = mx + scroll[0]
    world_y = my + scroll[1]

    # Calculate the chunk and tile coordinates
    chunk_x = world_x // (CHUNK_SIZE * TILE_SIZE)
    chunk_y = world_y // (CHUNK_SIZE * TILE_SIZE)
    tile_x = (world_x // TILE_SIZE) % CHUNK_SIZE
    tile_y = (world_y // TILE_SIZE) % CHUNK_SIZE

    # Create the chunk identifier
    chunk_key = f"{chunk_x},{chunk_y}"

    # Check if the chunk exists in the game map
    if chunk_key in game_map:
        # Modify the tile in the chunk to an empty tile (tile_type = 0)
        # game_map[chunk_key][tile_y * CHUNK_SIZE + tile_x][1] = 0
        print(game_map[chunk_key])
        for i in range(len(game_map[chunk_key])):
            try:
                print(game_map[chunk_key][i])
                del game_map[chunk_key][i]
            except:
                pass
            # game_map[chunk_key][i][1] = 0


def destroy_astroid():
    pass


running = True

while running:  # game loop
    display.fill(SKY_COLOUR)  # clear screen by filling it with blue

    # to keep track of absolute x,y positions
    scroll[0] += (player_rect.x - scroll[0] - 152) / 20
    scroll[1] += (player_rect.y - scroll[1] - 106) / 20

    scroll = scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    draw_bg()

    tile_rects = []
    draw_space(tile_rects)

    # ========================================= events =======================================
    for event in pyg.event.get():  # event loop
        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.MOUSEBUTTONUP:
            mx, my = pyg.mouse.get_pos()
            get_block(mx, my, scroll, CHUNK_SIZE, TILE_SIZE)
            destroy_block(game_map, mx, my, scroll, CHUNK_SIZE, TILE_SIZE)

        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                moving_right = True

            if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                moving_left = True

            if event.key == pyg.K_UP or event.key == pyg.K_w:
                moving_up = True

            if event.key == pyg.K_DOWN or event.key == pyg.K_s:
                moving_down = True

        if event.type == pyg.KEYUP:
            if event.key == pyg.K_g:
                print(game_map)
            if event.key == pyg.K_RIGHT or event.key == pyg.K_d:
                moving_right = False

            if event.key == pyg.K_LEFT or event.key == pyg.K_a:
                moving_left = False

            if event.key == pyg.K_UP or event.key == pyg.K_w:
                moving_up = False

            if event.key == pyg.K_DOWN or event.key == pyg.K_s:
                moving_down = False

    # ================================== movement =========================================
    # movement stuff
    player_movement = [0, 0]

    if moving_right == True:
        player_movement[0] += speed * time_deltatime

    if moving_left == True:
        player_movement[0] -= speed * time_deltatime

    if moving_up == True:
        player_movement[1] -= speed * time_deltatime

    if moving_down == True:
        player_movement[1] += speed * time_deltatime

    # flip image in direction of movement
    if player_movement[0] > 0:
        player_flipx = False

    if player_movement[0] < 0:
        player_flipx = True

    if player_movement[1] > 0:
        player_flipy = True

    if player_movement[1] < 0:
        player_flipy = False

    if dev_m == True:
        add_text(f"{clock.get_fps()}", 350, 330, 10)
        add_text(f"{player_movement}", 350, 370, 10)
        add_text(f"{player_rect}", 350, 350, 10)

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    # draw player
    display.blit(
        pyg.transform.flip(player_img1, player_flipx, player_flipy),
        (player_rect.x - scroll[0], player_rect.y - scroll[1]),
    )

    screen.blit(pyg.transform.scale(display, WINDOW_SIZE), (0, 0))
    pyg.display.update()
    time_deltatime = clock.tick(30)

pyg.quit()
