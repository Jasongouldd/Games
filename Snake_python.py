import pygame
import random

pygame.font.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Game settings
FPS = 60
VEL = 4

# Snake dimensions
SNAKE_WIDTH, SNAKE_HEIGHT = (20, 20)

# Font settings
SCORE_FONT = pygame.font.SysFont("comicsans", 50)


def draw_window(snake_tail, food, score):
    """
    Draw the game window.
    """
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, food)
    score_text = SCORE_FONT.render("Snake length: " + str(score), 1, BLUE)
    WIN.blit(score_text, (200, 0))

    for tail in snake_tail:
        pygame.draw.rect(WIN, BLUE, [tail[0], tail[1], SNAKE_WIDTH, SNAKE_HEIGHT])

    pygame.display.update()


def snake_movement(keys_pressed, vel):
    """
    Determine the velocity based on the keys pressed.
    """
    vel_x = 0
    vel_y = 0

    if keys_pressed[pygame.K_a]:  # left
        vel_x = -vel
    elif keys_pressed[pygame.K_d]:  # right
        vel_x = vel
    elif keys_pressed[pygame.K_w]:  # up
        vel_y = -vel
    elif keys_pressed[pygame.K_s]:  # down
        vel_y = vel

    return vel_x, vel_y


def main():
    clock = pygame.time.Clock()

    snake_x = WIDTH // 2
    snake_y = HEIGHT // 2

    vel_x = 0
    vel_y = 0

    food_x, food_y = random.randint(50, 650), random.randint(50, 650)

    snake_tail = []
    snake_length = 1
    score = len(snake_tail)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if any(keys_pressed[key] for key in [pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d]):
            vel_x, vel_y = snake_movement(keys_pressed, VEL)

        snake_x += vel_x
        snake_y += vel_y

        snake_head = [snake_x, snake_y]
        snake_tail.append(snake_head)

        if len(snake_tail) > snake_length:
            del snake_tail[0]

        snake_hd = pygame.Rect(snake_x, snake_y, SNAKE_WIDTH, SNAKE_HEIGHT)

        food = pygame.Rect(food_x, food_y, SNAKE_WIDTH, SNAKE_HEIGHT)
        if snake_hd.colliderect(food):
            food_x = random.randint(50, 650)
            food_y = random.randint(50, 650)
            snake_length += 1

        if snake_x >= WIDTH or snake_x < 0 or snake_y >= HEIGHT or snake_y < 0:
            run = False

        if snake_head in snake_tail[:-1]:
            run = False

        score = len(snake_tail) - 1
        draw_window(snake_tail, food, score)

    pygame.quit()


if __name__ == "__main__":
    main()
