import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20
GAME_SPEED = 12

# Color Palette (RGB)
COLOR_BG = (20, 24, 33)
COLOR_GRID = (30, 36, 48)
COLOR_SNAKE_HEAD = (46, 204, 113)
COLOR_SNAKE_BODY = (39, 174, 96)
COLOR_FOOD = (231, 76, 60)
COLOR_TEXT = (236, 240, 241)
COLOR_TEXT_DIM = (149, 165, 166)

# Set up Display Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Python Pygame")
clock = pygame.time.Clock()

# Fonts
font_score = pygame.font.SysFont("arial", 18, bold=True)
font_message = pygame.font.SysFont("arial", 28, bold=True)
font_sub = pygame.font.SysFont("arial", 16)


def draw_grid():
    """Draws a subtle background grid."""
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))


def generate_food(snake_body):
    """Generates a random food position not overlapping the snake body."""
    while True:
        food_x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        food_y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        if (food_x, food_y) not in snake_body:
            return food_x, food_y


def draw_snake(snake_body):
    """Draws the snake with a distinct head and rounded segments."""
    for i, (x, y) in enumerate(snake_body):
        color = COLOR_SNAKE_HEAD if i == len(snake_body) - 1 else COLOR_SNAKE_BODY
        rect = pygame.Rect(x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
        pygame.draw.rect(screen, color, rect, border_radius=4)


def main_game():
    """Main game loop handling state, input, rendering, and logic."""
    # Snake Initial Position (center screen)
    start_x = SCREEN_WIDTH // 2
    start_y = SCREEN_HEIGHT // 2
    snake_body = [(start_x - BLOCK_SIZE * 2, start_y), 
                  (start_x - BLOCK_SIZE, start_y), 
                  (start_x, start_y)]
    
    # Movement Variables
    dir_x, dir_y = BLOCK_SIZE, 0
    next_dir_x, next_dir_y = BLOCK_SIZE, 0
    
    # Game State Variables
    food_x, food_y = generate_food(snake_body)
    score = 0
    game_over = False

    while True:
        # Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        main_game()  # Restart
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    # Prevent 180-degree immediate turns
                    if event.key == pygame.K_UP and dir_y == 0:
                        next_dir_x, next_dir_y = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dir_y == 0:
                        next_dir_x, next_dir_y = 0, BLOCK_SIZE
                    elif event.key == pygame.K_LEFT and dir_x == 0:
                        next_dir_x, next_dir_y = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and dir_x == 0:
                        next_dir_x, next_dir_y = BLOCK_SIZE, 0

        if not game_over:
            # Commit Direction Change
            dir_x, dir_y = next_dir_x, next_dir_y

            # Calculate New Head Position
            head_x, head_y = snake_body[-1]
            new_head_x = head_x + dir_x
            new_head_y = head_y + dir_y

            # Collision Check: Wall Boundaries
            if (new_head_x < 0 or new_head_x >= SCREEN_WIDTH or
                new_head_y < 0 or new_head_y >= SCREEN_HEIGHT):
                game_over = True

            # Collision Check: Self Collision
            if (new_head_x, new_head_y) in snake_body:
                game_over = True

            if not game_over:
                snake_body.append((new_head_x, new_head_y))

                # Food Collision Check
                if new_head_x == food_x and new_head_y == food_y:
                    score += 10
                    food_x, food_y = generate_food(snake_body)
                else:
                    snake_body.pop(0)  # Move forward by removing tail

        # Render Screen Elements
        screen.fill(COLOR_BG)
        draw_grid()

        # Render Food
        food_rect = pygame.Rect(food_x + 2, food_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
        pygame.draw.rect(screen, COLOR_FOOD, food_rect, border_radius=6)

        # Render Snake
        draw_snake(snake_body)

        # Render HUD Score
        score_surface = font_score.render(f"Score: {score}", True, COLOR_TEXT)
        screen.blit(score_surface, (15, 12))

        # Game Over Screen Overlay
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            msg_surface = font_message.render("GAME OVER", True, COLOR_FOOD)
            score_final = font_sub.render(f"Final Score: {score}", True, COLOR_TEXT)
            instruction = font_sub.render("Press R to Restart or Q to Quit", True, COLOR_TEXT_DIM)

            screen.blit(msg_surface, (SCREEN_WIDTH // 2 - msg_surface.get_width() // 2, 120))
            screen.blit(score_final, (SCREEN_WIDTH // 2 - score_final.get_width() // 2, 180))
            screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 220))

        pygame.display.flip()
        clock.tick(GAME_SPEED)


if __name__ == "__main__":
    main_game()