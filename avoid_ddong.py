import pygame
import sys
import random
import os
import time

# pygame import 후 무조건 init() 수행.
pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 창 크기 설정
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# 60프레임마다 도시할 점수 Font
game_font = pygame.font.Font(None, 40)
# 현재 파일의 경로 가져오기.
current_path = os.path.dirname(__file__)

# 게임 배경 이미지 로드
background_path = "background_black.png"
background = pygame.image.load(os.path.join(current_path, background_path))

# 하준이 사진 세팅
hajun_path = "hajun.png"
hajun = pygame.image.load(os.path.join(current_path, hajun_path))
hajun_pos_x = 50

# 하율이 사진 세팅
hayul_path = "hayul.png"
hayul = pygame.image.load(os.path.join(current_path, hayul_path))
hayul_pos_x = 350

# 캐릭터 초기값 세팅
char_path = "hayul.png"
char = pygame.image.load(os.path.join(current_path, char_path))
char_size = char.get_rect().size
char_width = char_size[0]
char_height = char_size[1]
char_pos_x = SCREEN_WIDTH / 2
char_pos_y = SCREEN_HEIGHT - char_height

# 똥 초기값 세팅
ddong_path = "ddong.png"
ddong = pygame.image.load(os.path.join(current_path, ddong_path))
ddong_size = ddong.get_rect().size
ddong_width = ddong_size[0]
ddong_height = ddong_size[1]
ddong_pos_x = random.randint(0, SCREEN_WIDTH - ddong_width)
ddong_pos_y = 0
ddong_speed = 5

pos_x = 0   # 캐릭터 최초 위치
span = 0.5  # 좌, 우 키 누를때 증감수치

# 캐릭터 선택할 똥 위치
select_ddong_pos_x = SCREEN_WIDTH/2 - ddong_width/2
change_x = 0 # 캐릭터 선택할 똥 증감변수

# 점수 증가 아이템 세팅
item_list = ["diamond.png", "diagem.png", "gemstone.png", "heart.png", "lose.png", "bluegem.png"]
randnum = random.randint(0, len(item_list)-1)
item = pygame.image.load(os.path.join(current_path, item_list[randnum]))
item_pos_x = SCREEN_WIDTH / 2
item_pos_y = 0
item_speed = 5
itemscore = 0

# 게임 동작에 관련된 Flag
program_running = True
game_running = False
start_flag = False

# 게임이 준비시간 제공 함수 ( 제공할 시간을 파라미터로 전송 )
def set_timer(timer):
    while (timer != 0):
        timer_font = pygame.font.SysFont("malgungothic", 50)
        text = timer_font.render(f"{timer}", True, (0, 255, 0))
        SURFACE.fill(BLACK)
        SURFACE.blit(text, (SCREEN_WIDTH/2-20, SCREEN_HEIGHT/2-20))
        pygame.display.update()
        timer -= 1
        time.sleep(1)
        if timer == 0:
            text = timer_font.render("Start!!!", True, (0, 255, 0))
            SURFACE.fill(BLACK)
            SURFACE.blit(text, (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2-20))
            pygame.display.update()
            time.sleep(1)

# 게임 초기화면 설정.
while start_flag == False:
     start_font = pygame.font.SysFont("malgungothic", 25)
     SURFACE.fill(BLACK)
     SURFACE.blit(ddong, (SCREEN_WIDTH / 2 - ddong_width / 2, 100))
     start_text = start_font.render("똥피하기 게임을 시작합니다.", True, (0, 255, 0))
     SURFACE.blit(start_text, (50, 220))
     start_text = start_font.render("\"게임할 친구를 선택하세요..\"", True, (0, 255, 0))
     SURFACE.blit(start_text, (50, 270))
     SURFACE.blit(hajun, (50, 500))
     SURFACE.blit(ddong, (select_ddong_pos_x, 500))
     SURFACE.blit(hayul, (350, 500))
     pygame.display.update()
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False
            pygame.quit()
            sys.exit()
        # 왼쪽, 오른쪽 키보드를 눌러 똥 위치 이동.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x -= 0.5
            elif event.key == pygame.K_RIGHT:
                change_x += 0.5
        if event.type == pygame.KEYUP:
                change_x = 0

     select_ddong_pos_x += change_x

    # 왼쪽으로 똥을 이동하면 하준이, 오른쪽으로 이동하면 하율이가 선택된다.
     if select_ddong_pos_x <= hajun_pos_x + char_width:
         char_path = hajun_path
         char = pygame.image.load(os.path.join(current_path, char_path))
         set_timer(5)
         game_running = True
         start_flag = True
     elif select_ddong_pos_x + char_width >= hayul_pos_x:
         char_path = hayul_path
         char = pygame.image.load(os.path.join(current_path, char_path))
         set_timer(5)
         game_running = True
         start_flag = True

# 점수 계산을 위한 시간계산
start_tick = pygame.time.get_ticks()

while program_running:
    while game_running:
        # 게임이 동작중일때의 반복문
        dt = CLOCK.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            # 게임 동작중일때 왼쪽/오른쪽 키를 누르면 pos_x값을 증감
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pos_x -= span
                elif event.key == pygame.K_RIGHT:
                    pos_x += span
            # 왼쪽/오른쪽 키를 떼면 pos_x는 그대로..
            if event.type == pygame.KEYUP:
                pos_x = 0

        # 증감한 pos_x값을 캐릭터 위치에 더해줌
        char_pos_x += pos_x * dt
        # 똥 y값에 speed를 더해서 떨어지는것처럼 보이게함.
        ddong_pos_y += ddong_speed
        # 아이템도 똥과 같이 떨어지는것처럼 처리
        item_pos_y += item_speed

        # 똥이 화면을 넘어갔을때 최상단으로 올리고 x값을 랜덤하게 변경
        # 화면 넘어갈때마다 점점 똥 speed를 올리도록 구현.
        if ddong_pos_y > SCREEN_HEIGHT:
            ddong_pos_y = 0
            ddong_pos_x = random.randint(0, SCREEN_WIDTH - ddong_width)
            ddong_speed += 0.3

        # 점수증가 아이템이 화면을 넘어갔을때 최상단으로 올리고 x값을 랜덤하게..
        # 화면 넘어갈때마다 새로운 아이템이미지로 변경하고 아이템 속도는 고정.
        if item_pos_y > SCREEN_HEIGHT:
            item_pos_y = 0
            item_pos_x = random.randint(0, SCREEN_WIDTH - ddong_width)
            randnum = random.randint(0, len(item_list)-1)
            item = pygame.image.load(os.path.join(current_path, item_list[randnum]))

        # 화면이 오른쪽, 왼쪽으로 넘어가지 않도록 처리
        if char_pos_x >= SCREEN_WIDTH - char_size[0]:
            char_pos_x = SCREEN_WIDTH - char_size[0]

        if char_pos_x <= 0:
            char_pos_x = 0

        # 충돌 판단을 위한 똥 영역 추출
        ddong_rect = ddong.get_rect()
        ddong_rect.left = ddong_pos_x
        ddong_rect.top = ddong_pos_y

        # 충돌 판단을 위한 캐릭터 영역 추출
        char_rect = char.get_rect()
        char_rect.left = char_pos_x
        char_rect.top = char_pos_y

        # 점수 증가를 위한 아이템 영역 추출
        item_rect = item.get_rect()
        item_rect.left = item_pos_x
        item_rect.top = item_pos_y

        # 캐릭터와 똥이 충돌하면 게임 오버
        if char_rect.colliderect(ddong_rect):
            game_running = False

        # 캐릭터와 점수 아이템이 충돌하면 점수 5점 증가
        if char_rect.colliderect(item_rect):
            itemscore += 5
            item_pos_y = 0
        
        # 시간을 계산하여 점수로 환산
        current_tick = pygame.time.get_ticks()
        elapsed_time = (current_tick - start_tick)/1000
        score = game_font.render(str(int(elapsed_time) + itemscore), True, (0, 255, 255))

        # 배경, 캐릭터, 똥, 아이템, 점수를 화면에 도시.
        SURFACE.blit(background, (0,0))
        SURFACE.blit(char, (char_pos_x, char_pos_y))
        SURFACE.blit(ddong, (ddong_pos_x, ddong_pos_y))
        SURFACE.blit(item, (item_pos_x, item_pos_y))
        SURFACE.blit(score, (10, 10))
        # 화면 갱신
        pygame.display.update()

    # 게임이 종료 되었을때의 반복문.
    text_font = pygame.font.SysFont("malgungothic", 40)

    if char_path.__contains__("hajun"):
        text = text_font.render(f"하준이 점수는 {str(int(elapsed_time)+ itemscore)} 점 !!", True, (0, 255, 255))
        ddong_char_path = "hajun_ddong.png"
    elif char_path.__contains__("hayul"):
        text = text_font.render(f"하율이 점수는 {str(int(elapsed_time)+ itemscore)} 점 !!", True, (0, 255, 255))
        ddong_char_path = "hayul_ddong.png"

    # 똥 맞은 이미지
    ddong_char = pygame.image.load(os.path.join(current_path, ddong_char_path))
    ddong_char_size = ddong_char.get_rect().size
    ddong_char_width = ddong_char_size[0]

    SURFACE.fill(BLACK)
    #SURFACE.blit(char, (SCREEN_WIDTH / 2 - ddong_width / 2, 150))
    SURFACE.blit(ddong_char, (SCREEN_WIDTH / 2 - ddong_char_width / 2, 50))
    SURFACE.blit(text, (10, 450))
    text_font = pygame.font.SysFont("malgungothic", 25)
    text = text_font.render("다시 도전하려면 아무키나 누르세요..!!", True, (0, 255, 255))
    SURFACE.blit(text, (10, 520))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            game_running = True
            ddong_pos_x = random.randint(0, SCREEN_WIDTH - ddong_width)
            ddong_pos_y = 0
            ddong_speed = 5
            char_pos_x = SCREEN_WIDTH / 2
            char_pos_y = SCREEN_HEIGHT - char_height
            pos_x = 0   # 캐릭터 최초 위치
            span = 0.5  # 좌, 우 키 누를때 증감수치
            itemscore = 0
            start_tick = pygame.time.get_ticks()
