"""this is main driver file. It will be responsible for handling user input
and displaying the current GameState object """
import pygame as p
import pygame.draw
import Engine
from python.Service.UsersService import *

# config
p.init()
clock = pygame.time.Clock()
WIDTH = 1150
HEIGHT = 720
DIMENSION = 8
SQ_SIZE = 75  # square size
MAX_FPS = 60

# font
timeFont = pygame.font.SysFont('Consolas', 30)
small_font = p.font.Font('freesansbold.ttf', 30)
medium_font = p.font.Font('freesansbold.ttf', 40)
big_font = p.font.Font('freesansbold.ttf', 50)

# images
IMAGES = {}

'''
LOAD IMAGE FOR ALL PIECES
'''


def mainMenu(user1='user 1', user2='user 2', score1=0, score2=0):
    from main import main_menu as menu
    return menu(user1=user1, user2=user2, score1=score1, score2=score2)


def loadImages():
    pieces = ['bp', "bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (
            SQ_SIZE, SQ_SIZE))  # Resizes the Surface to a new size, given as (width, height)


def timeCounter(timer):
    x = timer
    seconds = x % 60
    minutes = int(x / 60) % 60
    hours = int(x / 3600)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def drawCaptured(screen, gs):
    try:
        capturedInt = 6
        # BLACK
        if len(gs.achievement['w']) > 2 * capturedInt:
            for i in range(capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"b{gs.achievement['w'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(600, (i + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(capturedInt, 2 * capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"b{gs.achievement['w'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(680, (i - capturedInt + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(2 * capturedInt, len(gs.achievement['w'])):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"b{gs.achievement['w'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(760, (i - 2 * capturedInt + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        elif len(gs.achievement['w']) > capturedInt:
            for i in range(capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"b{gs.achievement['w'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(600, (i + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(capturedInt, len(gs.achievement['w'])):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"b{gs.achievement['w'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(680, (i - capturedInt + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        else:
            for i in range(len(gs.achievement['w'])):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"b{gs.achievement['w'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(600, (i + 1) * SQ_SIZE, 1, 1))

        # WHITE
        if len(gs.achievement['b']) > 2 * capturedInt:
            for i in range(capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"w{gs.achievement['b'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(840, (i + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(capturedInt, 2 * capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"w{gs.achievement['b'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(930, (i - capturedInt + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(2 * capturedInt, len(gs.achievement['b'])):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"w{gs.achievement['b'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(1010, (i - 2 * capturedInt + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        if len(gs.achievement['b']) > capturedInt:
            for i in range(capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"w{gs.achievement['b'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(840, (i + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(capturedInt, 2 * capturedInt):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"w{gs.achievement['b'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(930, (i - capturedInt + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        else:
            for i in range(len(gs.achievement['b'])):
                # print(f"co an w{gs.achievement['w'][i].type}", end=" ")
                temp = str(f"w{gs.achievement['b'][i].type}")
                screen.blit(IMAGES[temp], p.Rect(840, (i + 1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    except:
        pass


def drawTurn(screen, gs, user1, user2):
    global counter
    counter -= 0.019
    text = timeCounter(int(counter)).rjust(3)
    # print (f"text : {text}")
    if text != "00:00:00":
        if gs.whiteToMove == True:
            screen.blit(big_font.render(f"White turn - {text}", True, 'black'), (20, 640))
        else:
            screen.blit(big_font.render(f"Black turn - {text}", True, 'black'), (20, 640))
    else:

        countWhite = len(gs.achievement['w'])
        countBlack = len(gs.achievement['b'])

        if countWhite < countBlack:
            pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
            screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
            screen.blit(small_font.render(f'Black won !', True, 'white'), (410, 350))
            screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))
            UsersService().updateScoreByUsername(user1, 1)
        elif countWhite > countBlack:
            pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
            screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
            screen.blit(small_font.render(f'White won !', True, 'white'), (410, 350))
            screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))
            UsersService().updateScoreByUsername(user2, 1)
        else:
            pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
            screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
            screen.blit(small_font.render(f'Draw !', True, 'white'), (410, 350))
            screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))
        pygame.time.wait(3000)
        # time.sleep(3)
        # counter, text = 8, '10'.rjust(3)
        #
        # gameOver =True
        # main()


def drawGameState(screen, gs, user1='user 1', user2='user 2', score1=0, score2=0):
    colors = [p.Color("white"), p.Color("gray")]
    global counter, text, timeTurn

    if (counter == 0):
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
            if i == 0 or i == 1 or i == 7:
                pygame.draw.line(screen, 'black', (0, SQ_SIZE * i), (WIDTH, SQ_SIZE * i), 2)  # NGANG
                pygame.draw.line(screen, 'black', (SQ_SIZE * i, 0), (SQ_SIZE * i, SQ_SIZE * 8), 2)  # DOC
            else:
                pygame.draw.line(screen, 'black', (0, SQ_SIZE * i), (SQ_SIZE * 8, SQ_SIZE * i), 2)  # NGANG
                pygame.draw.line(screen, 'black', (SQ_SIZE * i, 0), (SQ_SIZE * i, SQ_SIZE * 8), 2)  # DOC

        else:
            pygame.draw.line(screen, 'black', (SQ_SIZE * i, 0), (SQ_SIZE * i, WIDTH), 2)

    # draw user
    # pygame.draw.rect(screen, 'black', [602, 526, SQ_SIZE*8, SQ_SIZE])
    # pygame.draw.rect(screen, 'black', [602, 1, SQ_SIZE*8, SQ_SIZE])
    screen.blit(small_font.render(f'{user2} - Score: {score2}', True, 'black'), (740, 550))
    screen.blit(small_font.render(f'{user1} - Score: {score1}', True, 'black'), (740, 25))

    # load avatar
    ava1 = p.image.load("images/avaWhite1.jpg")
    ava1 = p.transform.scale(ava1, (SQ_SIZE - 4, SQ_SIZE - 4))
    screen.blit(ava1, (620, 528))

    ava2 = p.image.load("images/avaWhite1.jpg")
    ava2 = p.transform.scale(ava2, (SQ_SIZE - 4, SQ_SIZE - 4))
    screen.blit(ava2, (620, 3))

    # result
    result = gs.RESULT()

    # Surrend
    global gameOver, turnResult,updated
    if gameOver == True or result != None:
        if result != None:
            pygame.draw.rect(screen, 'black', [400, 300, 440, 80])
            screen.blit(small_font.render(f'{result}', True, 'white'), (410, 310))
            if result == 'WHITE WIN':
                if turnResult == True:
                    UsersService().updateScoreByUsername(user2, 1)
            elif result == 'BLACK WIN':
                if turnResult == True:
                    UsersService().updateScoreByUsername(user1, 1)
            screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 340))
            turnResult = False
        else:

            draw_game_over(screen, gs.whiteToMove, user1, user2)

    else:
        drawTurn(screen, gs, user1, user2)

    screen.blit(medium_font.render(" Surrend", True, 'black'), (75 * 8 + 180, 75 * 8 + 45))
    pygame.draw.line(screen, 'black', (0, 75 * 8), (WIDTH, 75 * 8), 2)

    # captured move
    drawCaptured(screen, gs)

    # warning checkamte
    rK, cK = gs.teams[gs.player]['K'][0].position
    if gs.Check(rK, cK, gs.board) != []:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("red"))
        screen.blit(s, (cK * SQ_SIZE, rK * SQ_SIZE))


def draw_game_over(screen, winner, user1='user 1', user2='user 2'):
    global gameOver ,updated

    print(f"test surrender ")
    pygame.draw.rect(screen, 'black', [400, 300, 440, 80])
    if winner == True:  # white
        screen.blit(small_font.render(f'Black won the game!', True, 'white'), (410, 310))
        if updated == False:
            UsersService().updateScoreByUsername(user1, 1)
    else:
        screen.blit(small_font.render(f'White won the game!', True, 'white'), (410, 310))
        if updated == False:
            UsersService().updateScoreByUsername(user2, 1)
    updated =True
    #gameOver = False
    screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 340))

    return True


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


def main(matchTimes=30 * 60, user1='user 1', user2='user 2', score1=0, score2=0):
    # pygame setup
    # global variable
    global gameOver, timeTurn
    global counter, text
    global turnResult , updated
    score1 = UsersService().findScoreByUsername(user1)
    score2 = UsersService().findScoreByUsername(user2)
    turnResult = False
    tempMatchTimes = matchTimes
    counter, text = matchTimes, '10'.rjust(3)  # overall time of match
    tempCounter = counter
    timeTurn = 1  # white : 1 , black :0
    gameOver = False

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

    userText = ''
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:  # Enter button
                gameOver = False
                main(matchTimes=tempMatchTimes, user1=user1, user2=user2, score1=score1, score2=score2)
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_p:  # P button
                print("return to menu")
                mainMenu(user1=user1, user2=user2, score1=score1, score2=score2)
                # tuple[0]

            elif e.type == p.MOUSEBUTTONDOWN:

                location = p.mouse.get_pos()  # (x,y) is location of the mouse
                if location[0] > 600 and location[1] > 600:  # surrend button
                    updated = False
                    gameOver = True
                    break
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

                gs.makeMove(move)
                if gs.RESULT() != None:
                    result = gs.RESULT()
                    print(result)
                    turnResult = True
                    end = 1
                    break

                # drawCaptured(screen, gs)
                sqSelected = ()  # reset
                playercClicks = []  # reset

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(p.Color("gray"))

        # RENDER YOUR GAME HERE
        drawGameState(screen, gs, user1, user2, score1, score2)

        if gs.board[row][col] != '--':
            validMoves = gs.board[row][col].getAllValidMoves(gs)

            highlightSquare(screen, gs, validMoves, sqSelected)

        clock.tick(MAX_FPS)  # update the clock : never run at more than FPS

        # flip() the display to put your work on screen
        p.display.flip()


if __name__ == '__main__':
    main()
