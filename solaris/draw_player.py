"""import pygame

global animation_frames
animation_frames = {}


# Draw the player
def draw_player1(window, BLUE, player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT):
    pygame.draw.rect(window, BLUE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))


def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 0

    for frame in frame_durations:
        animation_frame_id = animation_name + "_" + str(n)
        img_loc = path + "/" + animation_frame_id + ".png"
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1

    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_states = {}

# animation_states["run"] = load_animation("player_animations/run", [7, 7])
# animation_states["idle"] = load_animation("player_animations/idle", [7, 7, 40])
"""
