"""this is main driver file. It will be responsible for handling user input
and displaying the current GameState object """
import pygame as p
from Engine import GameState

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT / DIMENSION  # squre size
MAX_FPS = 15
IMAGES = {}

'''
LOAD IMAGE FOR ALL PIECES
'''
def loadImages():
    pieces = ['bp', "bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) #Resizes the Surface to a new size, given as (width, height)
def drawGameState(screen, gs):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draw the rectangle
            piece = gs.board[r][c]
            if (piece != '--'):
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''MAIN DRIVER FOR CODE. UPDATING THE GRPHICS'''
def main():
    # pygame setup
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock() # doc (https://www.pygame.org/docs/ref/time.html)

    gs = GameState()  # game state
    loadImages()  # running this once before while loop
    running = True

    # poll for events
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(p.Color("white"))

        # RENDER YOUR GAME HERE
        drawGameState(screen, gs)
        clock.tick(MAX_FPS) #update the clock : never run at more than FPS

        # flip() the display to put your work on screen
        p.display.flip()


if __name__ == '__main__':
    main()