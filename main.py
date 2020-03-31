import random
import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
# Background and Sound
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)
# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
# Enemy
ufoImg = pygame.image.load('ufo.png')
alienImg = []
enemyX = []
enemyY = []
enemyMoveX = []
enemyMoveY = []
num_of_enemys = 6
for i in range(num_of_enemys):
    alienImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(25, 715))
    enemyY.append(random.randint(25, 300))
    enemyMoveX.append(2)
    enemyMoveY.append(2)
# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletMoveY = 10
bullet_state = "ready"
# GUI
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(playerX, bulletY - 30)
                    bulletX = playerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_RIGHT:
                playerX_change = 0


    screen.fill((0, 191, 255))
    screen.blit(background, (0, 0))

    # Playermovement
    playerX += playerX_change
    if playerX > 715 or playerX < 25:
        playerX_change = 0
    player(playerX, playerY)

    # Enemymovement
    for i in range(num_of_enemys):
        enemy(enemyX[i], enemyY[i], i)
        numberListX = [-2, 0, 2]
        numberListY = [-2, 0, 2]
        if enemyX[i] > 715 or enemyX[i] < 25 or enemyY[i] > 300 or enemyY[i] < 0:
            enemyMoveX[i] = random.choice(numberListX)
            enemyMoveY[i] = random.choice(numberListY)
        enemyX[i] += enemyMoveX[i]
        enemyY[i] += enemyMoveY[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(25, 715)
            enemyY[i] = random.randint(25, 300)

    # Bulletmovement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletMoveY

    # Endgame
    if score_value == 5:
        for i in range(num_of_enemys):
            enemyX[i] = 1000
            enemyY[i] = 1000
            enemyMoveX[i] = 0
            enemyMoveY[i] = 0
            screen.blit(ufoImg, (-75, 100))
            font = pygame.font.Font('freesansbold.ttf', 32)
            ufo = font.render("Super!!", True, (255, 255, 255))
            screen.blit(ufo, (350, 300))

    show_score(textX, textY)
    pygame.display.update()
