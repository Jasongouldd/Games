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

    board.select_game_modes()

    bot = None
    flag = True

    while flag:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()


                bot, flag = board.select_game_mode(pos[0], pos[1])


    run = True
    clock = pygame.time.Clock()
    Turn = 'Black'
    board.draw_board()
    potential_moves = [[2, 3, 4], [2, 3, 5], [2, 4, 2], [2, 5, 3]]

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if Turn == 'Black' and bot:
            pygame.time.delay(1000)
            if bot == "Easy Bot":
                Turn = board.easy_bot(potential_moves, Turn)
            else:
                Turn = board.hard_bot(potential_moves, Turn)

            board.display_window()
            board.remove_potential_moves(potential_moves)




        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            Turn = board.handle_click(pos[0], pos[1], Turn)

            board.display_window()

            board.remove_potential_moves(potential_moves)

        potential_moves = board.potential_moves(Turn)

        if len(potential_moves)==0:
            Turn = "White" if Turn == "Black" else "Black"
            potential_moves = board.potential_moves(Turn)
            board.show_potential_moves(potential_moves, Turn)

            if len(potential_moves)==0:
                board.winner()

        board.show_potential_moves(potential_moves, Turn)


    pygame.quit()

if __name__ == "__main__":
    main()
