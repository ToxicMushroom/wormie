# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import pygame
import random
import sys

from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD1 = 0  # syntactic sugar: index of the worm's head
HEAD2 = 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy edit by TSM')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    blub1 = False
    blub2 = False
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords1 = [{'x': startx, 'y': starty},
                   {'x': startx - 1, 'y': starty},
                   {'x': startx - 2, 'y': starty}]
    wormCoords2 = [{'x': startx, 'y': starty - 2},
                   {'x': startx - 1, 'y': starty - 2},
                   {'x': startx - 2, 'y': starty - 2}]
    direction1 = RIGHT
    direction2 = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_a) and direction1 != RIGHT:  # snake 1
                    direction1 = LEFT
                elif (event.key == K_d) and direction1 != LEFT:
                    direction1 = RIGHT
                elif (event.key == K_w) and direction1 != DOWN:
                    direction1 = UP
                elif (event.key == K_s) and direction1 != UP:
                    direction1 = DOWN
                if (event.key == K_LEFT) and direction2 != RIGHT:  # snake 2
                    direction2 = LEFT
                elif (event.key == K_RIGHT) and direction2 != LEFT:
                    direction2 = RIGHT
                elif (event.key == K_UP) and direction2 != DOWN:
                    direction2 = UP
                elif (event.key == K_DOWN) and direction2 != UP:
                    direction2 = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm1 has hit itself or the edge
        if wormCoords1[HEAD1]['x'] == -1 or wormCoords1[HEAD1]['x'] == CELLWIDTH or wormCoords1[HEAD1]['y'] == -1 or \
                wormCoords1[HEAD1]['y'] == CELLHEIGHT:
            if direction1 == UP:
                newHead1 = {'x': wormCoords1[HEAD1]['x'], 'y': CELLHEIGHT - 1}
            elif direction1 == DOWN:
                newHead1 = {'x': wormCoords1[HEAD1]['x'], 'y': 0}
            elif direction1 == LEFT:
                newHead1 = {'x': CELLWIDTH - 1, 'y': wormCoords1[HEAD1]['y']}
            elif direction1 == RIGHT:
                newHead1 = {'x': 0, 'y': wormCoords1[HEAD1]['y']}
            blub1 = True

        for wormBody1 in wormCoords1[1:]:
            if wormBody1['x'] == wormCoords1[HEAD1]['x'] and wormBody1['y'] == wormCoords1[HEAD1]['y']:
                return  # game over

        # check if worm1 has eaten an apply
        if wormCoords1[HEAD1]['x'] == apple['x'] and wormCoords1[HEAD1]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords1[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if not blub1:
            if direction1 == UP:
                newHead1 = {'x': wormCoords1[HEAD1]['x'], 'y': wormCoords1[HEAD1]['y'] - 1}
            elif direction1 == DOWN:
                newHead1 = {'x': wormCoords1[HEAD1]['x'], 'y': wormCoords1[HEAD1]['y'] + 1}
            elif direction1 == LEFT:
                newHead1 = {'x': wormCoords1[HEAD1]['x'] - 1, 'y': wormCoords1[HEAD1]['y']}
            elif direction1 == RIGHT:
                newHead1 = {'x': wormCoords1[HEAD1]['x'] + 1, 'y': wormCoords1[HEAD1]['y']}
        else:
            blub1 = False

        if wormCoords2[HEAD2]['x'] == -1 or wormCoords2[HEAD2]['x'] == CELLWIDTH or wormCoords2[HEAD2]['y'] == -1 or \
                wormCoords2[HEAD2]['y'] == CELLHEIGHT:
            if direction2 == UP:
                newHead2 = {'x': wormCoords2[HEAD2]['x'], 'y': CELLHEIGHT - 1}
            elif direction2 == DOWN:
                newHead2 = {'x': wormCoords2[HEAD2]['x'], 'y': 0}
            elif direction2 == LEFT:
                newHead2 = {'x': CELLWIDTH - 1, 'y': wormCoords2[HEAD2]['y']}
            elif direction2 == RIGHT:
                newHead2 = {'x': 0, 'y': wormCoords2[HEAD2]['y']}
            blub2 = True

        for wormBody2 in wormCoords2[1:]:
            if wormBody2['x'] == wormCoords2[HEAD2]['x'] and wormBody2['y'] == wormCoords2[HEAD2]['y']:
                return  # game over

        # check if worm1 has eaten an apply
        if wormCoords2[HEAD2]['x'] == apple['x'] and wormCoords2[HEAD2]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords2[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if not blub2:
            if direction2 == UP:
                newHead2 = {'x': wormCoords2[HEAD2]['x'], 'y': wormCoords2[HEAD2]['y'] - 1}
            elif direction2 == DOWN:
                newHead2 = {'x': wormCoords2[HEAD2]['x'], 'y': wormCoords2[HEAD2]['y'] + 1}
            elif direction2 == LEFT:
                newHead2 = {'x': wormCoords2[HEAD2]['x'] - 1, 'y': wormCoords2[HEAD2]['y']}
            elif direction2 == RIGHT:
                newHead2 = {'x': wormCoords2[HEAD2]['x'] + 1, 'y': wormCoords2[HEAD2]['y']}
        else:
            blub2 = False

        wormCoords1.insert(0, newHead1)
        wormCoords2.insert(0, newHead2)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords1)
        drawWorm2(wormCoords2)
        drawApple(apple)
        drawScore(len(wormCoords1) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormie!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormie!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 1  # rotate by 3 degrees each frame
        degrees2 += 2  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Spel', True, WHITE)
    overSurf = gameOverFont.render('Gedaan', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                         wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                         wormInnerSegmentRect)


def drawWorm2(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                         wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                         wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
