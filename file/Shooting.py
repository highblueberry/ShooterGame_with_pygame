import pygame

# pygame 초기화 및 디스플레이 설정
pygame.init()
background = pygame.display.set_mode((500, 800))
pygame.display.set_caption("Protect")

# 이미지 불러오기
image_background = pygame.image.load("file/image/space.png")
image_player = pygame.image.load("file/image/player.png")
image_missile = pygame.image.load('file/image/missile.png')

# 이미지의 가로, 세로 크기 구하기
size_bg_width = background.get_size()[0]
size_bg_height = background.get_size()[1]

size_player_width = image_player.get_rect().size[0]
size_player_height = image_player.get_rect().size[1]

print("%d %d"%(size_player_width, size_player_height))

size_missile_width = image_missile.get_rect().size[0]
size_missile_height = image_missile.get_rect().size[1]
print("%d %d"%(size_missile_width, size_missile_height))

# player 시작 위치 정하기
x_pos_player = size_bg_width/2 - size_player_width/2
y_pos_player = size_bg_height - size_player_height

x_pos_missile = size_bg_width/2 - size_missile_width/2
y_pos_missile = size_bg_height - size_player_height - size_missile_height


# 플레이어 움직임 제어 변수
to_x_player = 0
to_y_player = 0

# 미사일 발사를 위한 변수
missiles = []

# 적 공격
enemy_missiles = []


# 게임 시작
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
    
    # 플레이어의 움직임을 게임화면 내에서만 움직이도록 제한
    if x_pos_player < 0:
        x_pos_player = 0
    elif x_pos_player > size_bg_width - size_player_width:
        x_pos_player = size_bg_width - size_player_width
    else :        
        
        x_pos_player += to_x_player
        y_pos_player += to_y_player
                         
    # 이미지 그리기
    background.blit(image_background, (0,0))
    background.blit(image_player, (x_pos_player, y_pos_player))

    
    # 발사한 미사일 그리기
    if len(missiles):
        for missile in missiles:
            missile[1] -= 0.3
            background.blit(image_missile, (missile[0], missile[1]))
            if missile[1] <= 0:
                missiles.remove(missile)
                
            
    pygame.display.update()        
pygame.quit()