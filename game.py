 
import pygame
import sys
import random

#tạo hàm
def draw_floor():
    screen.blit(floor,(floor_x_pos,600))
    screen.blit(floor,(floor_x_pos + 432,600))
#tạo hàm ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-700))
    return bot_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes: 
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768:
            screen.blit(pipe_surface,pipe)
        else:
            filp_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(filp_pipe  ,pipe)
#va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return True
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
#chim bay
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird
#end game
def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(score),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,60))
        screen.blit(score_surface,score_rect)
    if game_state == "over_game":
        score_surface = game_font.render(f"Score : {str(score)}",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,60))
        screen.blit(score_surface,score_rect)

        hight_score_surface = game_font.render(f"Hight score : {str(score)}",True,(255,255,255))
        hight_score_rect = hight_score_surface.get_rect(center = (216,120))
        screen.blit(hight_score_surface,hight_score_rect)
def update_score(score,hight_score):
    if score > hight_score:
        hight_score = score
    return hight_score

pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=512)
pygame.init()
screen=pygame.display.set_mode((432,768))
clock=pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF",40)

#tạo chim bay
gravity = 0.25
bird_movement = 0
game_activi = True
score = 0
hight_score = 0

#hình bg
bg = pygame.image.load("anh1.png").convert()
bg = pygame.transform.scale2x(bg)
floor = pygame.image.load("floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#tạo chim
bird = pygame.image.load("yellowbird-downflap.png").convert_alpha()
brid = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))

#tạo ống
pipe_surface = pygame.image.load("anh222.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface )
pipe_lst = []

#tạo timer
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1300)
pipe_height = [250,300,350]

#tạo màng hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load("message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))

#chèn âm thanh
flap_sound = pygame.mixer.Sound("sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sfx_hit.wav")
score_sound = pygame.mixer.Sound("sfx_point.wav")
count_dow = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_activi:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_activi == False:
                game_activi = True
                pipe_lst.clear()
                bird_rect.center =(100,284)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_lst.extend(create_pipe())
    screen.blit(bg,(0,0))
    if game_activi:
        #chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_activi = check_collision(pipe_lst)

        #ống
        pipe_lst = move_pipe(pipe_lst)
        draw_pipe(pipe_lst)
        score +=1
        score_display("main_game")
        count_dow -= 1
        if count_dow <= 0:
            score_sound.play()
            count_dow = 300
    else:
        screen.blit(game_over_surface,game_over_rect)
        hight_score = update_score(score,hight_score)
        score_display("over_game")
    #sàn
    floor_x_pos =floor_x_pos -1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)