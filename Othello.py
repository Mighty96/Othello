import pygame
import time
import sys

pygame.init()

# 이미지 불러오기
mainmenu_background = pygame.image.load("Images/mainmenu/background.png")
mainmenu_start = pygame.image.load("Images/mainmenu/start.png")
mainmenu_explain = pygame.image.load("Images/mainmenu/explain.png")
mainmenu_finish = pygame.image.load("Images/mainmenu/finish.png")
mainmenu_start_click = pygame.image.load("Images/mainmenu/start_click.png")
mainmenu_explain_click = pygame.image.load("Images/mainmenu/explain_click.png")
mainmenu_finish_click = pygame.image.load("Images/mainmenu/finish_click.png")

game_background = pygame.image.load("Images/game/background.png")
game_player_turn = pygame.image.load("Images/game/player_turn.png")
game_player1 = pygame.image.load("Images/game/animal1.png")
game_player2 = pygame.image.load("Images/game/animal2.png")
game_score = pygame.image.load("Images/game/score.png")
game_finish = pygame.image.load("Images/game/finish.png")

# 기본 설정
display_width = 960  # 화면 가로 크기
display_height = 640  # 화면 세로 크기
gameDisplay = pygame.display.set_mode((display_width, display_height))  # 화면 크기설정
pygame.display.set_caption("Othello")  # 타이틀
clock = pygame.time.Clock()
there_is = [[0 for i in range(8)] for j in range(8)]  # 돌이 놓여있는가? 누구의 돌인가? 를 판단
Red = (184, 59, 59)


class Button:  # 버튼
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표
        click = pygame.mouse.get_pressed()  # 클릭여부
        if x + width > mouse[0] > x and y + height > mouse[1] > y:  # 마우스가 버튼안에 있을 때
            gameDisplay.blit(img_act, (x_act, y_act))  # 버튼 이미지 변경
            if click[0] and action is not None:  # 마우스가 버튼안에서 클릭되었을 때
                time.sleep(0.2)
                action()
        else:
            gameDisplay.blit(img_in, (x, y))


class Player:  # 플레이어 행동
    def __init__(self, img, turn):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.turn = turn
        for i in range(8):
            for j in range(8):
                if (43 + (i * 70)) < mouse[0] < (113 + (i * 70)) and \
                        (40 + (j * 70)) < mouse[1] < (110 + (j * 70)) and \
                        there_is[i][j] == 0:  # 마우스 올려진 좌표 빈칸 검사
                    gameDisplay.blit(img, (53 + (i * 70), 50 + (j * 70)))  # 빈칸일 시 미리보기
                    if click[0] and turn == 1:  # 1P가 빈자리를 클릭
                        if possible_check(i, j, 1, 2):
                            there_is[i][j] = 1
                            self.turn = 2
                    elif click[0] and turn == 2:  # 2P가 빈자리를 클릭
                        if possible_check(i, j, 2, 1):
                            there_is[i][j] = 2
                            self.turn = 1


def possible_check(x, y, player, opponent):
    check = False  # 놓을 수 없다고 가정
    if x > 0 and y > 0 and there_is[x - 1][y - 1] == opponent:  # 좌상단
        temp_x = x - 1
        temp_y = y - 1
        while temp_x >= 0 and temp_y >= 0:
            if there_is[temp_x][temp_y] == opponent:
                temp_x -= 1
                temp_y -= 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_x += 1
                temp_y += 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_x += 1
                    temp_y += 1
                break
            else:
                break
    if y > 0 and there_is[x][y - 1] == opponent:  # 상단
        temp_x = x
        temp_y = y - 1
        while temp_y >= 0:
            if there_is[temp_x][temp_y] == opponent:
                temp_y -= 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_y += 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_y += 1
                break
            else:
                break
    if x < 7 and y > 0 and there_is[x + 1][y - 1] == opponent:  # 우상단
        temp_x = x + 1
        temp_y = y - 1
        while temp_x <= 7 and temp_y >= 0:
            if there_is[temp_x][temp_y] == opponent:
                temp_x += 1
                temp_y -= 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_x -= 1
                temp_y += 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_x -= 1
                    temp_y += 1
                break
            else:
                break
    if x < 7 and there_is[x + 1][y] == opponent:  # 우측
        temp_x = x + 1
        temp_y = y
        while temp_x <= 7:
            if there_is[temp_x][temp_y] == opponent:
                temp_x += 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_x -= 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_x -= 1
                break
            else:
                break
    if x < 7 and y < 7 and there_is[x + 1][y + 1] == opponent:  # 우하단
        temp_x = x + 1
        temp_y = y + 1
        while temp_x <= 7 and temp_y <= 7:
            if there_is[temp_x][temp_y] == opponent:
                temp_x += 1
                temp_y += 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_x -= 1
                temp_y -= 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_x -= 1
                    temp_y -= 1
                break
            else:
                break
    if y < 7 and there_is[x][y + 1] == opponent:  # 하단
        temp_x = x
        temp_y = y + 1
        while temp_y <= 7:
            if there_is[temp_x][temp_y] == opponent:
                temp_y += 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_y -= 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_y -= 1
                break
            else:
                break
    if x > 0 and y < 7 and there_is[x - 1][y + 1] == opponent:  # 좌하단
        temp_x = x - 1
        temp_y = y + 1
        while temp_x >= 0 and temp_y <= 7:
            if there_is[temp_x][temp_y] == opponent:
                temp_x -= 1
                temp_y += 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_x += 1
                temp_y -= 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_x += 1
                    temp_y -= 1
                break
            else:
                break
    if x > 0 and there_is[x - 1][y] == opponent:  # 좌측
        temp_x = x - 1
        temp_y = y
        while temp_x >= 0:
            if there_is[temp_x][temp_y] == opponent:
                temp_x -= 1
            elif there_is[temp_x][temp_y] == player:
                check = True
                temp_x += 1
                while there_is[temp_x][temp_y] == opponent:
                    there_is[temp_x][temp_y] = player
                    temp_x += 1
                break
            else:
                break
    return check


def mainmenu():
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.blit(mainmenu_background, (0, 0))
        Button(mainmenu_start, 405, 250, 150, 80, mainmenu_start_click, 380, 235, game)
        Button(mainmenu_explain, 405, 350, 150, 80, mainmenu_explain_click, 380, 335, explain)
        Button(mainmenu_finish, 405, 450, 150, 80, mainmenu_finish_click, 380, 435, finishgame)

        pygame.display.update()
        clock.tick(15)


def game():
    gameexit = False
    player_turn = 1
    there_is[3][3] = 1
    there_is[3][4] = 2
    there_is[4][3] = 2
    there_is[4][4] = 1

    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        count_player1 = 0
        count_player2 = 0
        gameDisplay.blit(game_background, (0, 0))  # 배경
        gameDisplay.blit(game_player_turn, (670, 0))
        gameDisplay.blit(game_score, (670, 250))
        gameDisplay.blit(game_player1, (670, 393))
        gameDisplay.blit(game_player2, (670, 495))
        for i in range(8):
            for j in range(8):
                if there_is[i][j] == 1:
                    gameDisplay.blit(game_player1, (53 + (i * 70), 50 + (j * 70)))
                    count_player1 += 1
                elif there_is[i][j] == 2:
                    gameDisplay.blit(game_player2, (53 + (i * 70), 50 + (j * 70)))
                    count_player2 += 1

        score(count_player1, count_player2)

        if player_turn == 1:
            gameDisplay.blit(game_player1, (760, 170))
            player1 = Player(game_player1, player_turn)
            player_turn = player1.turn
        else:
            gameDisplay.blit(game_player2, (760, 170))
            player2 = Player(game_player2, player_turn)
            player_turn = player2.turn
        pygame.display.update()
        if count_player1 + count_player2 == 64:
            gameDisplay.blit(game_finish, (150, 100))
            if count_player1 > count_player2:
                gameDisplay.blit(game_player1, (450, 300))
            elif count_player2 < count_player2:
                gameDisplay.blit(game_player2, (450, 300))
            else:
                gameDisplay.blit(game_player1, (350, 300))
                gameDisplay.blit(game_player2, (550, 300))
            time.sleep(5)
            mainmenu()

        clock.tick(60)


def retry():
    pass


def score(player1, player2):
    font = pygame.font.SysFont("a두리둥실", 60)
    player1_score = font.render(str(player1), True, Red)
    player2_score = font.render(str(player2), True, Red)
    gameDisplay.blit(player1_score, (750, 400))
    gameDisplay.blit(player2_score, (750, 500))


def explain():
    pass


def finishgame():
    pygame.quit()
    sys.exit()


mainmenu()
game()
