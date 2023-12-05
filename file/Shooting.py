import pygame
import random

# pygame 초기화 및 디스플레이 설정
pygame.init()
background = pygame.display.set_mode((700, 1000))
pygame.display.set_caption("Protect")

# 이미지 불러오기
image_background = pygame.image.load('space.png')
image_player = pygame.image.load('player.png')
image_missile = pygame.image.load('missile.png')
image_enemy = pygame.image.load('enemy.png')
image_enemy_missile = pygame.image.load('enemy_attack.png')

# 이미지의 가로, 세로 크기 구하기
size_bg_width = background.get_size()[0]
size_bg_height = background.get_size()[1]

size_player_width = image_player.get_rect().size[0]
size_player_height = image_player.get_rect().size[1]

size_enemy_width = image_enemy.get_rect().size[0]
size_enemy_height = image_enemy.get_rect().size[1]

size_enemy_missile_width = image_enemy_missile.get_rect().size[0]
size_enemy_missile_height = image_enemy_missile.get_rect().size[1]

size_missile_width = image_missile.get_rect().size[0]
size_missile_height = image_missile.get_rect().size[1]


# player 시작 위치 정하기
x_pos_player = size_bg_width/2 - size_player_width/2
y_pos_player = size_bg_height - size_player_height

x_pos_missile = size_bg_width/2 - size_missile_width/2
y_pos_missile = size_bg_height - size_player_height - size_missile_height


# 플레이어 움직임 제어 변수
to_x_player = 0
to_y_player = 0

# 적군 움직임 제어 변수
enemies_move = []
enemies_to_move = []
enemies_random_move = []


# 미사일 발사를 위한 변수
missiles = []

# 적 미사일 발사와 발사 주기를 위한 변수
enemy_missile_time = 0
enemy_missile_random_time = random.randint(100, 400)
enemy_missiles = []


# 적군 소환을 위한 함수
def spawn_enemy():
    global size_bg_width
    global size_bg_height
    global size_enemy_width
    global size_enemy_height
    
    enemy_x = random.randint(0, size_bg_width - size_enemy_width)
    enemy_y = size_enemy_height
    enemies_move.append([enemy_x, enemy_y])
    
    # 적이 어디로 움직직일지 정하는 변수를 리스트에 넣어서 관리
    enemies_random_move.append([random.randrange(0, size_bg_height - size_enemy_height) , random.randrange(0, size_bg_width - size_enemy_width)])

# 적군 이동방향을 랜덤으로 변경하는 함수
def initialize_enemy_random_move():
    global enemies_random_move
    
    for i in range(len(enemies_random_move)):
        enemies_random_move[i][0] = random.randint(0, size_bg_width - size_enemy_width)
        enemies_random_move[i][1] = random.randint(round(enemies_move[i][1]), size_bg_height - size_enemy_height)

# 적군을 그리기 위한 함수
def draw_enemies():
    for enemy in enemies_move:
        background.blit(image_enemy, (enemy[0], enemy[1]))


# 게임 시작
play = True 
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            
        if event.type == pygame.KEYDOWN:
                # 플레이어 이동
                if event.key == pygame.K_RIGHT:
                    to_x_player = 0.25
                if event.key == pygame.K_LEFT:
                    to_x_player = -0.25
                if event.key == pygame.K_UP:
                    to_y_player = -0.25
                if event.key == pygame.K_DOWN:
                    to_y_player = 0.25
                    
                # 플레이어 공격    
                if event.key == pygame.K_z:
                    x_pos_missile = x_pos_player + size_missile_width+12
                    y_pos_missile = y_pos_player + size_missile_height
                    missiles.append([x_pos_missile, y_pos_missile])
        
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    to_x_player = 0
                if event.key == pygame.K_LEFT:
                    to_x_player = 0
                if event.key == pygame.K_UP:
                    to_y_player = 0
                if event.key == pygame.K_DOWN:
                    to_y_player = 0
                    
    # 3초마다 적군 출현 및 적군 이동방향 변경
    if pygame.time.get_ticks() % 3000 == 0:
        spawn_enemy()
        initialize_enemy_random_move()
                    
    
    
    # 플레이어의 움직임을 게임화면 내에서만 움직이도록 제한
    if x_pos_player < 0:
        x_pos_player = 0
    elif x_pos_player > size_bg_width - size_player_width:
        x_pos_player = size_bg_width - size_player_width
    else :        
        x_pos_player += to_x_player
        y_pos_player += to_y_player
    
    # 랜덤으로 정해진 적군 이동
    for i in range(len(enemies_move)):
        if enemies_random_move[i][0] > enemies_move[i][0]:
            enemies_move[i][0] += 0.05
            if enemies_random_move[i][1] > enemies_move[i][1]:
                enemies_move[i][1] += 0.05
            
        elif enemies_random_move[i][0] < enemies_move[i][0]:
            enemies_move[i][0] -= 0.05
            if enemies_random_move[i][1] > enemies_move[i][1]:
                enemies_move[i][1] += 0.05
                         
    # 이미지 그리기
    background.blit(image_background, (0,0))
    background.blit(image_player, (x_pos_player, y_pos_player))
    # 적군 그리기
    draw_enemies()
    
    
    # 적군 미사일 발사
    enemy_missile_time += 1
    if enemy_missile_time == enemy_missile_random_time:
        enemy_missile_random_time = random.randint(700, 1400)
        enemy_missile_time = 0
        
        for i in range(len(enemies_move)):
            x = enemies_move[i][0] + size_enemy_missile_width
            enemy_missiles.append([x, enemies_move[i][1] + size_enemy_height])
    
    
    # 발사한 미사일 그리기
    if len(missiles):
        for missile in missiles:
            missile[1] -= 0.3
            background.blit(image_missile, (missile[0], missile[1]))
            if missile[1] <= 0:
                missiles.remove(missile)
                
    # 적군이 발사한 미사일 그리기
    if len(enemy_missiles):
        for missile in enemy_missiles:
            missile[1] += 0.2
            background.blit(image_enemy_missile, (missile[0], missile[1]))
            if missile[1] >= size_bg_height:
                enemy_missiles.remove(missile)
                
            
    pygame.display.update()        
pygame.quit()