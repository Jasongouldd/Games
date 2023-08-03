import pygame
import numpy as np
from board import board


pygame.init()

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")
board_layout = np.full((8,8),0)
board = board(WIN,WIDTH, HEIGHT, board_layout)

FPS = 10

def main():

    run = True
    clock = pygame.time.Clock()
    Turn = 'White'
    board.draw_board()
    potential_moves = []

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            Turn = board.handle_click(pos[0], pos[1], Turn)

            board.display_window()


            board.remove_potential_moves(potential_moves)  
            potential_moves = board.potential_moves(Turn)

            if len(potential_moves)==0:
                board.winner()
            
            board.show_potential_moves(potential_moves, Turn)


    pygame.quit()

if __name__ == "__main__":
    main()