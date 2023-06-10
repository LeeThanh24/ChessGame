import pygame
import sys
import Chess
from button import Button
from python.Service.MatchesService import MatchesService

overallTime = 0


def getMatchTimes():
    print(f"test time {overallTime}")
    return overallTime


def initMenu():
    pygame.init()
    global SCREEN, BG, WIDTH, HEIGHT
    WIDTH = 900
    HEIGHT = 720

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu")

    BG = pygame.image.load("../images/chessBackground2.jpg")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("../images/font.ttf", size)


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


def options(user1='user 1', user2='user 2', score1=0, score2=0):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        backgroundOption = pygame.image.load("../images/optionBackground.jpg")
        SCREEN.blit(backgroundOption, (0, 0))

        OPTIONS_TEXT = get_font(60).render("SELECT BLITZ", True, "#526D82")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH / 2, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_3M = Button(image=None, pos=(WIDTH / 2 + 10, 150),
                             text_input="3 Minutes", font=get_font(50), base_color="Black", hovering_color="White")
        OPTIONS_3M.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_3M.update(SCREEN)

        OPTIONS_5M = Button(image=None, pos=(WIDTH / 2 + 10, 300),
                             text_input="5 Minutes", font=get_font(50), base_color="Black", hovering_color="White")
        OPTIONS_5M.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_5M.update(SCREEN)

        OPTIONS_55M = Button(image=None, pos=(WIDTH / 2 + 10, 450),
                             text_input="5|5", font=get_font(50), base_color="Black", hovering_color="White")
        OPTIONS_55M.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_55M.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(WIDTH / 2 + 10, HEIGHT / 2 + 300),
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
                    main_menu(user1=user1, user2=user2, score1=score1, score2=score2)
                if OPTIONS_3M.checkForInput(OPTIONS_MOUSE_POS):
                    # matchTimes(30*60)
                    overallTime = 3 * 60
                    print(f"overall time now {overallTime} :1mins")
                    break
                if OPTIONS_5M.checkForInput(OPTIONS_MOUSE_POS):
                    # matchTimes(60 * 60)
                    overallTime = 5 * 60
                    print(f"overall time now {overallTime} :3mins")
                    break
                if OPTIONS_55M.checkForInput(OPTIONS_MOUSE_POS):
                    # matchTimes(90 * 60)
                    overallTime = 5 * 60
                    print(f"overall time now {overallTime} :5mins")
                    break

        pygame.display.update()


def paging(user1='user 1', user2='user 2', score1=0, score2=0):
    # Initialize Pygame
    pygame.init()

    # Create a window
    screen = pygame.display.set_mode((900, 720))

    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Set the font
    font = pygame.font.Font(None, 30)

    # Define the content to display
    matches = MatchesService().getAllMatches()
    content = []
    for i in range(len(matches)):
        temp = (matches[i].name + " " + "<" + matches[i].matchTime + ">")
        content.append(temp)
    content.reverse()
        # print(f"{temp}")
    print(f"len of content {len(content)}")
    content1 = [
        "Page 1 - Line 1",
        "Page 1 - Line 2",
        "Page 1 - Line 3",
        # ... add more lines for page 1
        "Page 2 - Line 1",
        "Page 2 - Line 2",
        "Page 2 - Line 3",
        # ... add more lines for page 2
        "Page 3 - Line 1",
        "Page 3 - Line 2",
        "Page 3 - Line 3",
        # ... add more lines for page 3
        "Page 4 - Line 1",
        "Page 4 - Line 2",
        "Page 4 - Line 3",
        # ... add more lines for page 4
        "Page 5 - Line 1",
        "Page 5 - Line 2",
        "Page 5 - Line 3",
        # ... add more lines for page 5
        "Page 6 - Line 1",
        "Page 6 - Line 2",
        "Page 6 - Line 3",
        # ... add more lines for page 6
        "Page 7 - Line 1",
        "Page 7 - Line 2",
        "Page 7 - Line 3",
        # ... add more lines for page 7
    ]

    # Define the number of lines per page
    lines_per_page = 7

    # Define the current page
    current_page = 1

    # Main game loop
    running = True
    while running:

        # Clear the screen
        screen.fill("#526D82")
        # BACK BUTTON
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK = Button(image=None, pos=(WIDTH / 2 + 10, HEIGHT / 2 + 300),
                              text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Red")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)

        OPTIONS_BACK.update(screen)
        # title
        OPTIONS_TEXT = get_font(60).render("MATCH HISTORY", True, "gray")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH / 2, 50))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Calculate the start and end index for the current page
        start_index = (current_page - 1) * lines_per_page
        end_index = start_index + lines_per_page

        # Extract the lines for the current page
        lines = content[start_index:end_index]

        # Render and blit the lines to the screen
        for i, line in enumerate(lines):
            MATCH_TEXT = get_font(20).render(line, True, BLACK)
            MATCH_TEXT_RECT = MATCH_TEXT.get_rect()
            MATCH_TEXT_RECT.center = (900 // 2, 130 + i * 70)
            screen.blit(MATCH_TEXT, MATCH_TEXT_RECT)


        # Render and blit the page number to the screen
        page_text = f"Page {current_page}"
        page_surface = font.render(page_text, True, BLACK)
        screen.blit(page_surface, (420, 600))



        # Check for events
        for event in pygame.event.get():

            def checkBackButton(x, y):
                if x >= 381 and x <= 531 and y >= 644 and y <= 670:
                    return True
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to go to the next page
                    current_page += 1
                    if current_page > (len(content) / lines_per_page)+1:
                        current_page = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y=event.pos
                if event.button == 1:  # Left mouse button
                    #print("Left mouse button pressed at", event.pos)
                    if checkBackButton(x,y):
                        #print("yes x y ")
                        main_menu(user1=user1, user2=user2, score1=score1, score2=score2)
                elif event.button == 3:  # Right mouse button
                    #print("Right mouse button pressed at", event.pos)
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    #print("Left mouse button released at", event.pos)
                    pass
                elif event.button == 3:  # Right mouse button
                    #print("Right mouse button released at", event.pos)
                    pass
            elif event.type == pygame.MOUSEMOTION:
                pass
                #print("Mouse moved to", event.pos)
                # 381 644
                # 531 670
            #
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()


def history(user1='user 1', user2='user 2', score1=0, score2=0):
    running = True
    while running:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_BACK = Button(image=None, pos=(WIDTH / 2 + 10, HEIGHT / 2 + 300),
                              text_input="BACK", font=get_font(40), base_color="Black", hovering_color="Red")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu(user1=user1, user2=user2, score1=score1, score2=score2)

        pygame.display.update()


def main_menu(user1='user 1', user2='user 2', score1=0, score2=0):
    initMenu()
    print(f"user 1 {user1} - score1 {score1}")
    print(f"user 2 {user2} - score2 {score2}")
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH / 2, 80))

        PLAY_BUTTON = Button(image=pygame.image.load("../images/Play Rect.png"), pos=(WIDTH / 2, 200),
                             text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("../images/Play Rect.png"), pos=(WIDTH / 2, 350),
                                text_input="OPTIONS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        HISTORY_BUTTON = Button(image=pygame.image.load("../images/Play Rect.png"), pos=(WIDTH / 2, 500),
                                text_input="HISTORY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("../images/Play Rect.png"), pos=(WIDTH / 2, 650),
                             text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, HISTORY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # play()
                    print(f"time in main.py {overallTime}")

                    if overallTime != 0:
                        Chess.main(matchTimes=overallTime, user1=user1, user2=user2, score1=score1, score2=score2)
                    else:
                        Chess.main(user1=user1, user2=user2, score1=score1, score2=score2)
                    return
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(user1=user1, user2=user2, score1=score1, score2=score2)

                if HISTORY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # history(user1=user1,user2=user2,score1=score1,score2=score2)
                    paging(user1=user1,user2=user2,score1=score1,score2=score2)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main_menu()
