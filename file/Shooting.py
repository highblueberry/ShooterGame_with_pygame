import pygame
import random

# pygame 초기화 및 디스플레이 설정
pygame.init()
background = pygame.display.set_mode((700, 1000))
pygame.display.set_caption("Protect")

# 이미지 불러오기
image_background = pygame.image.load('space.png').convert_alpha()
image_player = pygame.image.load('player.png').convert_alpha()
image_missile = pygame.image.load('missile.png').convert_alpha()
image_enemy = pygame.image.load('enemy.png').convert_alpha()
image_enemy_general = pygame.image.load('enemy_general.png').convert_alpha()
image_enemy_missile = pygame.image.load('enemy_attack.png').convert_alpha()
image_health = pygame.image.load('health.png').convert_alpha()
image_heal_potion = pygame.image.load('heal_potion.png').convert_alpha()
image_enemy_boss = pygame.image.load('enemy_boss.png').convert_alpha()



# 이미지의 가로, 세로 크기 구하기
size_bg_width = background.get_size()[0]
size_bg_height = background.get_size()[1]

size_player_width = image_player.get_rect().size[0]
size_player_height = image_player.get_rect().size[1]

size_enemy_width = image_enemy.get_rect().size[0]
size_enemy_height = image_enemy.get_rect().size[1]

size_enemy_general_width = image_enemy_general.get_rect().size[0]
size_enemy_general_height = image_enemy_general.get_rect().size[1]

size_enemy_boss_width = image_enemy_boss.get_rect().size[0]
size_enemy_boss_height = image_enemy_boss.get_rect().size[1]

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

# 보스의 위치 설정
x_pos_boss = size_bg_width/2 - size_enemy_boss_width/2
y_pos_boss = size_enemy_boss_height -300

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
enemies_random_move = []
enemy_speed = 0.05 # 적군 이동 속도
enemies_general_move = []
enemies_general_random_move = []
enemy_general_speed = 0.07

rect_enemy = [] # 충돌 감지를 위한 rect 배열
rect_enemy_general = []
rect_enemy_boss = []

hp_enemy = [] # 적군 체력
hp_enemy_general = []
hp_enemy_boss = 0

rect_enemy_boss = image_enemy_boss.get_rect()
rect_enemy_boss.topleft = (x_pos_boss, y_pos_boss)

boss_phase = False # True로 변하면 보스전 시작
pattern_level = 1 # 보스 패턴 구별을 위한 변수

killed = 0 # 처치한 적군의 수

# 미사일관련 변수
missiles = [] # 발사한 미사일 저장
rect_missile = [] # 충돌 감지를 위한 rect 배열

# 적 미사일관련 변수
boss_missile_time = 0 # 보스 미사일 발사주기
boss_missile_random_time = 800 # 보스 미사일 발사주기
enemy_missile_time = 0 # 적군 미사일 발사주기
enemy_missile_random_time = random.randint(100, 400) # 적군의 첫 번째 미사일 발사주기
enemy_missiles = [] # 발사한 적군 미사일 저장
rect_enemy_missile = [] # 충돌 감지를 위한 rect 배열

# 플레이 화면 관련 변수
score = 0 
font_score = pygame.font.Font(None, 36) # 폰트는 기본으로 지정
font_game_over = pygame.font.SysFont(None,100)
font_game_win = pygame.font.SysFont(None,100)

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
    
# 적군 대장기 소환 함수
def spawn_enemy_general():
    global size_bg_width
    global size_bg_height
    global size_enemy_general_width
    global size_enemy_general_height
    
    enemy_x = random.randint(0, size_bg_width - size_enemy_general_width)
    enemy_y = size_enemy_general_height
    enemies_general_move.append([enemy_x, enemy_y])
    
    # 적이 어디로 움직직일지 정하는 변수를 리스트에 넣어서 관리
    enemies_general_random_move.append([random.randrange(0, size_bg_height - size_enemy_general_height) , random.randrange(0, size_bg_width - size_enemy_general_width)])
    
    # 적군을 소환할 때마다 rect 배열에 추가
    rect_enemy_general.append(image_enemy_general.get_rect())
    
    # 적군의 기본 체력은 일반기의 두배인 14
    hp_enemy_general.append(14)

# 적군 이동방향 설정 함수
def initialize_enemy_random_move():
    global enemies_random_move
    
    for i in range(len(enemies_random_move)):
        enemies_random_move[i][0] = random.randint(0, size_bg_width - size_enemy_width)
        enemies_random_move[i][1] = random.randint(round(enemies_move[i][1]), size_bg_height - size_enemy_height - 300)
        
# 적군 대장기 이동방향 설정 함수  
def initialize_enemy_general_random_move():
    global enemies_general_random_move
    
    for i in range(len(enemies_general_random_move)):
        enemies_general_random_move[i][0] = random.randint(0, size_bg_width - size_enemy_general_width)
        enemies_general_random_move[i][1] = random.randint(round(enemies_general_move[i][1]), size_bg_height - size_enemy_general_height - 300)
        
# 적군을 그리기 위한 함수
def draw_enemies():
    for enemy in enemies_move:
        background.blit(image_enemy, (enemy[0], enemy[1]))
        
# 적군 대장기 그리기 함수
def draw_enemies_general():
    for enemy in enemies_general_move:
        background.blit(image_enemy_general, (enemy[0], enemy[1]))
        
# 적군 격추시 발동되는 함수
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
    
# 적군 대장기 격추시 발동되는 함수
def enemy_general_dead(id):
    # 적군 대장기는 격추시 무조건 아이템 생성
    make_heal_potion(enemies_general_move[id]) 
    
     # 파괴된 적군과 관련된 정보는 모두 제거
    enemies_general_move.remove(enemies_general_move[id])
    rect_enemy_general.remove(rect_enemy_general[id])
    enemies_general_random_move.remove(enemies_general_random_move[id])
    hp_enemy_general.remove(hp_enemy_general[id])
    
# 게임 시작
game_win = False
game_over = False
play = True 
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            
        if event.type == pygame.KEYDOWN:
                # 플레이어 이동
                if event.key == pygame.K_RIGHT:
                    to_x_player = 0.2
                if event.key == pygame.K_LEFT:
                    to_x_player = -0.2
                if event.key == pygame.K_UP:
                    to_y_player = -0.2
                if event.key == pygame.K_DOWN:
                    to_y_player = 0.2
                    
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
                            x_diff += 40
                                           
                    # 플레이어의 공격 레벨이 3인 경우
                    if player_level >= 3:
                        x_diff = -30
                        for i in range(3):
                            x_pos_missile = x_pos_player + size_missile_width + x_diff
                            y_pos_missile = y_pos_player + size_missile_height
                            missiles.append([x_pos_missile, y_pos_missile])
                            rect_missile.append(image_missile.get_rect())
                            x_diff += 40
        
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
    elif(killed <= 20): # 처치한 적군의 수가 11기가 넘으면 적 장군선이 출현하기 시작
        if pygame.time.get_ticks() % 1000 == 0:
            spawn_enemy()
            spawn_enemy_general()
            initialize_enemy_random_move()
            initialize_enemy_general_random_move()
    else: # 일정 수의 적군을 격추하면 보스 소환 또한 보스 패턴에 방해되지 않도록 적군은 이동을 멈춘다.
        if boss_phase == False:
            hp_enemy_boss = 400
            boss_phase = True    
        initialize_enemy_random_move()
        initialize_enemy_general_random_move()
    
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
    
    # 랜덤으로 정해진 이동방향으로 적군 이동
    for i in range(len(enemies_move)):
        if enemies_random_move[i][0] > enemies_move[i][0]:
            enemies_move[i][0] += enemy_speed
            if enemies_random_move[i][1] > enemies_move[i][1]:
                enemies_move[i][1] += enemy_speed
            
        elif enemies_random_move[i][0] < enemies_move[i][0]:
            enemies_move[i][0] -= enemy_speed
            if enemies_random_move[i][1] > enemies_move[i][1]:
                enemies_move[i][1] += enemy_speed      
    
    # 랜덤으로 정해진 이동방향으로 적군 대장기 이동
    for i in range(len(enemies_general_move)):
        if enemies_general_random_move[i][0] > enemies_general_move[i][0]:
            enemies_general_move[i][0] += enemy_general_speed
            if enemies_general_random_move[i][1] > enemies_general_move[i][1]:
                enemies_general_move[i][1] += enemy_general_speed
            
        elif enemies_general_random_move[i][0] < enemies_general_move[i][0]:
            enemies_general_move[i][0] -= enemy_general_speed
            if enemies_general_random_move[i][1] > enemies_general_move[i][1]:
                enemies_general_move[i][1] += enemy_general_speed 
                
              
    # 적군 이동 후 충돌확인을 위해 topleft 변수 갱신
    for i in range(len(enemies_move)):
        rect_enemy[i].topleft = (enemies_move[i][0], enemies_move[i][1])
        
    for i in range(len(enemies_general_move)):
        rect_enemy_general[i].topleft = (enemies_general_move[i][0], enemies_general_move[i][1])
        
    # 체력포션의 파괴된 적군의 위치에서 아래로 쭉 떨어짐
    for i in range(len(heal_potion_move)):
        heal_potion_move[i][1] += 0.18
        rect_heal_potion[i].topleft = (heal_potion_move[i][0], heal_potion_move[i][1])
        
        #체력 포션이 배경 밖으로 넘어가면 삭제
        if heal_potion_move[i][1] > size_bg_height:
            heal_potion_move.remove(heal_potion_move[i])
            rect_heal_potion.remove(rect_heal_potion[i])
            break

    # 스코어를 출력하기 위한 text 생성
    text = font_score.render(f"{score}", True, (255, 255, 255)) # 색상은 흰색
    rect_text = text.get_rect()

    # 이미지 그리기
    background.blit(image_background, (0,0))
    background.blit(image_player, (x_pos_player, y_pos_player))
    # 체력바 그리기
    draw_health()
    # score 그리기
    background.blit(text, (size_bg_width - rect_text.size[0]- 10, rect_text.size[1]-10))
    # 적군 그리기
    draw_enemies()
    draw_enemies_general()
    if boss_phase:
        background.blit(image_enemy_boss, (x_pos_boss, y_pos_boss))
    # 체력 포션 그리기
    for i in range(len(heal_potion_move)):
        background.blit(image_heal_potion, (heal_potion_move[i][0], heal_potion_move[i][1]))
        
    for i in range(len(heal_potion_move)):
        if rect_heal_potion[i].colliderect(rect_player):
            
            # 체력이 다 차지 않은 상태에서는 물약을 먹으면 채력만 회복
            if hp_player < 5:
                hp_player += 1
            # 체력이 다 찬 상태에서 물약을 먹으면 플레이어 공격 레벨 증가
            elif hp_player == 5:
                if player_level < 3: # 플레이어 레벨은 최대 3으로 제한 
                    player_level += 1
                # 체력도 풀이고 플레이어 레벨도 최종일 떄 물약을 먹으면 추가 score 증정
                else:
                    score += 10000
           
            heal_potion_move.remove(heal_potion_move[i])
            rect_heal_potion.remove(rect_heal_potion[i])
            break
    
    
    # 적군 미사일 발사
    if(boss_phase == False):
        enemy_missile_time += 1
        if enemy_missile_time == enemy_missile_random_time:
            enemy_missile_random_time = random.randint(700, 1400)
            enemy_missile_time = 0
            
            for i in range(len(enemies_move)):
                x = enemies_move[i][0] + size_enemy_missile_width
                enemy_missiles.append([x, enemies_move[i][1] + size_enemy_height])
                # 발사한 적군 미사일 충돌 감지를 위해 rect배열에 저장
                rect_enemy_missile.append(image_enemy_missile.get_rect())   
                
            for i in range(len(enemies_general_move)):
                x = enemies_general_move[i][0] + size_enemy_missile_width
                enemy_missiles.append([x, enemies_general_move[i][1] + size_enemy_general_height])
                # 발사한 적군 미사일 충돌 감지를 위해 rect배열에 저장
                rect_enemy_missile.append(image_enemy_missile.get_rect()) 
    
    
    if(boss_phase):         
        boss_missile_time += 1     
        if boss_missile_time == boss_missile_random_time:
            
            # 보스 패턴은 6가지로 나뉜다.
            
            # 맵 0 ~ 1/4지점 일자 총알
            if (pattern_level % 6 == 1):
                boss_missile_random_time = 900
                boss_missile_time = 0
            
                x_diff = 0
                for i in range(15):
                    x = x_pos_boss + 20 + x_diff
                    enemy_missiles.append([x, y_pos_boss + size_enemy_height+30])
                    
                    rect_enemy_missile.append(image_enemy_missile.get_rect())
                    x_diff -= 12  
                pattern_level = random.randint(1,6)
            
            # 맵 1/4 ~ 2/4지점 일자 총알
            elif(pattern_level % 6 == 2):
                boss_missile_random_time = 900
                boss_missile_time = 0
                
                x_diff = 0
                for i in range(15):
                    x = x_pos_boss + 20 + x_diff
                    enemy_missiles.append([x, y_pos_boss + size_enemy_height+30])
                    
                    rect_enemy_missile.append(image_enemy_missile.get_rect())
                    x_diff += 12  
                pattern_level = random.randint(1,6)
            
            # 맵 2/4 ~ 3/4지점 일자 총알
            elif(pattern_level % 6 == 3):
                boss_missile_random_time = 900
                boss_missile_time = 0
                
                x_diff = 0
                for i in range(15):
                    x = x_pos_boss + x_pos_boss + x_diff
                    enemy_missiles.append([x, y_pos_boss + size_enemy_height+30])
                    
                    rect_enemy_missile.append(image_enemy_missile.get_rect())
                    x_diff += 12  
                pattern_level = random.randint(1,6)
            
            # 맵 3/4 ~ 4/4지점 일자 총알
            elif(pattern_level % 6 == 4):
                boss_missile_random_time = 900
                boss_missile_time = 0
                
                x_diff = 0
                for i in range(15):
                    x = x_pos_boss + x_pos_boss + x_pos_boss + x_diff
                    enemy_missiles.append([x, y_pos_boss + size_enemy_height+30])
                    
                    rect_enemy_missile.append(image_enemy_missile.get_rect())
                    x_diff += 12  
                pattern_level = random.randint(1,6)
                
            # 맵 0 ~ 3/4지점 일자 총알    
            elif(pattern_level % 6 == 5):
                boss_missile_random_time = 900
                boss_missile_time = 0
                
                x_diff = 0
                for i in range(40):
                    x = 0 + x_diff
                    enemy_missiles.append([x, y_pos_boss + size_enemy_height+30])
                    
                    rect_enemy_missile.append(image_enemy_missile.get_rect())
                    x_diff += 12  
                pattern_level = random.randint(1,6)
            
            # 맵 1/4 ~ 4/4지점 일자 총알
            elif(pattern_level % 6 == 0):
                boss_missile_random_time = 900
                boss_missile_time = 0
                
                x_diff = 0
                for i in range(40):
                    x = size_bg_width + x_diff
                    enemy_missiles.append([x, y_pos_boss + size_enemy_height+30])
                    
                    rect_enemy_missile.append(image_enemy_missile.get_rect())
                    x_diff -= 12  
                pattern_level = random.randint(1,6)
    
    
    # 적군과 플레이어의 기체가 직접 부딪혔을 경우 체력 감소
    for rect in rect_enemy:
        if rect.colliderect(rect_player):
            hp_player -= 1
        
    for rect in rect_enemy_general:
        if rect.colliderect(rect_player):
            hp_player -= 1
        
    if rect_enemy_boss.colliderect(rect_player):
            hp_player -= 1
    
    
    
    # 발사한 미사일 그리기
    if len(missiles):
        for missile in missiles:
            i = missiles.index(missile)
            missile[1] -= 0.45
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
                        score += 1000
                        killed += 1
                        enemy_dead(j)
                    break
                
            # 적군 대장기가 플레이어의 미사일에 맞으면 체력감소
            for j in range(len(rect_enemy_general)):
                if(rect_missile[i].colliderect(rect_enemy_general[j])):
                    missiles.remove(missile)
                    rect_missile.remove(rect_missile[i])
                    hp_enemy_general[j] -= 1
                    if(hp_enemy_general[j] <= 0):
                        score += 5000
                        killed += 1
                        enemy_general_dead(j)
                    break
            
            if boss_phase:
                # 보스가 플레이어의 미사일에 맞으면 체력감소
                if(rect_missile[i].colliderect(rect_enemy_boss)):
                    missiles.remove(missile)
                    rect_missile.remove(rect_missile[i])
                    hp_enemy_boss -= 1
                    if(hp_enemy_boss == 0):
                        score += 100000
                        
                        # 보스를 격추하면 game win
                        game_win = True
                        gamewin = "Game Win!"
                
                 
            # 미사일이 화면 밖을 벗어나면 삭제       
            if missile[1] <= 0:
                missiles.remove(missile)
                rect_missile.remove(rect_missile[i])
                        
    # 적군이 발사한 미사일 그리기
    if len(enemy_missiles):
        for missile in enemy_missiles:
            i = enemy_missiles.index(missile)
            missile[1] += 0.17
            background.blit(image_enemy_missile, (missile[0], missile[1]))
            
            # topleft값 갱신
            rect_enemy_missile[i].topleft = (missile[0], missile[1])    
    
            # 플레이어가 적군의 미사일을 맞으면 체력 감소
            if rect_enemy_missile[i].colliderect(rect_player):
                enemy_missiles.remove(missile)
                rect_enemy_missile.remove(rect_enemy_missile[i])
                hp_player -= 1
                
                # 플레이어의 체려이 0이 되면 game over
                if hp_player <= 0:
                    game_over = True
                    gameover = "Game Over"

            # 미사일이 화면 밖을 벗어나면 삭제
            if missile[1] >= size_bg_height:
                enemy_missiles.remove(missile)
                rect_enemy_missile.remove(rect_enemy_missile[i])
                
    # hp를 모두 잃고 game over의 경우 텍스트 출력   
    if game_over:
        text_game_over = font_game_over.render(gameover, True, (255,0,0))
        
        # 스코어를 보여주기 위해 폰트 재지정
        font_score = pygame.font.Font(None, 100) # 폰트는 기본으로 지정
        text = font_score.render(f"{score}", True, (255, 255, 255)) # 색상은 흰색
        
        size_text_width = text_game_over.get_rect().size[0]
        size_text_height = text_game_over.get_rect().size[1]
        
        size_score_width = text.get_rect().size[0]
        size_score_height = text.get_rect().size[1]
        
        x_pos_text = size_bg_width/2 - size_text_width/2
        y_pos_text = size_bg_width/2 - size_text_height/2
        
        x_pos_score = size_bg_width/2 - size_score_width/2
        y_pos_score = size_bg_width/2 + size_text_height + size_score_height/2
        
        background.blit(text_game_over, (x_pos_text, y_pos_text))
        background.blit(text, (x_pos_score, y_pos_score))
        pygame.display.update()
        pygame.time.delay(10000)
        play = False
        
    # 보스를 격추하고 game win의 텍스트 출력
    if game_win:
        text_game_win = font_game_win.render(gamewin, True, (255,0,0))
        
        # 스코어를 보여주기 위해 폰트 재지정
        font_score = pygame.font.Font(None, 100) # 폰트는 기본으로 지정
        text = font_score.render(f"{score}", True, (255, 255, 255)) # 색상은 흰색
        
        size_text_width = text_game_win.get_rect().size[0]
        size_text_height = text_game_win.get_rect().size[1]
        
        size_score_width = text.get_rect().size[0]
        size_score_height = text.get_rect().size[1]
        
        x_pos_text = size_bg_width/2 - size_text_width/2
        y_pos_text = size_bg_width/2 - size_text_height/2
        
        x_pos_score = size_bg_width/2 - size_score_width/2
        y_pos_score = size_bg_width/2 + size_text_height + size_score_height/2
        
        background.blit(text_game_win, (x_pos_text, y_pos_text))
        background.blit(text, (x_pos_score, y_pos_score))
        pygame.display.update()
        pygame.time.delay(10000)
        play = False
    
    pygame.display.update()        
pygame.quit()