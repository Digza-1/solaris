import pygame
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("test")

# Player objects
player1 = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)
player2 = pygame.Rect(300, 300, PLAYER_SIZE, PLAYER_SIZE)
tri_pos = [(00, 60), (30, 30), (60, 60)]
tri_collider = pygame.draw.polygon(screen, WHITE, tri_pos)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of the keys
    keys = pygame.key.get_pressed()

    # Player 1 movement
    if keys[pygame.K_LEFT]:
        player1.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player1.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player1.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player1.y += PLAYER_SPEED

    # Player 2 movement
    if keys[pygame.K_a]:
        player2.x -= PLAYER_SPEED
    if keys[pygame.K_d]:
        player2.x += PLAYER_SPEED
    if keys[pygame.K_w]:
        player2.y -= PLAYER_SPEED
    if keys[pygame.K_s]:
        player2.y += PLAYER_SPEED

    # Check for collisions
    if player1.colliderect(player2):
        player1_color = RED
        player2_color = RED
    else:
        player1_color = WHITE
        player2_color = WHITE
    
    if player1.colliderect(tri_collider):
        player1_color = RED
        player2_color = RED
    else:
        player1_color = WHITE
        player2_color = WHITE


    # Fill the screen
    screen.fill((0, 0, 0))

    # Draw players
    pygame.draw.rect(screen, player1_color, player1)
    pygame.draw.rect(screen, player2_color, player2)
    pygame.draw.polygon(screen,player1_color,tri_pos)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
pygame.quit()
