"""this is main driver file. It will be responsible for handling user input
and displaying the current GameState object """
import pygame as p
import pygame.draw
import Engine
from python.Service.MatchesService import MatchesService
from python.Service.UsersService import *
from datetime import datetime

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
medium_font = p.font.Font('freesansbold.ttf', 36)
big_font = p.font.Font('freesansbold.ttf', 60)

# images
IMAGES = {}

'''
LOAD IMAGE FOR ALL PIECES
'''


def mainMenu(user1='user 1', user2='user 2', score1=0, score2=0):
    from Menu import main_menu as menu
    return menu(user1=user1, user2=user2, score1=score1, score2=score2)


def loadImages():
    pieces = ['bp', "bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("../images/" + piece + ".png"), (
            SQ_SIZE, SQ_SIZE))  # Resizes the Surface to a new size, given as (width, height)


def timeCounter(timer):
    x = timer
    seconds = x % 60
    minutes = int(x / 60) % 60
    hours = int(x / 3600)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def eachTimeCounter(timer):
    x = timer
    seconds = x % 60
    minutes = int(x / 60) % 60

    return f"{minutes:02}:{seconds:02}"


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
    global counter, count, playerTime, player2Time, previousPlayer, tempPlayerTime, turnResult, turn2Result
    global checkPlusTime, checkPlusTime2, isLastMode, start,player1Color ,player2Color
    # counter -= 0.019

    text = timeCounter(int(counter)).rjust(3)
    playerTimeText = eachTimeCounter(int(playerTime)).rjust(3)
    player2TimeText = eachTimeCounter(int(player2Time)).rjust(3)
    # if gs.whiteToMove == False and previousPlayer == 'w':  # from white to black
    #     playerTime = tempPlayerTime
    #     playerTime -= 0.019
    #     playerTimeText = eachTimeCounter(int(playerTime)).rjust(3)
    #
    if isLastMode == True :
        if gs.player == 'b' and gs.whiteToMove == False:  # white moved , black not moved
            if checkPlusTime == False:
                playerTime += 5
                checkPlusTime = True
            else:
                playerTimeText = eachTimeCounter(int(playerTime)).rjust(3)
                MATCH_TEXT = medium_font.render(f"{user2} turn - {playerTimeText}", True, 'black')
                MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                MATCH_TEXT_RECT.center = (190, 665)
                screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)

        if gs.player == 'w' and gs.whiteToMove == True:  # black moved , white not moved , except starting time
            if start == True:
                if checkPlusTime2 == False:

                    checkPlusTime2 = True
                else:
                    player2TimeText = eachTimeCounter(int(player2Time)).rjust(3)
                    MATCH_TEXT = medium_font.render(f"{user1} turn - {player2TimeText}", True, 'black')
                    MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                    MATCH_TEXT_RECT.center = (960, 665)
                    screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)
                start = False
            else:
                if checkPlusTime2 == False:
                    player2Time += 5
                    checkPlusTime2 = True
                else:
                    player2TimeText = eachTimeCounter(int(player2Time)).rjust(3)
                    MATCH_TEXT = medium_font.render(f"{user1} turn - {player2TimeText}", True, 'black')
                    MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                    MATCH_TEXT_RECT.center = (960, 665)
                    screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)

        if text != "00:00:00":
            if gs.player == 'w':  # WHITE
                if playerTimeText == '00:00':
                    MATCH_TEXT = medium_font.render(f"{user2} turn - {playerTimeText}", True, 'black')
                    MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                    MATCH_TEXT_RECT.center = (190, 665)
                    screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)

                    pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
                    screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
                    screen.blit(small_font.render(f'{user1} won !', True, 'white'), (410, 350))
                    screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))

                    current_datetime = datetime.now()
                    # Format the date and time as a string
                    matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    if turnResult == False:
                        MatchesService().insertMatch(f"{user1} WON {user2}", matchTime)
                        UsersService().updateScoreByUsername(user1, 1)
                        turnResult = True
                else:
                    playerTime -= 0.019
                    playerTimeText = eachTimeCounter(int(playerTime)).rjust(3)
                    player2Color = 'red'

                    checkPlusTime = False
            if checkPlusTime != True:
                MATCH_TEXT = medium_font.render(f"{user2} turn - {playerTimeText}", True, player2Color)
                MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                MATCH_TEXT_RECT.center = (190, 665)
                screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)

            if gs.player == 'b': # BLACK
                if player2TimeText == '00:00':
                    MATCH_TEXT = medium_font.render(f"{user1} turn - {player2TimeText}", True, 'black')
                    MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                    MATCH_TEXT_RECT.center = (960, 665)
                    screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)
                    pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
                    screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
                    screen.blit(small_font.render(f'{user2} won !', True, 'white'), (410, 350))
                    screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))

                    current_datetime = datetime.now()
                    # Format the date and time as a string
                    matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    if turn2Result == False:
                        MatchesService().insertMatch(f"{user1} LOSE {user2}", matchTime)
                        UsersService().updateScoreByUsername(user2, 1)
                        turn2Result = True
                else:
                    player2Time -= 0.019
                    player2TimeText = eachTimeCounter(int(player2Time)).rjust(3)

                    player1Color ='red'
                    checkPlusTime2 = False
            if checkPlusTime2 != True:
                MATCH_TEXT = medium_font.render(f"{user1} turn - {player2TimeText}", True, player1Color)
                MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                MATCH_TEXT_RECT.center = (960, 665)
                screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)
    else :
        # if gs.player == 'b' and previousPlayer =='w':  # white moved , black not moved
        #     playerTime += 5
        #     playerTimeText = eachTimeCounter(int(playerTime)).rjust(3)
        #
        #
        # if gs.player == 'w' and previousPlayer =='b':  # black moved , white not moved , except starting time
        #     player2Time += 5
        #     player2TimeText = eachTimeCounter(int(player2Time)).rjust(3)

        if text != "00:00:00":
            if gs.player == 'w':  # WHITE
                if playerTimeText == '00:00':
                    MATCH_TEXT = medium_font.render(f"{user2} turn - {playerTimeText}", True, 'black')
                    MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                    MATCH_TEXT_RECT.center = (190, 665)
                    screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)

                    pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
                    screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
                    screen.blit(small_font.render(f'{user1} won !', True, 'white'), (410, 350))
                    screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))

                    current_datetime = datetime.now()
                    # Format the date and time as a string
                    matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    if turnResult == False:
                        MatchesService().insertMatch(f"{user1} WON {user2}", matchTime)
                        UsersService().updateScoreByUsername(user1, 1)
                        turnResult = True
                else:
                    previousPlayer = 'w'
                    playerTime -= 0.019
                    playerTimeText = eachTimeCounter(int(playerTime)).rjust(3)
                    player2Color ='red'

            MATCH_TEXT = medium_font.render(f"{user2} turn - {playerTimeText}", True, player2Color)
            MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
            MATCH_TEXT_RECT.center = (190, 665)
            screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)
            player2Color = 'black'
            if gs.player == 'b':
                if player2TimeText == '00:00':
                    MATCH_TEXT = medium_font.render(f"{user1} turn - {player2TimeText}", True, 'black')
                    MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
                    MATCH_TEXT_RECT.center = (960, 665)
                    screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)
                    pygame.draw.rect(screen, 'black', [400, 300, 440, 150])
                    screen.blit(small_font.render(f"Time's up !", True, 'white'), (410, 310))
                    screen.blit(small_font.render(f'{user2} won !', True, 'white'), (410, 350))
                    screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 390))

                    current_datetime = datetime.now()
                    # Format the date and time as a string
                    matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    if turn2Result == False:
                        MatchesService().insertMatch(f"{user1} LOSE {user2}", matchTime)
                        UsersService().updateScoreByUsername(user2, 1)
                        turn2Result = True

                else:
                    previousPlayer = 'b'
                    player2Time -= 0.019
                    player2TimeText = eachTimeCounter(int(player2Time)).rjust(3)

                    checkPlusTime2 = False
                    player1Color = 'red'
            MATCH_TEXT = medium_font.render(f"{user1} turn - {player2TimeText}", True, player1Color)
            MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
            MATCH_TEXT_RECT.center = (960, 665)
            screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)
            player1Color = 'black'


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
        # if i != 8:
        if i == 0 or i == 1 or i == 7:
            pygame.draw.line(screen, 'black', (0, SQ_SIZE * i), (WIDTH, SQ_SIZE * i), 2)  # NGANG
            pygame.draw.line(screen, 'black', (SQ_SIZE * i, 0), (SQ_SIZE * i, SQ_SIZE * 8), 2)  # DOC
        else:
            pygame.draw.line(screen, 'black', (0, SQ_SIZE * i), (SQ_SIZE * 8, SQ_SIZE * i), 2)  # NGANG
            pygame.draw.line(screen, 'black', (SQ_SIZE * i, 0), (SQ_SIZE * i, SQ_SIZE * 8), 2)  # DOC
    # else:
    #     pygame.draw.line(screen, 'black', (SQ_SIZE * i, 0), (SQ_SIZE * i, WIDTH), 2)
    pygame.draw.line(screen, 'black', (SQ_SIZE * 4 + 90, SQ_SIZE * 8,), (SQ_SIZE * 4 + 90, WIDTH), 4)  # DOC
    pygame.draw.line(screen, 'black', (SQ_SIZE * 9 + 100, SQ_SIZE * 8,), (SQ_SIZE * 9 + 100, WIDTH), 4)  # DOC

    # draw user
    pygame.draw.rect(screen, 'black', [602, 526, SQ_SIZE * 8, SQ_SIZE])
    pygame.draw.rect(screen, 'black', [602, 1, SQ_SIZE * 8, SQ_SIZE])
    screen.blit(small_font.render(f'{user2} - Score: {score2}', True, 'white'), (740, 550))
    screen.blit(small_font.render(f'{user1} - Score: {score1}', True, 'white'), (740, 25))

    # load avatar
    ava1 = p.image.load("../images/avaWhite1.jpg")
    ava1 = p.transform.scale(ava1, (SQ_SIZE - 4, SQ_SIZE - 4))
    screen.blit(ava1, (620, 528))

    ava2 = p.image.load("../images/avaWhite1.jpg")
    ava2 = p.transform.scale(ava2, (SQ_SIZE - 4, SQ_SIZE - 4))
    screen.blit(ava2, (620, 3))

    # result
    result = gs.RESULT()

    # captured move
    drawCaptured(screen, gs)

    # Surrend
    global gameOver, turnResult, updated
    if gameOver == True or result != None:
        if result != None:
            pygame.draw.rect(screen, 'black', [400, 300, 440, 80])

            if result == 'WHITE WIN':
                if turnResult == True:
                    UsersService().updateScoreByUsername(user2, 1)
                    name = user1 + " LOSE " + user2

                    # Get the current date and time
                    current_datetime = datetime.now()
                    # Format the date and time as a string
                    matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    MatchesService().insertMatch(name, matchTime)
                screen.blit(small_font.render(f'{user2} WON the game', True, 'white'), (410, 310))
            elif result == 'BLACK WIN':
                screen.blit(small_font.render(f'{user1} WON the game', True, 'white'), (410, 310))
                if turnResult == True:
                    UsersService().updateScoreByUsername(user1, 1)
                    name = user1 + " WIN " + user2
                    # Get the current date and time
                    current_datetime = datetime.now()
                    # Format the date and time as a string
                    matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
                    MatchesService().insertMatch(name, matchTime)
            screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 340))
            turnResult = False
        else:
            draw_game_over(screen, gs.whiteToMove, user1, user2)

    else:
        drawTurn(screen, gs, user1, user2)

    screen.blit(medium_font.render(" Surrend", True, 'black'), (75 * 7-20, 75 * 8 + 45))
    pygame.draw.line(screen, 'black', (0, 75 * 8), (WIDTH, 75 * 8), 2)



    # warning checkamte
    rK, cK = gs.teams[gs.player]['K'][0].position
    if gs.Check(rK, cK, gs.board) != []:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("red"))
        screen.blit(s, (cK * SQ_SIZE, rK * SQ_SIZE))


def draw_game_over(screen, winner, user1='user 1', user2='user 2'):
    global gameOver, updated

    # print(f"test surrender ")
    pygame.draw.rect(screen, 'black', [400, 300, 440, 80])
    if winner == True:  # white
        screen.blit(small_font.render(f'{user1} WON the game!', True, 'white'), (410, 310))

        if updated == False:
            UsersService().updateScoreByUsername(user1, 1)
            name = user1 + " WIN " + user2

            # Get the current date and time
            current_datetime = datetime.now()
            # Format the date and time as a string
            matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
            MatchesService().insertMatch(name, matchTime)
    else:
        screen.blit(small_font.render(f'{user2} WON the game!', True, 'white'), (410, 310))
        if updated == False:
            UsersService().updateScoreByUsername(user2, 1)
            name = user1 + " LOSE " + user2

            # Get the current date and time
            current_datetime = datetime.now()
            # Format the date and time as a string
            matchTime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
            MatchesService().insertMatch(name, matchTime)
    updated = True
    # gameOver = False
    screen.blit(small_font.render(f'Press ENTER to Restart', True, 'white'), (410, 340))

    return True


def highlightSquare(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected

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


def main(matchTimes=1 * 60, user1='user 1', user2='user 2', score1=0, score2=0):
    # pygame setup
    # global variable
    global gameOver, timeTurn, playerTime, player2Time, previousPlayer, tempPlayerTime
    global counter, text
    global turnResult, turn2Result, updated, isLastMode, checkPlusTime, checkPlusTime2
    global start ,player1Color ,player2Color

    start = True
    # score for users
    score1 = UsersService().findScoreByUsername(user1)
    score2 = UsersService().findScoreByUsername(user2)

    # check if update to database
    turnResult = False
    turn2Result = False

    # match time
    tempMatchTimes = matchTimes
    counter, text = 60, '10'.rjust(3)  # overall time of match
    isLastMode = False
    if matchTimes == 5 * 60:
        isLastMode = True

    # PLAYER TIME
    playerTime = matchTimes
    player2Time = matchTimes
    tempPlayerTime = matchTimes
    previousPlayer = 'w'
    checkPlusTime = False
    checkPlusTime2 = False

    #PLAYER COLOR
    player1Color ="red"
    player2Color ="red"

    # Game over
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
                if location[0] >= 392 and location[0] <=776 and location[1] > 600:  # surrend button
                    updated = False
                    gameOver = True
                    # (825, 600)
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
