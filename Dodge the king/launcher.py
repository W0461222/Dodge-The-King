import pygame, sys
from pygame.display import mode_ok
from pygame.locals import *
import random, time

pygame.init()

# colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 0 , 255)
light_blue = pygame.Color(125, 125, 255)
red = pygame.Color(255, 0, 0)

print("Starting Game:")
print("DATA: Game Loading 6 Assets")

# Display
displaysurf = pygame.display.set_mode((400, 600))
displaysurf.fill(white)
pygame.display.set_caption("Game")

background = pygame.image.load("data/flag.png")
print("DATA: Loading " + str(background))
print("DATA: Done")
end_screen = pygame.image.load("data/end.png")
print("DATA: Loading " + str(end_screen))
print("DATA: Done")

print("DATA: Assets Loaded")
print("DATA: Loading Fonts")
# fonts
font = pygame.font.SysFont("Verderna", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over Nerd", True, black)

# audio
pygame.mixer.music.load('data/background.mp3')

# Debug

print("DATA: Loaded Music And Fonts...")
print("DATA: Sucessfully Loaded")

# others
screen_height = 600
screen_width = 400
speed = 5
increase = 1
score = 0

print("DATA: Loading Display: " + str(screen_height) + " x " + str(screen_width))


# Makes a fixed FPS
FPS = 60
framepersec = pygame.time.Clock()
print("WARNING: FPS Value Set At " + str(FPS) + " (This is not a bug)")
print("DATA: Done Loading")
# Enemys And Objects

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(screen_width, screen_height), 0)

    def move(self):
        global score
        self.rect.move_ip(0, 10)
        if (self.rect.bottom > 600):
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
    
    """def draw(self, surface):
        surface.blit(self.image, self.rect)"""

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            self.rect.move_ip(0, 5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < screen_width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    """def draw(self, surface):
        surface.blit(self.image, self.rect)"""

# setting up sprites
p1 = player()
e1 = enemy()

# creating sprite groups
enemies = pygame.sprite.Group()
enemies.add(e1)
all_sprites = pygame.sprite.Group()
all_sprites.add(p1)
all_sprites.add(e1)

print("DATA: Loaded Sprites")

# User event
inc_speed = pygame.USEREVENT + increase
pygame.time.set_timer(inc_speed, 10000)

pygame.mixer.music.play(-1)

# Start Game Conformation

# game loop
while True:

    displaysurf.blit(background, (0, 0))
    scores = font_small.render(str(score), True, black)
    fps_display = font_small.render("FPS: " + str(FPS), True, black)
    displaysurf.blit(fps_display, (320, 10))
    displaysurf.blit(scores, (10, 10))

    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 2

        if event.type == QUIT:
            print("WARNING: This is Not An Issue.")
            print("WARNING: Crash Handler: Game Forcibly Closed.")
            pygame.quit()
            sys.exit()

    increase += 0.01
    print(str(increase))

    for entity in all_sprites:
        displaysurf.blit(entity.image, entity.rect)
        entity.move()

    # collision
    if pygame.sprite.spritecollideany(p1, enemies):
        displaysurf.blit(background, (0, 0))
        displaysurf.blit(end_screen, (0, 0))
        displaysurf.blit(game_over, (30, 250))
        
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        print("WARNING: Game Closed: Game Over!")
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    framepersec.tick(FPS + increase)
