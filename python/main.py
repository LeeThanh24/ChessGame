import pygame
import sys
import Chess
from button import Button


overallTime = 0
def getMatchTimes ( ) :
    print(f"test time {overallTime}")
    return overallTime

def initMenu ():
    pygame.init()
    global SCREEN, BG,WIDTH,HEIGHT
    WIDTH = 900
    HEIGHT = 720

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("images/chessBackground2.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("images/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        backgroundOption = pygame.image.load("images/optionBackground.jpg")
        SCREEN.blit(backgroundOption,(0,0))

        OPTIONS_TEXT = get_font(60).render("SELECT TIMES", True, "#526D82")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_30M = Button(image=None, pos=(WIDTH / 2 + 10, 150),
                             text_input="30 Minutes", font=get_font(50), base_color="Black", hovering_color="White")
        OPTIONS_30M.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_30M.update(SCREEN)

        OPTIONS_60M = Button(image=None, pos=(WIDTH / 2 + 10, 300),
                             text_input="60 Minutes", font=get_font(50), base_color="Black", hovering_color="White")
        OPTIONS_60M.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_60M.update(SCREEN)

        OPTIONS_90M = Button(image=None, pos=(WIDTH / 2 + 10, 450),
                             text_input="90 Minutes", font=get_font(50), base_color="Black", hovering_color="White")
        OPTIONS_90M.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_90M.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(WIDTH/2+10, HEIGHT /2+300),
                            text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Red")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        global overallTime
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_30M.checkForInput(OPTIONS_MOUSE_POS):
                    #matchTimes(30*60)
                    overallTime = 30*60
                    print (f"overall time now {overallTime} :30mins")
                    break
                if OPTIONS_60M.checkForInput(OPTIONS_MOUSE_POS):
                    # matchTimes(60 * 60)
                    overallTime = 60 * 60
                    print (f"overall time now {overallTime} :60mins")
                    break
                if OPTIONS_90M.checkForInput(OPTIONS_MOUSE_POS):
                    #matchTimes(90 * 60)
                    overallTime = 90 * 60
                    print (f"overall time now {overallTime} :90mins")
                    break

        pygame.display.update()

def main_menu():
    initMenu()
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 120))

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(WIDTH / 2, 250),
                             text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(WIDTH / 2, 400),
                                text_input="OPTIONS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(WIDTH / 2, 550),
                             text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #play()
                    print(f"time in main.py {overallTime}")
                    if overallTime !=0 :
                        Chess.main(matchTimes=overallTime)
                    else :
                        Chess.main()
                    return
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
if __name__ == '__main__':
    main_menu()