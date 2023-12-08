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
image_health = pygame.image.load('health.png')
image_heal_potion = pygame.image.load('heal_potion.png')

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

size_health_width = image_health.get_rect().size[0]
size_health_height = image_health.get_rect().size[1]

size_heal_potion_width = image_heal_potion.get_rect().size[0]
size_heal_potion_height = image_heal_potion.get_rect().size[1]

# player 시작 위치 정하기
x_pos_player = size_bg_width/2 - size_player_width/2
y_pos_player = size_bg_height - size_player_height

x_pos_missile = size_bg_width/2 - size_missile_width/2
y_pos_missile = size_bg_height - size_player_height - size_missile_height


# 플레이어 관련 변수
to_x_player = 0 # 플레이어 움직임 제어 변수
to_y_player = 0

rect_player = image_player.get_rect()
rect_player.topleft = (x_pos_player, y_pos_player)

player_level = 1 # 플레이어의 공격 레벨

hp_player = 5 # 플레이어 체력
x_pos_health = 0 # 플레이어 체력바의 위치

heal_potion_move = [] # 아이템을 저장하는 배열
rect_heal_potion = []


# 적군 관련 변수
enemies_move = [] # 적군 움직임 제어 변수
enemies_to_move = []
enemies_random_move = []
enemy_speed = 0.08 # 적군 이동 속도
rect_enemy = [] # 충돌 감지를 위한 rect 배열

hp_enemy = [] # 적군 체력 

killed = 0 # 처치한 적군의 수

# 미사일관련 변수
missiles = [] # 발사한 미사일 저장
rect_missile = [] # 충돌 감지를 위한 rect 배열

# 적 미사일관련 변수
enemy_missile_time = 0 # 적군 미사일 발사주기
enemy_missile_random_time = random.randint(100, 400) # 적군의 첫 번째 미사일 발사주기
enemy_missiles = [] # 발사한 적군 미사일 저장
rect_enemy_missile = [] # 충돌 감지를 위한 rect 배열

# 체력바를 그려주는 함수
def draw_health():
    global hp_player
    
    if(hp_player == 5):
        background.blit(image_health, (20, size_health_height))
        background.blit(image_health, (45, size_health_height))
        background.blit(image_health, (70, size_health_height))
        background.blit(image_health, (95, size_health_height))
        background.blit(image_health, (120, size_health_height))            
        
    elif(hp_player == 4):
        background.blit(image_health, (20, size_health_height))
        background.blit(image_health, (45, size_health_height))
        background.blit(image_health, (70, size_health_height))
        background.blit(image_health, (95, size_health_height))
        
    elif(hp_player == 3):
        background.blit(image_health, (20, size_health_height))
        background.blit(image_health, (45, size_health_height))
        background.blit(image_health, (70, size_health_height))
        
    elif(hp_player == 2):
        background.blit(image_health, (20, size_health_height))
        background.blit(image_health, (45, size_health_height))
        
    elif(hp_player == 1):
        background.blit(image_health, (20, size_health_height))
    
# 아이템을 그려주는 함수        
def make_heal_potion(position): # 격추된 적군의 위치를 인자로 받아옴
    heal_potion_move.append([position[0], position[1]])
    rect_heal_potion.append(image_heal_potion.get_rect())
    rect_player.topleft = (position[0], position[1])
    
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
    
    # 적군을 소환할 때마다 rect 배열에 추가
    rect_enemy.append(image_enemy.get_rect())
    
    # 적군의 기본 체력은 7    
    hp_enemy.append(7)

# 적군 이동방향을 랜덤으로 변경하는 함수
def initialize_enemy_random_move():
    global enemies_random_move
    
    for i in range(len(enemies_random_move)):
        enemies_random_move[i][0] = random.randint(0, size_bg_width - size_enemy_width)
        enemies_random_move[i][1] = random.randint(round(enemies_move[i][1]), size_bg_height - size_enemy_height - 300)

# 적군을 그리기 위한 함수
def draw_enemies():
    for enemy in enemies_move:
        background.blit(image_enemy, (enemy[0], enemy[1]))
        
def enemy_dead(id): # id : 체력이 0이된 적군의 index
    # 적군을 죽이면 확률로 아이템이 나온다
    item_chance = random.randint(0, 101)
    if(item_chance < 70):
        make_heal_potion(enemies_move[id]) 
    
     # 파괴된 적군과 관련된 정보는 모두 제거
    enemies_move.remove(enemies_move[id])
    rect_enemy.remove(rect_enemy[id])
    enemies_random_move.remove(enemies_random_move[id])
    hp_enemy.remove(hp_enemy[id])
    
    
        

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
                    if player_level == 1:
                        x_pos_missile = x_pos_player + size_missile_width+12
                        y_pos_missile = y_pos_player + size_missile_height
                        missiles.append([x_pos_missile, y_pos_missile])
                        # 발사한 미사일 충돌 감지를 위해 rect배열에 저장
                        rect_missile.append(image_missile.get_rect())
                        
                    # 플레이어의 공격 레벨이 2인 경우
                    if player_level == 2:
                        x_diff = -10
                        for i in range(2):
                            x_pos_missile = x_pos_player + size_missile_width + x_diff
                            y_pos_missile = y_pos_player + size_missile_height
                            missiles.append([x_pos_missile, y_pos_missile])
                            rect_missile.append(image_missile.get_rect())
                            x_diff += 24
                                           
                    # 플레이어의 공격 레벨이 3인 경우
                    if player_level == 3:
                        x_diff = -30
                        for i in range(3):
                            x_pos_missile = x_pos_player + size_missile_width + x_diff
                            y_pos_missile = y_pos_player + size_missile_height
                            missiles.append([x_pos_missile, y_pos_missile])
                            rect_missile.append(image_missile.get_rect())
                            x_diff += 24
        
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    to_x_player = 0
                if event.key == pygame.K_LEFT:
                    to_x_player = 0
                if event.key == pygame.K_UP:
                    to_y_player = 0
                if event.key == pygame.K_DOWN:
                    to_y_player = 0
                    
    # 2초마다 적군 출현 및 적군 이동방향 변경
    if(killed <= 10) :
        if pygame.time.get_ticks() % 2000 == 0:
            spawn_enemy()
            initialize_enemy_random_move()
    else: # 처치한 적군의 수가 5기가 넘으면 적군 스폰타임을 0.5초로 줄인다.
        if pygame.time.get_ticks() % 500 == 0:
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
    # 플레이어 이동 후 충돌확인을 위해 topleft 변수 갱신
    rect_player.topleft = (x_pos_player, y_pos_player)
    
    # 랜덤으로 정해진 적군 이동
    for i in range(len(enemies_move)):
        if enemies_random_move[i][0] > enemies_move[i][0]:
            enemies_move[i][0] += enemy_speed
            if enemies_random_move[i][1] > enemies_move[i][1]:
                enemies_move[i][1] += enemy_speed
            
        elif enemies_random_move[i][0] < enemies_move[i][0]:
            enemies_move[i][0] -= enemy_speed
            if enemies_random_move[i][1] > enemies_move[i][1]:
                enemies_move[i][1] += enemy_speed                
                   
    # 적군 이동 후 충돌확인을 위해 topleft 변수 갱신
    for i in range(len(enemies_move)):
        rect_enemy[i].topleft = (enemies_move[i][0], enemies_move[i][1])
        
    # 체력포션의 파괴된 적군의 위치에서 아래로 쭉 떨어짐
    for i in range(len(heal_potion_move)):
        heal_potion_move[i][1] += 0.18
        rect_heal_potion[i].topleft = (heal_potion_move[i][0], heal_potion_move[i][1])
        
        #체력 포션이 배경 밖으로 넘어가면 삭제
        if heal_potion_move[i][1] > size_bg_height:
            heal_potion_move.remove(heal_potion_move[i])
            rect_heal_potion.remove(rect_heal_potion[i])

    # 이미지 그리기
    background.blit(image_background, (0,0))
    background.blit(image_player, (x_pos_player, y_pos_player))
    #체력바 그리기
    draw_health()
    # 적군 그리기
    draw_enemies()
    # 체력 포션 그리기
    for i in range(len(heal_potion_move)):
        background.blit(image_heal_potion, (heal_potion_move[i][0], heal_potion_move[i][1]))
        
    for i in range(len(heal_potion_move)):
        if rect_heal_potion[i].colliderect(rect_player):
            
            # 체력이 다 차지 않은 상태에서는 물약을 먹으면 채력만 회복
            if hp_player < 5:
                hp_player += 1
            # 체력이 다 찬 상태에서 물약을 먹으면 플레이어 공격 레벨 증가
            else:
                if player_level <= 3: # 플레이어 레벨은 최대 3으로 제한 
                    player_level += 1
                
            heal_potion_move.remove(heal_potion_move[i])
            rect_heal_potion.remove(rect_heal_potion[i])
            break
    
    
    # 적군 미사일 발사
    enemy_missile_time += 1
    if enemy_missile_time == enemy_missile_random_time:
        enemy_missile_random_time = random.randint(700, 1400)
        enemy_missile_time = 0
        
        for i in range(len(enemies_move)):
            x = enemies_move[i][0] + size_enemy_missile_width
            enemy_missiles.append([x, enemies_move[i][1] + size_enemy_height])
            # 발사한 적군 미사일 충돌 감지를 위해 rect배열에 저장
            rect_enemy_missile.append(image_enemy_missile.get_rect())   
    
    # 발사한 미사일 그리기
    if len(missiles):
        for missile in missiles:
            i = missiles.index(missile)
            missile[1] -= 0.3
            background.blit(image_missile, (missile[0], missile[1]))
            
            # topleft값 갱신
            rect_missile[i].topleft = (missile[0], missile[1])
            
            # 적군이 플레이어의 미사일에 맞으면 체력감소
            for j in range(len(rect_enemy)):
                if(rect_missile[i].colliderect(rect_enemy[j])):
                    missiles.remove(missile)
                    rect_missile.remove(rect_missile[i])
                    hp_enemy[j] -= 1
                    if(hp_enemy[j] <= 0):
                        enemy_dead(j)
                    break
                 
            # 미사일이 화면 밖을 벗어나면 삭제       
            if missile[1] <= 0:
                missiles.remove(missile)
                rect_missile.remove(rect_missile[i])
                
                
    # 적군이 발사한 미사일 그리기
    if len(enemy_missiles):
        for missile in enemy_missiles:
            i = enemy_missiles.index(missile)
            missile[1] += 0.2
            background.blit(image_enemy_missile, (missile[0], missile[1]))
            
            # topleft값 갱신
            rect_enemy_missile[i].topleft = (missile[0], missile[1])    
    
            # 플레이어가 적군의 미사일을 맞으면 체력 감소
            if rect_enemy_missile[i].colliderect(rect_player):
                enemy_missiles.remove(missile)
                rect_enemy_missile.remove(rect_enemy_missile[i])
                hp_player -= 1
                
                # 적군의 공격에 맞으면 플레이어 공격 레벨 하락
                if player_level > 1:
                    player_level -= 1

            # 미사일이 화면 밖을 벗어나면 삭제
            if missile[1] >= size_bg_height:
                enemy_missiles.remove(missile)
                rect_enemy_missile.remove(rect_enemy_missile[i])
    
    #print(hp_player)
    pygame.display.update()        
pygame.quit()