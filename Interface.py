import pygame
import numpy as np
import time
pygame.init() 

screenSize = 600

gridSpacing = 50

marginSize = (screenSize - 9 * gridSpacing) / 2

lineLength = screenSize - 2 * marginSize

screen = pygame.display.set_mode((screenSize,screenSize))
pygame.display.set_caption("Sudoku!")
 
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
pale = (252, 217, 192)
turqoise = (189, 242, 216)

myFont = pygame.font.SysFont("Arial", 40, False)
winFont = pygame.font.SysFont("Arial", 100, True)

grid = np.array([[0,0,0,1,0,5,0,0,0],
                [0,0,1,4,0,8,9,0,0],
                [0,7,0,0,3,0,0,4,0],
                [0,0,6,0,0,0,4,0,0],
                [2,0,0,0,0,0,0,0,1],
                [0,0,0,6,9,3,0,0,0],
                [0,8,2,3,0,6,7,9,0],
                [0,9,5,0,0,0,8,1,0],
                [0,0,3,9,0,1,6,0,0]]) #this is for storing the actual numerical data

solved_grid = grid 

square = [[0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0]]  #this is for storing all the squares in the grid 

fixed =  [[0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0]] #this is for permanently storing whether a value was originally known or not

for i in range(9):
    for j in range(9):
        square[j][i] = pygame.Rect(marginSize + i * gridSpacing,marginSize + j * gridSpacing,gridSpacing,gridSpacing) 
        if grid[j][i] == 0: 
            fixed[j][i] = 0
        else: 
            fixed[j][i] = 1
            
def isValid(x, y, n): 
    global grid
    for i in range(9): 
        if grid[y][i] == n and i != x: 
            return False 
    for j in range(9): 
        if grid[j][x] == n and j != y:
            return False 
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3): 
        for j in range(3): 
            if grid[y0 + j][x0 + i] == n and (x0 + i != x and y0 + j != y): 
                return False 
    return True 
                
def solve(): 
    for i in range(9): 
        for j in range(9): 
            for n in range(1,10): 
                if solved_grid[j][i] == 0 and fixed[j][i] == 0: 
                    if isValid(i, j, n): 
                        solved_grid[j][i] = n
                        solve() 
                        solved_grid[j][i] = 0
    return solved_grid 
            
    
def click(pos):
    for i in range(9): 
        for j in range(9): 
            if square[j][i].collidepoint(pos): 
                return (i, j)
    else: 
        return None 

    
def gameLoop(): 
    global grid
    global square
    
    run = True
    active = False 
    pos = (0,0)
    
    while run:    
            
        screen.fill(white)
        key = 0
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False
            if event.type == pygame.KEYDOWN: 
                if fixed[pos[1]][pos[0]] == 0:
                    if event.key == pygame.K_1: 
                        grid[pos[1]][pos[0]] = 1
                    elif event.key == pygame.K_2: 
                        grid[pos[1]][pos[0]] = 2
                    elif event.key == pygame.K_3: 
                        grid[pos[1]][pos[0]] = 3
                    elif event.key == pygame.K_4: 
                        grid[pos[1]][pos[0]] = 4
                    elif event.key == pygame.K_5: 
                        grid[pos[1]][pos[0]] = 5
                    elif event.key == pygame.K_6: 
                        grid[pos[1]][pos[0]] = 6
                    elif event.key == pygame.K_7: 
                        grid[pos[1]][pos[0]] = 7
                    elif event.key == pygame.K_8: 
                        grid[pos[1]][pos[0]] = 8
                    elif event.key == pygame.K_9: 
                        grid[pos[1]][pos[0]] = 9
                    else: 
                        grid[pos[1]][pos[0]] = 0
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos = click(pygame.mouse.get_pos())
        
        for i in range(9): 
            for j in range(9):
                leftSide = marginSize + i * gridSpacing
                upperSide = marginSize + j * gridSpacing
                if square[j][i].collidepoint(pygame.mouse.get_pos()): 
                    if i % 3 == 0 and j % 3 == 0: 
                        pygame.draw.rect(screen,pale,(leftSide + 4, marginSize + 4, gridSpacing - 4, lineLength - 4))
                        pygame.draw.rect(screen,pale,(marginSize + 4, upperSide + 4, lineLength - 4, gridSpacing - 4))
                        pygame.draw.rect(screen,turqoise,(leftSide + 4, upperSide + 4, gridSpacing - 4, gridSpacing - 4))
                    elif i % 3 == 0:
                        pygame.draw.rect(screen,pale,(leftSide + 4, marginSize + 4, gridSpacing - 2, lineLength - 4))
                        pygame.draw.rect(screen,pale,(marginSize + 4, upperSide + 2, lineLength - 4, gridSpacing - 2))
                        pygame.draw.rect(screen,turqoise,(leftSide + 4, upperSide + 2, gridSpacing - 4, gridSpacing - 2))
                    elif j % 3 == 0: 
                        pygame.draw.rect(screen,pale,(leftSide + 2, marginSize + 4, gridSpacing - 2, lineLength - 4))
                        pygame.draw.rect(screen,pale,(marginSize + 4, upperSide + 2, lineLength - 4, gridSpacing - 2))
                        pygame.draw.rect(screen,turqoise,(leftSide + 2, upperSide + 4, gridSpacing - 2, gridSpacing - 4))
                    else: 
                        pygame.draw.rect(screen,pale,(leftSide + 2, marginSize + 4, gridSpacing - 2, lineLength - 4))
                        pygame.draw.rect(screen,pale,(marginSize + 4, upperSide + 2, lineLength - 4, gridSpacing - 2))
                        pygame.draw.rect(screen,turqoise,(leftSide + 2, upperSide + 2, gridSpacing - 2, gridSpacing - 2))
                        
        for i in range(10): 
            if i % 3 == 0: 
                thickness = 4
            else: 
                thickness = 2
            pygame.draw.rect(screen,(black),(marginSize + i * gridSpacing, marginSize, thickness, lineLength))
            pygame.draw.rect(screen,(black),(marginSize, marginSize + i * gridSpacing, lineLength, thickness))                
                        
        for i in range(9):
            for j in range(9):
                color = white
                leftSide = marginSize + i * gridSpacing
                upperSide = marginSize + j * gridSpacing
                if grid[j][i] != 0: 
                    if fixed[j][i] == 1:
                        color = black
                    elif isValid(i, j, grid[j][i]) == True: 
                        color = blue
                    else: 
                        color = red 
                    text = myFont.render("{}".format(grid[j][i]), 1, color)
                    screen.blit(text, (leftSide + 15, upperSide + 5))
        
        
                    
                    
        
                
        pygame.display.update()         
                
gameLoop() 
pygame.quit() 
