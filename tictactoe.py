import random
import sys
import pygame
import numpy as np
import copy

from constants import *

# Initialise pygame
#not importing for some reason had to hardcode


pygame.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI') # Title of the screen
screen.fill(BG_COLOR)

class Board:
    
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))  # Initialize the board
        self.empty_squares = self.squares #list of empty squares
        self.marked_squares = 0

    def final_state(self):
        """ 
        Returns 0 if there's no win yet
        Returns 1 if Player 1 wins
        Returns 2 if Player 2 wins
        """
        # Vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        
        # Horizontal wins (fixed)
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        # Descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]

        # Ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[2][0]

        # No win
        return 0
    

         
        

    def mark_square(self, row, col, player):
        self.squares[row][col] = player 
        self.marked_squares +=1 #increment marked squares 

    def empty_square(self, row, col):
        return self.squares[row][col] == 0  
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range (ROWS):
            for col in range(COLS):
                if self.empty_square(row , col):
                    empty_squares.append( (row,col) )

        return empty_squares            
    
    def is_full(self):
        return self.marked_squares == 9
    
    def is_empty(self):
        return self.marked_squares == 0
    
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    
    
    
    def minimax(self , board , maximising):
        # terminal cases
        case = board.final_state()
        # player 1 wins
        if case == 1:
            return 1 , None # eval and move
        
        #player 2 wins
        if case == 2:
            return -1 , None #minimising
        
        #draw 
        elif board.is_full():
          return 0 , None
        
        if maximising:
            max_eval = -100
            best_move = None
            empty_squares =board.get_empty_squares()

            for (row , col ) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row , col , 1 )
                eval = self.minimax(temp_board , False ) [0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row , col)

            return max_eval , best_move
            

        elif not maximising:
            min_eval =100
            best_move = None
            empty_squares =board.get_empty_squares()

            for (row , col ) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row , col , self.player )
                eval = self.minimax(temp_board , True ) [0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row , col)

            return min_eval , best_move
            

    
    
    
    def eval(self , main_board):
        if self.level == 0:
            #random
            eval = 'random'
            move = self.random_choice(main_board)
            

        else:
            #minimax algo
           eval , move =  self.minimax(main_board , False)
           print(f'AI has chosen to mark the square in pos {move} with an evaluation of {eval} ')


            

        return move



class Game:

    def __init__(self):
        self.board=Board()
        self.ai=AI()
        self.player=1
        self.game_mode = 'ai' 
        self.running = True
        self.show_lines()

    def make_move(self , row , col):
        self.board.mark_square(row,col,self.player)
        self.draw_fig(row,col)
        self.next_turn()

    
    def show_lines(self):
        #vertical
        pygame.draw.line(screen, LINE_COLOR ,(SQ_SIZE,0),(SQ_SIZE , HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR ,(WIDTH - SQ_SIZE,0),(WIDTH - SQ_SIZE , HEIGHT),LINE_WIDTH)

        #horizontal
        pygame.draw.line(screen, LINE_COLOR ,(0,SQ_SIZE),(WIDTH ,SQ_SIZE),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR ,(0 , HEIGHT - SQ_SIZE),(WIDTH , HEIGHT - SQ_SIZE),LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            #draw cross 
            #descending line
            start_desc = (col * SQ_SIZE + offset, row * SQ_SIZE + offset)
            end_desc = ( col * SQ_SIZE + SQ_SIZE - offset , row * SQ_SIZE + SQ_SIZE - offset)
            pygame.draw.line(screen , CROSS_COLOR , start_desc , end_desc , CROSS_WIDTH)

            #ascending line
            start_asc = (col * SQ_SIZE + offset , row * SQ_SIZE + SQ_SIZE - offset)
            end_asc = (col * SQ_SIZE + SQ_SIZE - offset , row * SQ_SIZE + offset)
            pygame.draw.line(screen , CROSS_COLOR , start_asc , end_asc , CROSS_WIDTH)
            
            
        elif self.player == 2:
            
            #draw circle
            center = (col * SQ_SIZE + SQ_SIZE // 2 , row * SQ_SIZE + SQ_SIZE // 2 )

            pygame.draw.circle(screen, CIRC_COLOR, center , RADIUS , CIRC_WIDTH)
              

    def next_turn(self):
      self.player= self.player % 2 +1 #switching player using modulus

    def is_over(self):
        return self.board.final_state() != 0 or self.board.is_full()
          



def main():
    #game object
    game = Game()
    board=game.board
    ai = game.ai
    #Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQ_SIZE
                col=pos[0] // SQ_SIZE
                
                if board.empty_square(row , col) and game.running:
                 game.make_move(row,col)

                 if game.is_over():
                     game.running = False

        if game.game_mode == "ai" and game.player == ai.player and game.running:
            pygame.display.update()

            # ai method
            row , col = ai.eval(board)
            game.make_move(row,col)
            if game.is_over():
                     game.running = False
            
                 
        pygame.display.update()            

main()

