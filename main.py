#Schelling's Segregation Model with Python
#Author: bozb
#Date: 8.05.2021
#----------------------
import pygame, os, time
import numpy as np

#Declaring variables.
#Game loop delay.
DELAY = 0.1
#These constants should be sum to 1.
EMPTY_CELL_PROBABILITY=0.2
RED_CELL_PROBABILITY=0.4
BLUE_CELL_PROBABILITY=0.4
#-----------------------
#Tolerance constant should be between 1-8 (Low Tolerance to the Opposite Color - High Tolerance to the Opposite Color)
TOLERANCE = 2
#-----------------------
#Main board variables with Numpy for Cellular Automata implementation.
#Two board will change throughout the simulation.
board = np.random.choice([0,1,2],(50,50),p=[EMPTY_CELL_PROBABILITY,RED_CELL_PROBABILITY,BLUE_CELL_PROBABILITY])
#TO GET UNIFORM DISTRIBUTION OF CELLS USE THIS -> board = np.random.randint(3,size=(50,50))
nextboard = np.full((50,50),0)

#Setting up the PyGame.
pygame.init()
screen = pygame.display.set_mode((500,500))

#This function checks every cell on the board if the cell is happy about its surroundings.
#If it is happy then the function will move to the next living cell
#If it is not happy then it will move to the empty cell where it can be happy
def checkIfHappy():
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == 1:
                neighbours=n_check(x,y,board,2)
                if neighbours > TOLERANCE:
                    searchEmpty(1,2)
                else:
                    nextboard[x][y]=1
            if j == 2:
                neighbours=n_check(x,y,board,1)
                if neighbours > TOLERANCE:
                    searchEmpty(2,1)
                else:
                    nextboard[x][y]=2

#The function that checks a cell's neighbours and returns sum of the opposite color neighbours.
#This will be used to check if the sum of the neighbours exceed the tolerance threshold.
def n_check(x_check, y_check, boardToCheck, group):
    sumOfN = 0 
    for i, j in ( 
            (x_check - 1, y_check), (x_check + 1, y_check), (x_check, y_check - 1),
            (x_check, y_check + 1), (x_check - 1, y_check - 1), (x_check - 1, y_check + 1),
            (x_check + 1, y_check - 1), (x_check + 1, y_check + 1)):
        if not (0 <= i < len(boardToCheck) and 0 <= j < len(boardToCheck[i])): 
            continue
        if boardToCheck[i][j]==group: 
            sumOfN+=1 
    return sumOfN

#The function that searches empty cells for other cells to move in.
def searchEmpty(who, freeOfWhom):
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j == 0:
                n = n_check(x, y, board, freeOfWhom)
                if n > 1:
                    continue
                else:
                    transX = x
                    transY = y
                    board[x][y]=5
                    nextboard[x][y]=who

#Displaying the game board on the screen.
def displayBoard():
    for x, i in enumerate(nextboard):
        for y, j in enumerate(i):
            if j == 1:
                pygame.draw.rect(screen,(255,0,0),[y*10,x*10,9,9])
            if j == 2:
                pygame.draw.rect(screen,(0,0,255),[y*10,x*10,9,9])
            if j == 0:
                pygame.draw.rect(screen,(255,255,255),[y*10,x*10,9,9])

#Main game loop.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    checkIfHappy()
    displayBoard()
    board=np.copy(nextboard)
    nextboard=np.full((50,50),0)
    pygame.display.update()
    time.sleep(DELAY)
    screen.fill((0,0,0))
    
    