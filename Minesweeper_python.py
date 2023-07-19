import pygame
import os
import random

# Initialize pygame modules
pygame.init()

# Window dimensions
width, height = 255, 275
WIN = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper!!!")

# Grid settings
grid_width, grid_height = 20, 20
grid_num_cols, grid_num_rows = 10, 10
mines = 20
margin = 5
lower_grid = 20

# Game settings
FPS = 10

# Fonts and Colors
timer_font = pygame.font.SysFont("comicsans", 15)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Sounds
MINE_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Bomb.mp3'))

# Fonts
Mines_FONT = pygame.font.SysFont("comicsans", 15)
Winner_FONT = pygame.font.SysFont("comicsans", 20)
Mine_count_font = pygame.font.Font('freesansbold.ttf', 20)

# Import Flag and Mine images
Flag_Image = pygame.image.load(os.path.join('Assets', 'Flag.png'))
Flag = pygame.transform.scale(Flag_Image, (grid_width, grid_height))

Mine_Image = pygame.image.load(os.path.join('Assets', 'Mine.png'))
Mine = pygame.transform.scale(Mine_Image, (grid_width - 4, grid_height - 4))

# Creating dictionary for bombs and count of bombs around grid
def create_layout(grid_tracker, mine_locations):
    miness = set()
    for _ in range(mines):
        row, column = random.randint(0, 9), random.randint(0, 9)
        mine_locations[row][column] = 'mine'
        miness.add((row, column))
        grid_tracker[row][column] = 'mine'

    for row in range(10):
        for column in range(10):
            if (row, column) in miness:
                continue

            total = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_row = row + dx
                    new_column = column + dy

                    if (
                        0 <= new_row < 10 and
                        0 <= new_column < 10 and
                        (new_row, new_column) in miness
                    ):
                        total += 1

            mine_locations[row][column] = total if total > 0 else ''

def check_adjacent(mine_locations, grid_locations, row, column):
    additional_check = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_row = row + dx
            new_column = column + dy

            if (
                0 <= new_row < 10 and
                0 <= new_column < 10 and
                mine_locations[new_row][new_column] == '' and
                grid_locations[new_row][new_column] != 'cleared'
            ):
                grid_locations[new_row][new_column] = 'cleared'
                if mine_locations[new_row][new_column] == '':
                    for dx_inner in [-1, 0, 1]:
                        for dy_inner in [-1, 0, 1]:
                            if dx_inner == 0 and dy_inner == 0:
                                continue
                            inner_row = new_row + dx_inner
                            inner_column = new_column + dy_inner
                            if (
                                0 <= inner_row < 10 and
                                0 <= inner_column < 10 and
                                grid_locations[inner_row][inner_column] != 'cleared'
                            ):
                                grid_locations[inner_row][inner_column] = 'cleared'
                                additional_check.append([inner_row, inner_column])

    for x in additional_check:
        check_adjacent(mine_locations, grid_locations, x[0], x[1])


def display_window(grid, elapsed_time, mines_left):
    WIN.fill(BLACK)
    for x in grid:
        if x[2] == "Grey":
            WIN.blit(Flag, (x[0], x[1]))
        elif x[2] == 'Mine':
            WIN.blit(Mine, (x[0] + 2, x[1] + 2))
        elif x[2] == 'fatal_mine':
            pygame.draw.rect(WIN, RED, [x[0], x[1], grid_width, grid_height])
            WIN.blit(Mine, (x[0] + 2, x[1] + 2))
        elif x[2] == RED:
            pygame.draw.rect(WIN, x[2], [x[0], x[1], grid_width, grid_height])
            Mine_number = Mine_count_font.render(str(x[3]), 1, WHITE)
            WIN.blit(Mine_number, (x[0] + 5, x[1] + 2))
        else:
            pygame.draw.rect(WIN, x[2], [x[0], x[1], grid_width, grid_height])
            if x[2] == BLUE and x[3] != '':
                Mine_number = Mine_count_font.render(str(x[3]), 1, WHITE)
                WIN.blit(Mine_number, (x[0] + 5, x[1] + 2))

    mines_marked_font = Mines_FONT.render("Mines left: " + str(mines_left), 1, WHITE)
    WIN.blit(mines_marked_font, (5, 0))
    timer_text = timer_font.render("Time: " + str(elapsed_time), 1, WHITE)
    WIN.blit(timer_text, (185, 0))
    pygame.display.update()

def winner():
    draw_text_line1 = Winner_FONT.render("You navigated the", 1, WHITE)
    draw_text_line2 = Winner_FONT.render("midfield successfully!!", 1, WHITE)

    line1_x = width / 2 - draw_text_line1.get_width() / 2
    line1_y = height / 2 - draw_text_line1.get_height() - draw_text_line2.get_height() // 2
    line2_x = width / 2 - draw_text_line2.get_width() / 2
    line2_y = height / 2 - draw_text_line2.get_height() // 2

    WIN.blit(draw_text_line1, (line1_x, line1_y))
    WIN.blit(draw_text_line2, (line2_x, line2_y))

    pygame.display.update()
    pygame.time.delay(5000)

start_time = 0

def main():
    global start_time
    if start_time == 0:
        start_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    run = True
    end_game = False
    grid_tracker = [[0 for _ in range(grid_num_cols)] for _ in range(grid_num_cols)]
    mine_locations = [[0 for _ in range(grid_num_cols)] for _ in range(grid_num_cols)]
    create_layout(grid_tracker, mine_locations)

    grid = []
    mines_marked = 0
    eliminated_squares = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            action = event.button
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (grid_width + margin)
            row = (pos[1] - lower_grid) // (grid_height + margin)

            if action == 1:
                if mine_locations[row][column] == 'mine':
                    grid_tracker[row][column] = 'fatal_mine'
                    end_game = True
                    MINE_HIT_SOUND.play()
                else:
                    grid_tracker[row][column] = 1
                    eliminated_squares += 1
                    check_adjacent(mine_locations, grid_tracker, row, column)
            elif action == 3:
                if grid_tracker[row][column] == 2:
                    grid_tracker[row][column] = 0
                    mines_marked -= 1
                elif grid_tracker[row][column] == 0:
                    grid_tracker[row][column] = 2
                    mines_marked += 1

        def grid_creation(grid_tracker, grid, mine_locations, eliminated_squares):
            eliminated_squares = 0
            if end_game:
                for row in range(grid_num_rows):
                    for column in range(grid_num_cols):
                        if grid_tracker[row][column] == 'fatal_mine':
                            grid.append(
                                ((margin + grid_width) * column + margin,
                                 (margin + grid_height) * row + margin + lower_grid,
                                 "fatal_mine",
                                 ""))
                        elif mine_locations[row][column] == 'mine':
                            grid.append(
                                ((margin + grid_width) * column + margin,
                                 (margin + grid_height) * row + margin + lower_grid,
                                 "Mine",
                                 ""))
            else:
                for row in range(grid_num_rows):
                    for column in range(grid_num_cols):
                        if grid_tracker[row][column] == 1 or grid_tracker[row][column] == 'cleared':
                            eliminated_squares += 1
                            grid.append(
                                ((margin + grid_width) * column + margin,
                                 (margin + grid_height) * row + margin + lower_grid,
                                 RED,
                                 mine_locations[row][column]))
                        elif grid_tracker[row][column] == 2:
                            grid.append(
                                ((margin + grid_width) * column + margin,
                                 (margin + grid_height) * row + margin + lower_grid,
                                 "Grey",
                                 ""))
                        else:
                            grid.append(
                                ((margin + grid_width) * column + margin,
                                 (margin + grid_height) * row + margin + lower_grid,
                                 BLUE,
                                 ""))
            return grid

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        display_window(grid_creation(grid_tracker, grid, mine_locations, eliminated_squares),
                       elapsed_time,
                       mines - mines_marked)

        if end_game:
            pygame.time.delay(4000)
            eliminated_squares = 0
            mines_marked = 0
            end_game = False
            start_time = 0  # Reset the start time
            main()

        if mines - mines_marked == 0:
            winner()
            main()

if __name__ == "__main__":
    main()
