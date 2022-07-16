from typing import Collection
import numpy as np
import pygame
import sys
import math

from pygame import draw


ROW_COUNT = 6

COLUMN_COUNT = 7



# define function for drawing the board
def draw_board(board):
    # iterate through each cols and rows
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BACK_COLOR,(c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            
            pygame.draw.circle(screen, CIRC_COLOR,(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+(SQUARESIZE/2))), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if(board[r][c]==1):
                pygame.draw.circle(screen, PLAYER1_COLOR,(int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+(SQUARESIZE/2))), RADIUS)

            elif(board[r][c]==2):
                pygame.draw.circle(screen, PLAYER2_COLOR,(int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    #  creates a matrix of sixe 6*7

    return board

def drop_piece(board,row,col,piece):
    board[row][col]=piece

def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if (board[r][col]==0):
            return r
    #  check in which row given col is free 


def is_valid_input(board, col):
    return board[ROW_COUNT-1][col] == 0

def print_board(board):
    print(np.flip(board,0))
    # printing the matrix upside down so the user first get to drop piece from the bottom rows 

def winning_move(board,piece):
    # check horizontal row for win
    # to check horizontal row number will be same 
    # but column no will vary
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c]== piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece :
                return True

    # verical locations for win
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT):
            if board[r][c]== piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece :
                return True

    # check for positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]== piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece :
                return True

    # check for negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c]== piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece :
                return True


# initialize pygame module by init function
pygame.init()

# define window size
SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
BACK_COLOR = "#EDFF7A"
CIRC_COLOR = "#30638E"
PLAYER1_COLOR = "#512500"
PLAYER2_COLOR = "#F26419"
RADIUS = int(SQUARESIZE/2 -15)

myfont = pygame.font.SysFont("monospace", 75)
game_over = False
board = create_board()
turn =0

draw_board(board)
pygame.display.update()

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,CIRC_COLOR, (0,0,width,SQUARESIZE))
            posx = event.pos[0]
            if turn ==0:
                pygame.draw.circle(screen, PLAYER1_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, PLAYER2_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

            #  get the position where it is clicked 


            # ask for player 1 to input
            if turn == 0:
                posx = event.pos[0]  # between 0 and 700
                col = int(math.floor(posx/SQUARESIZE))
                #  check for valid input
                if is_valid_input(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row,col,1)
                    #  piece is 1 for player 1

                    if winning_move(board, 1):
                        pygame.draw.rect(screen,CIRC_COLOR, (0,0,width,SQUARESIZE))
                        label = myfont.render("Player 1 wins!!", 1,PLAYER1_COLOR)
                        screen.blit(label,(40,10))
                        game_over = True
                    

            
            # ask for player 2 to input
            else:
                posx = event.pos[0]  # between 0 and 700
                col = int(math.floor(posx/SQUARESIZE)) # x coordinate / squaresize gives col no

                #  check for valid input
                if is_valid_input(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row,col,2)
                    #  piece is 1 for player 1

                    if winning_move(board, 2):
                        pygame.draw.rect(screen,CIRC_COLOR, (0,0,width,SQUARESIZE))
                        label = myfont.render("Player 2 wins!!", 1,PLAYER2_COLOR)
                        screen.blit(label,(40,10))
                        game_over = True
            turn += 1
            turn = turn%2
            print_board(board)
            draw_board(board)

            if game_over:
                pygame.time.wait(3000)
    
print("*** Game Over ***")