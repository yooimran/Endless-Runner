import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player properties
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 50
player_speed = 5

# Obstacle properties
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Background properties
bg_color1 = (0, 0, 100)
bg_color2 = (0, 100, 0)
bg_y = 0
bg_speed = 1

# Clock
clock = pygame.time.Clock()


# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Function to draw the player character
def draw_player(x, y):
    # Body
    pygame.draw.rect(screen, GREEN, (x, y + 25, player_width, player_height - 25))
    # Head
    pygame.draw.circle(screen, GREEN, (x + player_width // 2, y + 25), player_width // 2)


# Function to display the start screen
def start_screen():
    screen.fill(BLACK)
    draw_text("Endless Runner", font, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Press SPACE to Start", font, WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Press ESC to Exit", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


# Function to reset the game
def reset_game():
    global player_x, player_y, obstacles, score, game_over
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 50
    obstacles = []
    score = 0
    game_over = False


# Display the start screen
start_screen()

# Main game loop
running = True
game_over = False
while running:
    if not game_over:
        # Background
        bg_y += bg_speed
        if bg_y > HEIGHT:
            bg_y = 0
        pygame.draw.rect(screen, bg_color1, (0, bg_y, WIDTH, HEIGHT))
        pygame.draw.rect(screen, bg_color2, (0, bg_y - HEIGHT, WIDTH, HEIGHT))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Spawn obstacles
        if len(obstacles) == 0 or obstacles[-1][1] > obstacle_height * 2:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacles.append([obstacle_x, 0])

        # Move obstacles
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            pygame.draw.rect(screen, WHITE, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

            # Collision detection
            if player_y < obstacle[1] + obstacle_height and player_x < obstacle[
                0] + obstacle_width and player_x + player_width > obstacle[0]:
                game_over = True

            # Increase score when passing an obstacle
            if obstacle[1] > HEIGHT:
                score += 1
                obstacles.remove(obstacle)

        # Draw the player
        draw_player(player_x, player_y)

        # Display score
        draw_text("Score: " + str(score), font, WHITE, WIDTH // 2, 50)
    else:
        screen.fill(BLACK)
        draw_text("Game Over!", font, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Score: " + str(score), font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Press SPACE to Play Again", font, WHITE, WIDTH // 2, HEIGHT // 2 + 100)
        draw_text("Press ESC to Exit", font, WHITE, WIDTH // 2, HEIGHT // 2 + 150)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                if event.key == pygame.K_ESCAPE:
                    running = False

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
