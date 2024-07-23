import pygame
import random


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255,0,255)
YELLOW = (255, 255,0)
CYAN = (0,255,255)

colors = [RED,GREEN,BLUE, PURPLE, YELLOW, CYAN]



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Breaker")


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([100, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT - 50

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.rect.width // 2
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT // 2 - self.rect.height // 2
        self.velocity = [random.choice([-4, 4]), -4]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - self.rect.width:
            self.velocity[0] = -self.velocity[0]
        if self.rect.y <= 0:
            self.velocity[1] = -self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]


class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([75, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()


paddle = Paddle()
all_sprites.add(paddle)


ball = Ball()
all_sprites.add(ball)
balls.add(ball)


for row in range(5):
    for column in range(10):
        block = Block(random.choice(colors), column * 78 + 1, row * 22 + 50)
        all_sprites.add(block)
        blocks.add(block)


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    all_sprites.update()

   
    if pygame.sprite.collide_rect(ball, paddle):
        ball.bounce()

    
    block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
    for block in block_hit_list:
        ball.bounce()

    
    if ball.rect.y >= SCREEN_HEIGHT:
        running = False

   
    screen.fill(BLACK)

    
    all_sprites.draw(screen)

    
    pygame.display.flip()

    
    clock.tick(60)


pygame.quit()
