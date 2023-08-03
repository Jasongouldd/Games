import pygame
import numpy as np

class board:

    def __init__(self,WIN, WIDTH, HEIGHT, board_layout):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        
        self.margin = 5
        self.grid_width = (self.WIDTH - self.margin) // 8
        self.grid_height = (self.HEIGHT - self.margin) // 8
        
        self.WIN = WIN

        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.PURPLE = (221,160,221)

        winner_font = pygame.font.SysFont("comicsans", 40)
        self.winner_font = winner_font



        self.board_layout = board_layout
        self.change_squares = []

        self.starting_position = [[2,3,3],[1,4,3],[1,3,4],[2,4,4]]
        self.potential_move_board = np.full((8,8),0)

    def draw_board(self):
        self.WIN.fill(self.GREEN)

        for num in range(1,8):
            pygame.draw.rect(self.WIN,self.BLACK,[0,self.grid_height*num,self.WIDTH,self.margin])
            pygame.draw.rect(self.WIN,self.BLACK,[self.grid_width*num,0,self.margin,self.HEIGHT])
        
        for sq in self.starting_position:
            if sq[0]==1:
                self.board_layout[sq[1]][sq[2]] = 1
                pygame.draw.circle(self.WIN, self.WHITE, ((sq[1]*self.grid_width)+((self.grid_width + self.margin)//2), 
                                                     (sq[2]*self.grid_height)+((self.grid_height + self.margin)//2)), 
                                                     (self.grid_width-20)//2, (self.grid_height-20)//2)
            
            else:
                self.board_layout[sq[1]][sq[2]] = 2
                pygame.draw.circle(self.WIN, self.BLACK, ((sq[1]*self.grid_width)+((self.grid_width + self.margin)//2), 
                                                     (sq[2]*self.grid_height)+((self.grid_height + self.margin)//2)), 
                                                     (self.grid_width-20)//2, (self.grid_height-20)//2)    


        pygame.display.update()


    def display_window(self):
        
        for square in self.change_squares:

            if square[0] == 1:
                self.board_layout[square[1]][square[2]] = 1 
                pygame.draw.circle(self.WIN, self.WHITE, ((square[1]*self.grid_width)+((self.grid_width + self.margin)//2)
                                                          , (square[2]*self.grid_height)+((self.grid_height + self.margin)//2)),
                                                            (self.grid_width-20)//2, (self.grid_height-20)//2)
            elif square[0]==2:
                self.board_layout[square[1]][square[2]] = 2 
                pygame.draw.circle(self.WIN, self.BLACK, ((square[1]*self.grid_width)+((self.grid_width + self.margin)//2)
                                                          , (square[2]*self.grid_height)+((self.grid_height + self.margin)//2)),
                                                            (self.grid_width-20)//2, (self.grid_height-20)//2)
            else:
                continue
        
        self.change_squares = []
        pygame.display.update()

    def handle_click(self,x, y,Turn):
        column = x // self.grid_width
        row = y // self.grid_height
        
        if Turn == 'White':
            self.change_squares = self.check_valid_moves(column, row, Turn)
            if len(self.change_squares) > 0:
                Turn = 'Black'
                return Turn
            return Turn
        elif Turn == 'Black':
            self.change_squares = self.check_valid_moves(column, row, Turn)
            if len(self.change_squares) > 0:
                Turn = 'White'
                return Turn
            return Turn

    def check_valid_moves(self,column, row, Turn):
        square_list = []
        current_color = 1 if Turn=='White' else 2
        op_color = 2 if Turn =='White' else 1
        
        if self.board_layout[column][row]==1 or self.board_layout[column][row]==2:
            return []
        else:
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if ((column + x) < 0) or ((column + x) > 7) or ((row + y) < 0) or ((row + y) > 7):
                        continue
                    elif x==0 and y==0:
                        continue
                    elif self.board_layout[column+x][row+y]==current_color:
                        continue
                    elif self.board_layout[column+x][row+y]==0:
                        continue
                    else:
                        flag = True
                        step = 1
                        step_list = []

                        while flag:

                            if ((column + x + step*x) < 0) or ((column + step*x) > 7) or ((row + step*y) < 0) or ((row + step*y) > 7):
                                flag = False

                            elif self.board_layout[column + x*step][row + y*step] == op_color:
                                step_list.append([current_color, column + x*step, row + y*step])
                                step += 1

                            elif self.board_layout[ column +x*step][ row + y*step] == current_color:
                                flag = False
                                square_list.extend(step_list)

                            else:  
                                flag = False
        if len(square_list) > 0:
            square_list.append([current_color, column, row])
            return square_list
        else:
            return []               

    def potential_moves(self, Turn):
        indices = np.where(self.board_layout == 0)
        row_col_combo = np.transpose(indices)

        potential_moves = []
        for cord in row_col_combo:
            add = self. check_valid_moves(cord[0], cord[1], Turn)
            if not add:
                continue
            potential_moves.extend(add)

        return potential_moves


    def winner(self):
        winner = 'White' if np.count_nonzero(self.board_layout == 1) > np.count_nonzero(self.board_layout == 2) else 'Black'

        end_font = self.winner_font.render(f"{winner} Wins!!!!!", 1, self.WHITE)
        line1_x = self.WIDTH / 2 - end_font.get_width() / 2
        line1_y = self.HEIGHT / 2 - end_font.get_height() /2


        self.WIN.fill(self.PURPLE)
        self.WIN.blit(end_font, (line1_x, line1_y))

        pygame.display.update()
        pygame.time.delay(4000)

    def show_potential_moves(self, potential_moves, Turn):
        
        color = self.WHITE if Turn == 'White' else self.BLACK
        for square in potential_moves:
            if self.board_layout[square[1]][square[2]] == 0:
                pygame.draw.circle(self.WIN, color, ((square[1]*self.grid_width)+((self.grid_width + self.margin)//2)
                                                            , (square[2]*self.grid_height)+((self.grid_height + self.margin)//2)),
                                                            (self.grid_width-20)//2, 7)

        pygame.display.update()

    def remove_potential_moves(self, potential_moves):
        
        for square in potential_moves:
            if self.board_layout[square[1]][square[2]] == 0:
                pygame.draw.circle(self.WIN, self.GREEN, ((square[1]*self.grid_width)+((self.grid_width + self.margin)//2)
                                                            , (square[2]*self.grid_height)+((self.grid_height + self.margin)//2)),
                                                            (self.grid_width-20)//2, 7)

        pygame.display.update()
    