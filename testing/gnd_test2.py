import noise
import numpy as np
import matplotlib.pyplot as plt


def generate_ground_v3(
    x, y, offset, seed, scale, octaves, persistence, lacunarity, CHUNK_SIZE, FULL_HEIGHT
):
    chunk_data = []

    for x_pos in range(CHUNK_SIZE):
        target_x = x * CHUNK_SIZE + x_pos
        column_data = []

        # Layer 1: 1D noise for stone and air
        stone_value = generate_stone_layer(target_x, scale, seed)
        if stone_value > 0.1:  # Adjust the threshold as needed
            column_data.append(1)  # Stone
        else:
            column_data.append(0)  # Air

        # Layer 2: 1D noise for thickness of dirt layer
        dirt_thickness = generate_dirt_layer(target_x, scale, seed)
        column_data.extend([1] * dirt_thickness)

        # Layer 3: 2D noise for ores
        ore_value = generate_ore_layer(target_x, y, scale, octaves, persistence, lacunarity, seed)
        if ore_value > 0.2:  # Adjust the threshold as needed
            column_data.append(2)  # Ore
        else:
            column_data.append(1)  # Stone

        # Layer 4 and 5: 2D noise for caves
        cave_value = generate_cave_layer(target_x, y, scale, octaves, persistence, lacunarity, seed)
        if cave_value > 0.5:  # Adjust the threshold as needed
            column_data[0] = 0  # Air (overwrite stone with air)

        # Pad with air to reach full height
        while len(column_data) < FULL_HEIGHT:
            column_data.append(0)  # Air

        # Trim to full height
        column_data = column_data[:FULL_HEIGHT]

        chunk_data.append(column_data)

    return chunk_data

def generate_stone_layer(x, scale, seed):
    stone_noise = noise.pnoise1(x * scale, base=seed)
    return stone_noise

def generate_dirt_layer(x, scale, seed):
    dirt_noise = noise.pnoise1(x * scale, base=seed + 1)
    dirt_thickness = int(FULL_HEIGHT * (dirt_noise + 1) / 2)
    return dirt_thickness

def generate_ore_layer(x, y, scale, octaves, persistence, lacunarity, seed):
    ore_noise = noise.pnoise2(
        x * scale,
        y * scale,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        base=seed + 2,
    )
    return ore_noise

def generate_cave_layer(x, y, scale, octaves, persistence, lacunarity, seed):
    cave_noise = noise.pnoise2(
        x * scale * 10,
        y * scale * 10,
        octaves=octaves,
        persistence=persistence,
        lacunarity=lacunarity,
        base=seed + 3,
    )
    return cave_noise

def visualize_chunk(chunk_data):
    chunk_height = len(chunk_data)
    chunk_width = len(chunk_data[0])
    terrain = np.zeros((chunk_height, chunk_width, 3), dtype=np.uint8)

    for i in range(chunk_height):
        for j in range(chunk_width):
            if chunk_data[i][j] == 0:  # Air
                terrain[i, j] = [135, 206, 235]  # Sky color

            elif chunk_data[i][j] == 1:  # Stone
                terrain[i, j] = [169, 169, 169]  # Gray for stone

            elif chunk_data[i][j] == 4:  # dirt
                terrain[i, j] = [146, 94, 34]  # brown

            elif chunk_data[i][j] == 2:  # Ore
                terrain[i, j] = [255, 215, 0]  # Gold color

    plt.imshow(terrain)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    CHUNK_SIZE = 300  # Adjust the chunk size as needed
    FULL_HEIGHT = 300  # Adjust the full height as needed
    seed = 0  # Seed for noise generation
    scale = 0.008
    octaves = 2
    persistence = 0.4
    lacunarity = 1.8

    # Specify the chunk coordinates (x, y)
    chunk_x = 999
    chunk_y = 0

    chunk_data = generate_ground_v3(
        chunk_x,
        chunk_y,
        10,
        seed,
        scale,
        octaves,
        persistence,
        lacunarity,
        CHUNK_SIZE,
        FULL_HEIGHT,
    )

    # Visualize the generated chunk
    visualize_chunk(chunk_data)
