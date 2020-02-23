# this game was inspired by https://www.youtube.com/watch?v=FfWpgLFMI7w
# Icons made by https://www.flaticon.com/authors/photo3idea-studio - > photo3idea_studio at > www.flaticon.com
# Background image: https://pl.freepik.com/darmowe-zdjecie-wektory/kochanie > Kochanie plik wektorowy utworzone przez starline - pl.freepik.com
# Background music from Free Music Archive https://freemusicarchive.org/

# TODO: (0) put doc comments
# TODO: (1) restart game
# TODO: (2) new sounds and images
# TODO: (3) save high score and show list of it after game over
# TODO: (4) refactor code (new file, OOP maybe?)
# TODO: (5) move speed from timer not only loop


import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screenX = 800
screenY = 600
background = pygame.image.load('./include/graphics/bck.png')
screen = pygame.display.set_mode((screenX, screenY))

# background sound
mixer.music.load('./include/sounds/background.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Sarenka Forever')
icon = pygame.image.load('./include/graphics/roe-ico.png')
pygame.display.set_icon(icon)

# lvl
lvl = 1
lvl_txtX = screenX - 100
lvl_txtY = 10
mov_speed = 5 * lvl

# Player initialization
playerImg = pygame.image.load('./include/graphics/roe.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./include/graphics/enemy.png'))
    enemyX.append(random.randint(0, screenX))
    enemyY.append(0)
    enemyX_change.append(mov_speed)
    enemyY_change.append(0)

# Bullet
bulletImg = pygame.image.load('./include/graphics/ball.png')
bulletX = 0
bulletY = playerY
bullet_change = 5 * mov_speed
bullet_vis = False

# Score
score_val = 0
font = pygame.font.Font('./include/fonts/LittleDaisy.ttf', 32)
textX = 10
textY = 10

# Game Over
font_over = pygame.font.Font('./include/fonts/LittleDaisy.ttf', 64)
is_game_over = False


def game_over_text():
    over_text = font_over.render('GAME OVER ', True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    score = font.render('Score: ' + str(score_val), True, (0, 0, 0))
    screen.blit(score, (x, y))


def show_lvl(x, y, lvl):
    lvl_txt = font.render('lvl: ' + str(lvl), True, (0, 0, 0))
    screen.blit(lvl_txt, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet(x):
    global bullet_vis
    bullet_vis = True
    screen.blit(bulletImg, (x + 16, bulletY + 10))


# collision
def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    if distance < 35:
        return True
    return False


def levelization(score_val, step):
    global lvl
    if score_val % step == 0:
        return int((score_val / step) + 1)
    else:
        return lvl


# game loop
running = True
while running:
    # background - white RGB
    # screen.fill((255, 255, 255))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                playerX_change = -mov_speed * 2
            if event.key == pygame.K_RIGHT:
                playerX_change = mov_speed * 2
            if event.key == pygame.K_UP:
                playerY_change = -mov_speed * 2
            if event.key == pygame.K_DOWN:
                playerY_change = mov_speed * 2
            if event.key == pygame.K_SPACE:
                if not bullet_vis:
                    bullet_sound = mixer.Sound('./include/sounds/laser.wav')
                    bullet_sound.play()
                    # get current x coordinate if bullet is visible
                    bulletX = playerX
                    bullet(bulletX)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= (screenX - 64):
        playerX = screenX - 64
    if playerY <= 0:
        playerY = 0
    elif playerY >= (screenY - 64):
        playerY = screenY - 64

    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if isCollision(enemyX[i], enemyY[i], playerX, playerY):
            is_game_over = True

        if is_game_over:
            for j in range(num_of_enemies):
                enemyY[j] = screenY * 10
            game_over_text()
            break

        else:
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = mov_speed
                enemyY[i] += mov_speed * 5
            elif enemyX[i] >= (screenX - 64):
                enemyX_change[i] = -mov_speed
                enemyY[i] += mov_speed * 5
            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY) and bullet_vis:
                collision_sound = mixer.Sound('./include/sounds/explosion.wav')
                collision_sound.play()
                enemyY[i] = -1
                bulletY = playerY
                bullet_vis = False
                score_val += 1
                lvl = levelization(score_val, 12)
                enemyX[i] = random.randint(0, screenX - 66)
            enemy(enemyX[i], enemyY[i], i)

            for j in range(num_of_enemies):
                if j != i:
                    if isCollision(enemyX[i], enemyY[i], enemyX[j], enemyY[j]):
                        enemyX[i] = random.randint(0, screenX - 66)
                        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_vis = False
    if bullet_vis:
        bullet(bulletX)
        bulletY -= mov_speed * 7.5

    player(playerX, playerY)
    show_score(textX, textY)
    show_lvl(lvl_txtX, lvl_txtY, lvl)
    pygame.display.update()
