import pygame
import os
pygame.init()

WIDTH, HEIGHT = (400, 400)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

FPS = 30
WHITE = (255,255,255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)

game_outcome_font = pygame.font.SysFont("comicsans", 50)

#Grid squares
GRID_WIDTH = (WIDTH)/3
GRID_HEIGHT = (HEIGHT)/3

#X and O Images
WIDTH_ADJUSTMENT = 20
HEIGHT_ADJUSTMENT =20
WIDTH_SIZE = GRID_WIDTH - WIDTH_ADJUSTMENT
HEIGHT_SIZE = GRID_HEIGHT - HEIGHT_ADJUSTMENT

x_image = pygame.image.load(os.path.join('Assets', 'x.png'))
x_scaled_image = pygame.transform.scale(x_image, (WIDTH_SIZE, HEIGHT_SIZE))

o_image = pygame.image.load(os.path.join('Assets', 'o.png'))
o_scaled_image = pygame.transform.scale(o_image, (WIDTH_SIZE, HEIGHT_SIZE))

def display_window(Grid):
    WIN.fill(WHITE)

    pygame.draw.rect(WIN,BLACK,[0,GRID_HEIGHT-2.5,400,5])
    pygame.draw.rect(WIN,BLACK,[0,GRID_HEIGHT*2-2.5,400,5])
    pygame.draw.rect(WIN,BLACK,[GRID_WIDTH-2.5,0,5,400])
    pygame.draw.rect(WIN,BLACK,[GRID_WIDTH*2-2.5,0,5,400])
    for square in Grid:
        if square[2]=='x':
            WIN.blit(x_scaled_image,(square[0]+WIDTH_ADJUSTMENT/2,square[1]+HEIGHT_ADJUSTMENT/2))
        elif square[2]=='o':
            WIN.blit(o_scaled_image,(square[0]+WIDTH_ADJUSTMENT/2,square[1]+HEIGHT_ADJUSTMENT/2))
        else:
            continue    

    pygame.display.update()

def check_outcome(grid_tracker):
    if grid_tracker[0][0]!= 0 and grid_tracker[0][0]==grid_tracker[0][1] and grid_tracker[0][0]==grid_tracker[0][2]: 
        return grid_tracker[0][0], True
    elif grid_tracker[1][0]!= 0 and grid_tracker[1][0]==grid_tracker[1][1] and grid_tracker[1][0]==grid_tracker[1][2]: 
        return grid_tracker[1][0], True
    elif grid_tracker[2][0]!= 0 and grid_tracker[2][0]==grid_tracker[2][1] and grid_tracker[2][0]==grid_tracker[2][2]: 
        return grid_tracker[2][0], True
    elif grid_tracker[0][0]!= 0 and grid_tracker[0][0]==grid_tracker[1][0] and grid_tracker[0][0]==grid_tracker[2][0]: 
        return grid_tracker[0][0], True
    elif grid_tracker[0][1]!= 0 and grid_tracker[0][1]==grid_tracker[1][1] and grid_tracker[0][1]==grid_tracker[2][1]: 
        return grid_tracker[0][1], True
    elif grid_tracker[0][2]!= 0 and grid_tracker[0][2]==grid_tracker[1][2] and grid_tracker[0][2]==grid_tracker[2][2]: 
        return grid_tracker[0][2], True
    elif  grid_tracker[0][0]!= 0 and grid_tracker[0][0]==grid_tracker[1][1] and grid_tracker[0][0]==grid_tracker[2][2]: 
        return grid_tracker[0][0], True
    elif  grid_tracker[2][0]!= 0 and grid_tracker[2][0]==grid_tracker[1][1] and grid_tracker[1][1]==grid_tracker[0][2]: 
        return grid_tracker[0][2], True

    else:
        return None, False

def game_outcome(outcome):
    final = "X Wins!!!" if outcome=='x' else 'O Wins!!!' if outcome=='o' else "Draw!!!!"
    draw_text_line1 = game_outcome_font.render(final, 1, BLUE)

    line1_x = WIDTH / 2 - draw_text_line1.get_width() / 2
    line1_y = HEIGHT / 2 - draw_text_line1.get_height() / 2
    
    WIN.blit(draw_text_line1, (line1_x, line1_y))
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    Grid = []
    move = 'x'
    game_state = False
    grid_tracker = [[0 for _ in range(3)] for _ in range(3)]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            y = int(pos[0] // GRID_HEIGHT)
            x = int(pos[1] // GRID_WIDTH)
            if grid_tracker[x][y]=='x' or grid_tracker[x][y]=='o':
                continue
            else:
                grid_tracker[x][y]=move
                if move=='x':
                    move='o'
                else:
                    move='x'
        
        for row in range(3):
            for column in range(3):
                if grid_tracker[row][column]=='x':
                    Grid.append((GRID_WIDTH*column,GRID_HEIGHT*row,'x'))
                elif grid_tracker[row][column]=='o':
                    Grid.append((GRID_WIDTH*column,GRID_HEIGHT*row,'o'))
                else:
                    Grid.append((GRID_WIDTH*column,GRID_HEIGHT*row,'empty'))

        display_window(Grid)
        outcome, game_state = check_outcome(grid_tracker)
        if game_state:
            game_outcome(outcome)
            pygame.time.delay(4000)
            Grid = 0
            main()
        if (grid_tracker[0].count(0) + grid_tracker[1].count(0) + 
            grid_tracker[2].count(0))==0:

            game_outcome("draw")
            pygame.time.delay(4000)
            Grid = 0
            main()

    print(grid_tracker)
if __name__ == "__main__":
    main()