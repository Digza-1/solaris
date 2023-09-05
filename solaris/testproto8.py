import pygame
import random
import pickle
import noise


# Define chunk size
CHUNK_WIDTH = 10
CHUNK_HEIGHT = GROUND_ROWS

# Initialize loaded chunks dictionary
loaded_chunks = {}


# Generate and load visible chunks
def load_visible_chunks(player_block):
    global loaded_chunks

    current_chunk_index = player_block[0] // CHUNK_WIDTH

    for chunk_index in range(current_chunk_index, current_chunk_index + 2):
        if chunk_index not in loaded_chunks:
            chunk_x = chunk_index * CHUNK_WIDTH * BLOCK_SIZE
            chunk_y = 0
            chunk_ground = generate_final_ground_for_chunk(chunk_x, chunk_y)
            loaded_chunks[chunk_index] = chunk_ground

    chunks_to_unload = [
        chunk_index
        for chunk_index in loaded_chunks
        if abs(chunk_index - current_chunk_index) > 1
    ]
    for chunk_index in chunks_to_unload:
        loaded_chunks.pop(chunk_index)


# Save a chunk using pickle
def save_chunk(chunk_index, chunk_ground):
    with open(f"chunk_{chunk_index}.pkl", "wb") as file:
        pickle.dump(chunk_ground, file)


# Load a chunk using pickle
def load_chunk(chunk_index):
    with open(f"chunk_{chunk_index}.pkl", "rb") as file:
        chunk_ground = pickle.load(file)
    return chunk_ground


# Generate ground for a specific chunk
def generate_final_ground_for_chunk(chunk_x, chunk_y):
    ground = []
    for row in range(CHUNK_HEIGHT):
        ground_row = []
        for col in range(CHUNK_WIDTH):
            # Your chunk-specific ground generation logic here
            # Use chunk_x and chunk_y to determine the position of the chunk
            
            ground_row.append( )  # Example
        ground.append(ground_row)
    return ground


# Game loop
def game_loop():
    global player_block
    global loaded_chunks

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        red_x, red_y = get_block_center_position(
            (player_x), (player_y + 0.5 * PLAYER_HEIGHT), BLOCK_SIZE
        )

        move_player(loaded_chunks[player_block[0] // CHUNK_WIDTH])

        window.fill(BLACK)

        # Draw visible chunks
        for chunk_index, chunk_ground in loaded_chunks.items():
            chunk_x = chunk_index * CHUNK_WIDTH * BLOCK_SIZE
            chunk_y = 0
            draw_chunk(chunk_ground, chunk_x, chunk_y)

        draw_player1()
        draw_red(red_x, red_y)

        pygame.display.flip()

        clock.tick(60)

    # Save loaded chunks using pickle
    for chunk_index, chunk_ground in loaded_chunks.items():
        save_chunk(chunk_index, chunk_ground)

    pygame.quit()


# Run the game loop
game_loop()
