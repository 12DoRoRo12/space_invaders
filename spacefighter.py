import pygame, sys
from random import randint
from pygame import mixer
pygame.init()
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

#ბექგრაუნდის მუსიკა
mixer.music.load("images/background.wav")
mixer.music.play(-1)
#ხმოვანი ეფექტები
shooting = mixer.Sound("images/shooting.wav")
happy_ending = mixer.Sound("images/happy_ending.wav")
unhappy_ending = mixer.Sound("images/unhappy_ending.wav")
#ეკრანის ზომები
width = 970
height = 712
#ეკრანის შექმნა
screen = pygame.display.set_mode((width, height))
#ფონი
background = pygame.image.load("images/background.jpg")
#ფონის გაზრდა
background = pygame.transform.scale(background, (width, height))
#ეკრანის წარწერის შეცვლა
pygame.display.set_caption("Space Fighters")
#აიქონის შეცვლა
icon = pygame.image.load("images/enemy3.png")
pygame.display.set_icon(icon)
class Player():
    def __init__(self, image_path, x, y, life):
        self.player = pygame.image.load(image_path)
        self.player = pygame.transform.scale(self.player, (100, 100))
        self.rect = self.player.get_rect()
        self.x = x
        self.y = y
        self.speed = 0
        self.life = life
    def appearance(self):
        self.rect.center = [self.x, self.y]
        screen.blit(self.player, self.rect)
    def movement(self):
        self.x += self.speed
    def check_borders(self, x1, x2):
        if self.x < x1:
            self.x = x1
        if self.x > x2:
            self.x = x2
class Enemy():
    def __init__(self, image_path, y, speed_x, speed_y, life):
        self.enemy = pygame.image.load(image_path)
        self.enemy = pygame.transform.scale(self.enemy, (100, 100))
        self.enemy = pygame.transform.rotate(self.enemy, 180)
        self.rect = self.enemy.get_rect()
        self.x = randint(100, 870)
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.life = life
    def appearance(self):
        self.rect.center = [self.x, self.y]
        screen.blit(self.enemy, self.rect)
    def movement(self, x1, x2):
        self.x += self.speed_x
        if self.x > x2:
            self.speed_x *= -1
            self.y += self.speed_y
        if self.x < x1:
            self.speed_x *= -1
            self.y += self.speed_y



class Bullet():
    def __init__(self, image_path, x, y, speed, rotate):
        self.bullet = pygame.image.load(image_path)
        self.bullet = pygame.transform.rotate(self.bullet, rotate)
        self.x = x
        self.y = y
        self.rect = self.bullet.get_rect()
        self.speed = speed
        self.fired = False
    def shooting(self, direction):
        if self.fired == True:
            self.y -= self.speed * direction
            self.rect.center = [self.x, self.y]
            screen.blit(self.bullet, self.rect)
        if self.y < 0 or self.y > 700:
            self.fired = False
    def hit_target(self, enemy_rect, enemy_life, own_x, own_y):
        if enemy_rect.collidepoint((self.x, self.y)):
            enemy_life -= 1
            self.fired = False
            self.x = own_x
            self.y = own_y
        return enemy_life


player = Player("images/player.png", 485, 600, 3)
enemy = Enemy("images/enemy3.png", 100, 0.5, 60, 3)
p_bullet = Bullet("images/bullet.png", player.x, player.y, 1, 0)
e_bullet = Bullet("images/bullet.png", enemy.x, enemy.y, 1, 180)
#ქულების გამოტანის ფუნქციონალი
font = pygame.font.Font(None, 30)

def score(player_life, enemy_life):
    text = font.render(f"Pl/En: {player_life}/{enemy_life}", True, (255, 255, 255))
    screen.blit(text, (0, 0))
font1 = pygame.font.Font(None, 90)
def game_over():
    game_over_text = font1.render("Game Over", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=[width/2, height/2])
    screen.blit(game_over_text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()
while True:
    clock.tick(600)
    #ეკრანზე ფონის დაკვრა
    screen.blit(background, (0, 0))
    #სიცოცხლის მაჩვენებელი
    score(player.life, enemy.life)
    #მოთამაშის და მოწინააღმდეგის დახატვა
    player.appearance()
    enemy.appearance()

    player.movement()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.speed = 0.5
            if event.key == pygame.K_LEFT:
                player.speed = -0.5
            if event.key == pygame.K_SPACE and p_bullet.fired == False:
                shooting.play()
                p_bullet.fired = True
                p_bullet.x = player.x
                p_bullet.y = player.y - 50

                e_bullet.x = enemy.x
                e_bullet.y = enemy.y + 50
                e_bullet.fired = True
                shooting.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.speed = 0
    #ამოწმებს მოთამაშე რომ არ გაცდეს ეკრანს
    player.check_borders(50,920)
    #მოწინააღმდეგის მოძრაობა
    enemy.movement(50,920)
    #მოთამაშის მიერ ტყვიის გასროლა
    p_bullet.shooting(1)
    enemy.life = p_bullet.hit_target(enemy.rect, enemy.life, player.x, player.y)
    
    # მოწინააღმდეგის ტყვიის გასროლა
    e_bullet.shooting(-1)
    player.life = e_bullet.hit_target(player.rect, player.life, enemy.x, enemy.y)
    if enemy.life <= 0:
        happy_ending.play()
        screen.blit(background, (0, 0))
        score(player.life, enemy.life)
        game_over()
    #მოწინააღმდეგის ხომალდთან შეჯახება
    if player.rect.collidepoint((enemy.x, enemy.y)):
        unhappy_ending.play()
        screen.blit(background, (0, 0))
        score(player.life, enemy.life)
        game_over()
    # თუ დაგვამარცხეს
    if player.life <= 0:
        unhappy_ending.play()
        screen.blit(background, (0, 0))
        score(player.life, enemy.life)
        game_over()
    pygame.display.update()
