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
alienImg = []
enemyX = []
enemyY = []
enemyMoveX = []
enemyMoveY = []
num_of_enemies = 12
first_enemyX = 700
for i in range(num_of_enemies):
    alienImg.append(pygame.image.load('enemy.png'))
    enemyX.append(first_enemyX)
    enemyY.append(50)
    enemyMoveX.append(3)
    enemyMoveY.append(3)
    first_enemyX -= 60

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletMoveY = 10
bullet_state = "ready"

# GUI-Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# GUI-GameOver
game_over = False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, b):
    screen.blit(alienImg[b], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enx, eny, bulx, buly):
    distance = math.sqrt((math.pow(enx - bulx, 2)) + (math.pow(eny - buly, 2)))
    if distance < 27:
        return True
    else:
        return False


def isCollisionP(enx, eny, playx, playy):
    distance = math.sqrt((math.pow(enx - playx, 2)) + (math.pow(eny - playy, 2)))
    if distance < 80:
        return True
    else:
        return False


def endgame(var1):
    if var1:
        font_GameOver = pygame.font.Font('freesansbold.ttf', 32)
        text_GameOver = font_GameOver.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text_GameOver, (300, 250))
        show_score(textX, textY)


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
    for i in range(num_of_enemies):
        enemy(enemyX[i], enemyY[i], i)
        enemyX[i] += enemyMoveX[i]
        if enemyX[i] >= 736:
            enemyMoveX[i] = -3
            enemyY[i] += 50
        if enemyX[i] <= 0:
            enemyMoveX[i] = 3
            enemyY[i] += 50

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = 900
            enemyY[i] = 300
            enemyMoveX[i] = 0
            enemyMoveY[i] = 0

    # Bulletmovement
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletMoveY

    # Endgame
    if score_value == 12:
        for i in range(num_of_enemies):
            enemyX[i] = 1000
            enemyY[i] = 1000
            enemyMoveX[i] = 0
            enemyMoveY[i] = 0
            font_WinGame = pygame.font.Font('freesansbold.ttf', 32)
            text_WinGame = font_WinGame.render("Gewonnen!", True, (255, 255, 255))
            screen.blit(text_WinGame, (300, 250))

    # GameOver
    for i in range(num_of_enemies):
        collision1 = isCollisionP(enemyX[i], enemyY[i], playerX, playerY)
        if collision1:
            for d in range(num_of_enemies):
                enemyX[d] = 1000
                enemyY[d] = 1000
                enemyMoveX[d] = 0
                enemyMoveY[d] = 0
                game_over = True
    endgame(game_over)
    show_score(textX, textY)

    pygame.display.update()
