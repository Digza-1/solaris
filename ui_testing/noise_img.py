import noise
import numpy as np
import cv2


def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity, seed):
    perlin_noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            perlin_noise[y][x] = round(noise.pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=4024,
                repeaty=4024,
                base=seed,
            ),1)

    return perlin_noise

def perlin_2(width, height, scale, octaves, persistence, lacunarity, seed):
    perlin_noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            perlin_noise[y][x] = round(noise.pnoise2(
                x / scale,
                y / scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=4024,
                repeaty=4024,
                base=seed,
            ),1)

    return perlin_noise


def normalize_perlin_noise(perlin_noise):
    return (perlin_noise - perlin_noise.min()) / (
        perlin_noise.max() - perlin_noise.min()
    )


def show_perlin_noise_image(perlin_noise):
    normalized_noise = normalize_perlin_noise(perlin_noise) * 255
    img = np.array(normalized_noise, dtype=np.uint8)
    cv2.imshow("Perlin Noise Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_perlin_noise_image_raw(perlin_noise):
    img = np.array(perlin_noise, dtype=np.uint8)
    cv2.imshow("Perlin Noise Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def add_color(world):
    color_world = np.zeros(world.shape + (3,), dtype=np.uint8)
    height, width = world.shape  # Get the dimensions from the input world

    for i in range(height):
        for j in range(width):
            if world[i][j] < 1.0:
                if world[i][j] < -0.05:
                    color_world[i][j] = np.array(
                        [0, 0, 255], dtype=np.uint8
                    )  # Blue for deep areas
                elif world[i][j] < 0:
                    color_world[i][j] = np.array(
                        [255, 0, 0], dtype=np.uint8
                    )  # Red for shallow areas
                else:
                    color_world[i][j] = np.array(
                        [0, 255, 0], dtype=np.uint8
                    )  # Green for intermediate areas
            else:
                color_world[i][j] = np.array(
                    [0, 0, 0], dtype=np.uint8
                )  # Black for values >= 1.0

    return color_world


def no_colour(world):
    height, width = world.shape
    world2 = np.zeros(world.shape, dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            if world[i][j] < 1.0:
                if world[i][j] < -0.05:
                    world2[i][j] = np.array([255], dtype=np.uint8)
                elif world[i][j] < 0:
                    world2[i][j] = np.array([125], dtype=np.uint8)
                else:
                    world2[i][j] = np.array([50], dtype=np.uint8)
            else:
                world2[i][j] = np.array([0], dtype=np.uint8)  # Black for values >= 1.0

    return world2


shape = (512, 512)

width = 512
height = 512
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = 0

# perlin_noise1 = generate_perlin_noise(
#     width, height, scale, octaves, persistence, lacunarity, seed
# )
perlin_noise1 = perlin_2(
    width, height, scale, octaves, persistence, lacunarity, seed
)

show_perlin_noise_image(perlin_noise1)