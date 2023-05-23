"""this is main driver file. It will be responsible for handling user input
and displaying the current GameState object """
import pygame as p
import pygame.draw

import Engine

p.init()
clock = pygame.time.Clock()
#565 579
counter, text =10, '10'.rjust(3)
tempCounter = counter
timeTurn = 1 #white : 1 , black :0
pygame.time.set_timer(pygame.USEREVENT, 1000)
timeFont = pygame.font.SysFont('Consolas', 30)
WIDTH = 800
HEIGHT = 720
DIMENSION = 8
SQ_SIZE = 75  # square size
MAX_FPS = 60
corChessNotation =0
turnChessNotation = False
small_font = p.font.Font('freesansbold.ttf', 30)
medium_font = p.font.Font('freesansbold.ttf', 40)
big_font = p.font.Font('freesansbold.ttf', 50)
turn_step = 0
IMAGES = {}
chessNotation = ""
'''
LOAD IMAGE FOR ALL PIECES
'''


def loadImages():
    pieces = ['bp', "bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (
            SQ_SIZE, SQ_SIZE))  # Resizes the Surface to a new size, given as (width, height)

def timeCounter (timer ) :
    x = timer #seconds
    seconds = x % 60
    minutes = int(x / 60) % 60

    return f"{minutes:02}:{seconds:02}"

def drawGameState(screen, gs):
    colors = [p.Color("white"), p.Color("gray")]
    global counter, text ,timeTurn
    counter -= 0.019

    text = timeCounter(int(counter)).rjust(3)
    if (counter ==0) :
            return
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]

            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # draw the rectangle
            piece = gs.board[r][c]
            if (piece != '--'):
                screen.blit(IMAGES[piece.name], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    for i in range(9):
        if i != 8:
            pygame.draw.line(screen, 'black', (0, 75 * i), (75 * 8, 75 * i), 2)
            pygame.draw.line(screen, 'black', (75 * i, 0), (75 * i, 75 * 8), 2)
        else:
            pygame.draw.line(screen, 'black', (75 * i, 0), (75 * i, WIDTH), 2)
    if text != "00:00" :
        if timeTurn ==1 :
            screen.blit(big_font.render(f"White : {text}", True, 'black'), (20, 640))
        else :

            screen.blit(big_font.render(f"Black : {text}", True, 'black'), (20, 640))
    else :
        counter = tempCounter
        if timeTurn ==1  :
            timeTurn =0
        else :
            timeTurn =1


    global chessNotation,corChessNotation
    if chessNotation != 'CHUA END GAME' :

        screen.blit(medium_font.render(chessNotation, True, 'black'), ( 75*8+10,corChessNotation+5))
    screen.blit(small_font.render(" Surrender", True, 'black'), (75*8+15, 75*8+45))
    # screen.blit(small_font.render(text, True, 'black'), (75*8-200, 75*8+30))


    pygame.draw.line(screen, 'black', (0, 75 * 8), (WIDTH, 75 * 8), 2)

    rK, cK = gs.teams[gs.player]['K'][0].position
    if gs.Check(rK, cK, gs.board) != []:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("red"))
        screen.blit(s, (cK * SQ_SIZE, rK * SQ_SIZE))


def highlightSquare(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected
        # if gs.board[r][c] != '--':
        #     if gs.board[r][c].team == ('w' if gs.whiteToMove else 'b'):  # squareSelected is piece can be moved
        # highlight selected square
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(60)
        s.fill(p.Color("blue"))
        screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
        # hightlight the move from that square
        for move in validMoves:
            if gs.board[move[0]][move[1]] == '--':
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))
            elif gs.board[move[0]][move[1]].team != gs.player:
                s.set_alpha(100)
                s.fill(p.Color("orange"))
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))
                s.set_alpha(30)
                s.fill(p.Color("blue"))


'''MAIN DRIVER FOR CODE. UPDATING THE GRPHICS'''


def main():
    # pygame setup

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()  # doc (https://www.pygame.org/docs/ref/time.html)

    gs = Engine.GameState()  # game state
    loadImages()  # running this once before while loop
    running = True

    row, col = 0, 0
    end = 0
    sqSelected = ()  # no square is selected , keep track of the last click of the user (tuple : (row,col))
    playercClicks = []  # keep track of player click (two tuples :[(6,4) , (4,4)])
    # poll for events
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                print ("yes")
                main()
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:

                location = p.mouse.get_pos()  # (x,y) is location of the mouse
                if location[0] >600 and location[1] >600 :
                    if gs.whiteToMove == True:
                        print("white lose")
                    else:
                        print("black lose")

                else:
                    print(f"mouse position : {location}")
                    col = (int)(location[0] // SQ_SIZE)
                    row = (int)(location[1] // SQ_SIZE)
                    if sqSelected == (row, col):  # the user clicked the same square twice
                        sqSelected = ()  # deselect
                        playercClicks = []  # clear player select
                    else:
                        sqSelected = (row, col)

                        playercClicks.append(sqSelected)  # append for both 1st and 2nd clicks

            if end == 0 and len(playercClicks) == 2:  # after 2nd click
                move = Engine.Move(playercClicks[0], playercClicks[1], gs.board)
                global chessNotation
                chessNotation = move.getChessNotation()

                gs.makeMove(move)
                if gs.RESULT() != None:
                    print(gs.RESULT())
                    end = 1
                    break

                sqSelected = ()  # reset
                playercClicks = []  # reset

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(p.Color("gray"))

        # RENDER YOUR GAME HERE
        drawGameState(screen, gs)

        if gs.board[row][col] != '--':
            validMoves = gs.board[row][col].getAllValidMoves(gs)

            highlightSquare(screen, gs, validMoves, sqSelected)

        clock.tick(MAX_FPS)  # update the clock : never run at more than FPS

        # flip() the display to put your work on screen
        p.display.flip()


if __name__ == '__main__':
    main()
