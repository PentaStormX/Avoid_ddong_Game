import pygame
import sys
import random
import os

# pygame import 후 무조건 init() 수행.
pygame.init()

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 창 크기 설정
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# 점수 계산을 위한 시간계산
start_tick = pygame.time.get_ticks()
# 60프레임마다 도시할 점수 Font
game_font = pygame.font.Font(None, 40)
# 현재 파일의 경로 가져오기.
current_path = os.path.dirname(__file__)

# 게임 배경 이미지 로드
background_path = "background.png"
background = pygame.image.load(os.path.join(current_path, background_path))

# 캐릭터 초기값 세팅
char_path = "hajun.png"
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

pos_x = 0   # 캐릭터 좌/우 증감 변수
span = 0.5  # 증감수치

game_running = True     # 게임 동작 flag
program_running = True  # 프로그램 동작 flag

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

        # 증감한 pos_x값과 tick 곱한값이 캐릭터 좌우 위치.
        char_pos_x += pos_x * dt
        # 프레임마다 변하는 똥의 y값 위치
        ddong_pos_y += ddong_speed

        # 똥의 y위치가 창 크기보다 커지면 즉, 화면을 벗어나면
        # 다시 최상위로 올리고 x값 랜덤 조정 후 똥 속도 업!!
        if ddong_pos_y > SCREEN_HEIGHT:
            ddong_pos_y = 0
            ddong_pos_x = random.randint(0, SCREEN_WIDTH - ddong_width)
            ddong_speed += 0.3

        # 캐릭터가 창 우측으로 벗어나지 못하도록 예외처리
        if char_pos_x >= SCREEN_WIDTH - char_size[0]:
            char_pos_x = SCREEN_WIDTH - char_size[0]

        # 캐릭터가 창 좌측으로 벗어나지 못하도록 예외처리
        if char_pos_x <= 0:
            char_pos_x = 0

        # 충돌 판단을 위해 똥의 영역 구하기.
        ddong_rect = ddong.get_rect()
        ddong_rect.left = ddong_pos_x
        ddong_rect.top = ddong_pos_y

        # 충돌 판단을 위해 캐릭터의 영역 구하기.
        char_rect = char.get_rect()
        char_rect.left = char_pos_x
        char_rect.top = char_pos_y

        # 충돌 시 게임 종료.
        if char_rect.colliderect(ddong_rect):
            game_running = False
        
        # 시간계산해서 점수 도시
        current_tick = pygame.time.get_ticks()
        elapsed_time = (current_tick - start_tick)/1000
        score = game_font.render(str(int(elapsed_time)), True, (0, 255, 255))

        # 배경 도시먼저 하고 캐릭터, 똥, 점수를 도시한다.
        # 배경을 나중에 하면 미리 그린 이미지가 사라짐.
        SURFACE.blit(background, (0,0))
        SURFACE.blit(char, (char_pos_x, char_pos_y))
        SURFACE.blit(ddong, (ddong_pos_x, ddong_pos_y))
        SURFACE.blit(score, (10, 10))
        pygame.display.update()
    
    # 게임이 종료 되었을때의 반복문.
    text_font = pygame.font.SysFont("malgungothic", 40)
    if char_path.__contains__("hajun"):
        text = text_font.render(f"하준이 점수는 {str(int(elapsed_time))} 점 !!", True, (0, 255, 255))
    elif char_path.__contains__("hayul"):
        text = text_font.render(f"하율이 점수는 {str(int(elapsed_time))} 점 !!", True, (0, 255, 255))
    # 검은 배경에 점수 도시하고 종료버튼 누르면 프로그램 종료.
    SURFACE.fill((0, 0, 0))
    SURFACE.blit(text, (10, 10))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False
            pygame.quit()
            sys.exit()


