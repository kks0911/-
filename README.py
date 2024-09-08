import pygame
import random
#기본 크기,프레임 블록크기 설정
WIDTH=400
HEIGHT=600
FPS=50
BLOCK_SIZE=8

INIT_POS=(WIDTH//2,HEIGHT-30)
#색깔
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

#pygame 기본설정
pygame.init()
score=0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1952 GAME score: "+ str(score))
clock=pygame.time.Clock()
ship_image = pygame.image.load("컴공동아리/image/spaceship.png")

#스프라이트 그룹
all_sprites=pygame.sprite.Group()
player_bullet=pygame.sprite.Group()
enemy_sprites=pygame.sprite.Group()
enemy_bullet=pygame.sprite.Group()

#총알 클래스
# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self,centerx,centery):
        #sprite를 상속합니다.
        #생성자 받는 데이터로 x,y좌표를 입력받습니다
        #좌표는 현재 플레이어의 위치입니다.
        super().__init__()
        #그룹에 추가
        player_bullet.add(self)
        all_sprites.add(self)
        #크기, 색 설정
        self.image = pygame.Surface([2 , 3])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        #입력
        self.rect.x = centerx
        self.rect.y = centery - 2
        
       
    def update(self):
        self.rect.y-=4
        if self.rect.y<0 : 
            self.kill()
#플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        all_sprites.add(self)
        self.image = pygame.image.load("컴공동아리/image/spaceship.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT-30
        
        #마지막으로 사격한 시간과 딜레이를 계산합니다.
        self.last_shoot=0
        self.shoot_delay=200
        #생명
        self.life = 3
        
    def update(self):
        now = pygame.time.get_ticks()
        #키를 입력받고 움직임,사격
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.x<=0 :
                self.rect.x=0
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
            if self.rect.x >=WIDTH-4:
                self.rect.x=WIDTH-4
        if keys[pygame.K_UP]:
            self.rect.y -= 3
            if self.rect.y<=HEIGHT//2:
                self.rect.y=HEIGHT//2
        if keys[pygame.K_DOWN]:
            self.rect.y += 3
            if self.rect.y >=HEIGHT-8:
                self.rect.y = HEIGHT-8  
        if keys[pygame.K_SPACE]:
            if now-self.last_shoot >= self.shoot_delay:
                self.last_shoot=now
                #스페이스바를 누르면 사격합니다.
                #총알의 생성자로 플레이어의 좌표를 주어야 합니다.
                bullet=Bullet(self.rect.centerx,self.rect.centery)
        #만약 적군의 총알과 부딪히는경우 목숨1을 깎습니다.
        if pygame.sprite.spritecollide(self, enemy_bullet, True):
            self.life -= 1
            if self.life == 0 :
                pygame.quit()
#적군의 총알 클래스
class Enemy_bullet(pygame.sprite.Sprite):
    #적군의 총알은 기본적으로 발사한 적군의 위치에서 생성되어야 합니다.
    #따라서 좌표를 입력받습니다.
    def __init__(self,centerx,centery,y,x):
        super().__init__()
        self.image = pygame.Surface([2,2])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        all_sprites.add(self)
        enemy_bullet.add(self)
        #총알의 위치
        self.rect.x = centerx
        self.rect.y = centery
        #총알의 방향
        self.diry=float(y)
        self.dirx=float(x)
    #업데이트 메소드
    def update(self):
        #총알의 방향에 따라 총알이 움직입니다.
        self.rect.y += float(self.diry)
        self.rect.x -= float(self.dirx)
#총알은 모두 Enemy_bullet 클래스를 상속받습니다.
#총알 1
class BulletT1(Enemy_bullet):
    def __init__(self,centerx,centery,y,x):
        super().__init__(centerx,centery,y,x)
      
    def update(self):
        super().update()
#총알 2
class BulletT2(Enemy_bullet):
    def __init__(self,centerx,centery,y,x):
        super().__init__(centerx,centery,y,x)
        self.image = pygame.Surface([2,3])
        self.image.fill(BLUE)
    def update(self):
        super().update()
#총알 3
class BulletT3(Enemy_bullet):
    def __init__(self,centerx,centery,y,x):
        super().__init__(centerx,centery,y,x)
        self.image = pygame.Surface([2,2])
        self.image.fill(YELLOW)
    def update(self):
        super().update()
#Enemy 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_sprites.add(self)
        all_sprites.add(self)
        self.image = pygame.Surface([BLOCK_SIZE*2, BLOCK_SIZE])
        self.rect = self.image.get_rect()
        #랜덤 위치에 생성
        self.rect.x = random.randint(0,WIDTH-4)
        self.rect.y = random.randint(0,HEIGHT//3)
        #마지막으로 쏜 시간, 총알 클래스변수 , 목숨을 기본적으로 저장합니다
        self.last_shoot=0
        self.bullet_class = None
        self.life = 1
        #속도는 좌,우 랜덤속도를 갖습니다.
        self.speed=random.uniform(-2.5,2.5)
    def update(self):
        #만약 맵 밖으로 나가면 사라집니다.
        if self.rect.x <-10 or self.rect.x>WIDTH:
            self.kill()
        now = pygame.time.get_ticks()
        temp=-500
        #시간이 지나면 방향이 바뀝니다.
        if now-temp>=2000 :
            temp=0
            self.rect.x+= self.speed*-1
            
#모든 적군은 enemy 클래스를 상속받습니다.
class EnemyT1(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE*2, BLOCK_SIZE])
        self.image.fill(RED)
 
        #마지막으로 쏜 시간, 딜레이
        #총알 클래스
        #목숨
        self.last_shoot=0
        self.shoot_delay=900
        self.bullet_class=BulletT1
        self.life=2
    def update(self):
        super().update()
        global score     
        #시간이 지날때마다 총알을 발사합니다.
        now = pygame.time.get_ticks()
        if now - self.last_shoot>=self.shoot_delay :
            self.last_shoot=now
            #총알의 위치로 적군의 위치정보, 사격할 방향을 줍니다
            self.bullet_class(self.rect.centerx,self.rect.centery,4,0)
        if pygame.sprite.spritecollide(self,player_bullet, True) :
            self.life -= 1
            if self.life == 0:
                score+=1
                self.kill()
#두번째 enemy
class EnemyT2(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE*1.5, BLOCK_SIZE*1.5])
        self.image.fill(BLUE)
    
        self.last_shoot=0
        self.shoot_delay=400
        self.bullet_class=BulletT2
        self.life = 3
    def update(self):
        super().update()
        global score
        now = pygame.time.get_ticks()
        if now - self.last_shoot>=self.shoot_delay :
            self.last_shoot=now
            self.bullet_class(self.rect.centerx,self.rect.centery,3,1)
            self.bullet_class(self.rect.centerx,self.rect.centery,3,-1)
        if pygame.sprite.spritecollide(self,player_bullet, True) :
            self.life -= 1
            if self.life == 0:
                score += 2
                self.kill()
#3번째 enemy
class EnemyT3(Enemy):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE*1.5, BLOCK_SIZE*1.5])
        self.image.fill(YELLOW)
  
        self.last_shoot=0
        self.shoot_delay=500
        self.bullet_class=BulletT3
        self.life = 3
    def update(self):
        super().update()
        global score
        now = pygame.time.get_ticks()
        if now - self.last_shoot>= self.shoot_delay :
            self.last_shoot=now
            self.bullet_class(self.rect.centerx-4,self.rect.centery,4,0)
            self.bullet_class(self.rect.centerx+4,self.rect.centery,4,0)
        if pygame.sprite.spritecollide(self,player_bullet, True) :
            self.life -= 1
            if self.life == 0:
                score+=3
                self.kill()
                
def game_over_screen():
    screen.fill(RED)  # 배경색 변경 (원하는 색으로 변경 가능)
    font = pygame.font.Font(None, 72)  # 큰 글씨체 설정
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2-50))
    screen.blit(text, text_rect)

    score_text = font.render("Your Score: " + str(score), True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2+50))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    pygame.time.wait(3000)
    
def game_loop():
    font = pygame.font.Font(None, 36)
    player=Player()
    temp = 0
    while True:
        now = pygame.time.get_ticks()
        #enemy를 자동으로 생성합니다.
        if now-temp >= 300 and now-temp <=310 and len(enemy_sprites.sprites())<=10:
            EnemyT1()
        if now-temp >= 600 and now-temp <=610 and len(enemy_sprites.sprites())<=10:
            EnemyT2()
        if now-temp >= 700 and now-temp <=720 and len(enemy_sprites.sprites())<=10:
            EnemyT3()
        if now-temp>=1200 :
            temp=now
        for event in pygame.event.get():
            if player.life == 0:
                game_over_screen()
                pygame.quit()
                quit()

        # 모든 스프라이트 업데이트 및 그리기
        all_sprites.update()
        all_sprites.draw(screen)

        # 점수 표시
        score_text = font.render("Score: " + str(score), True, WHITE)
        text_rect = score_text.get_rect()
        text_rect.topright = (WIDTH - 10, 10)
        screen.blit(score_text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

game_loop()
       
