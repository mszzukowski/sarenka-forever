# this game was inspired by https://www.youtube.com/watch?v=FfWpgLFMI7w
# Icons made by https://www.flaticon.com/authors/photo3idea-studio - > photo3idea_studio at > www.flaticon.com
# Background image: https://pl.freepik.com/darmowe-zdjecie-wektory/kochanie > pl.freepik.com
# Background music from Free Music Archive https://freemusicarchive.org/

# TODO: (2) new sounds and images
# TODO: (4) refactor code (new file, OOP maybe?)
# TODO: (5) move speed from timer not only loop


import pygame
import random
import math
import json
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

# Enemy initialization
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

# High score list
high_score_list = []

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
font_over = pygame.font.Font('./include/fonts/Canterbury.ttf', 32)
is_game_over = False


def game_over_text(hs_list):
    # what to say after game is over
    to_show = ['GAME OVER', 'High scores:']
    for players in hs_list:
        element = str(players['name']) + ": " + str(players['score'])
        to_show.append(element)

    to_show.append('Press [R] to restart game or [Q] to quit')
    for e in range(len(to_show)):
        over_text = font_over.render(to_show[e], True, (0, 0, 0))
        screen.blit(over_text, (10, 50 + 50 * e))


def show_score(x, y):
    # shows player score
    score = font.render('Score: ' + str(score_val), True, (0, 0, 0))
    screen.blit(score, (x, y))


def show_lvl(x, y, level):
    # shows player lvl
    lvl_txt = font.render('lvl: ' + str(level), True, (0, 0, 0))
    screen.blit(lvl_txt, (x, y))


def player(x, y):
    # shows player
    screen.blit(playerImg, (x, y))


def enemy(x, y, num):
    # shows enemies
    screen.blit(enemyImg[num], (x, y))


def bullet(x):
    # function to define player ammunition
    # todo: don't use global variables!
    global bullet_vis
    bullet_vis = True
    screen.blit(bulletImg, (x + 16, bulletY + 10))


def is_collision(x1, y1, x2, y2):
    # collision detection
    distance = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    if distance < 35:
        return True
    return False


def levelization(score_value, step):
    # added to change lvl number
    global lvl
    if score_value % step == 0:
        return int((score_value / step) + 1)
    else:
        return lvl


def restart_game():
    # function to restart the game. Works pretty well.
    # TODO: don't use global variables!
    global score_val, lvl, playerX, playerY, num_of_enemies, is_game_over, screenY, enemyY
    score_val = 0
    lvl = 1
    playerX = 370
    playerY = 480
    player(playerX, playerY)
    show_score(textX, textY)
    show_lvl(lvl_txtX, lvl_txtY, lvl)
    is_game_over = False
    for num in range(num_of_enemies):
        enemyY[num] = 0


def high_score(score, name='Player'):
    # getting hs table from file and save to it
    champion = False
    with open('configs/hs.json') as hs_file:
        hs = json.load(hs_file)
        for l in hs['high_scores']:
            if score_val > int(l['score']):
                champion = True
        if champion:
            adder = {'name': name, 'score': score}
            hs['high_scores'].append(adder)
            hs['high_scores'] = sorted(hs['high_scores'], key=lambda k: int(k['score']), reverse=True)

    if len(hs['high_scores']) > 7:
        hs['high_scores'] = hs['high_scores'][:7]
    if champion:
        with open('configs/hs.json', 'w') as saver:
            json.dump(hs, saver)
    return hs['high_scores']


# game loop
running = True
while running:
    screen.blit(background, (0, 0))

    # events handler - keyboard inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
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
            if event.key == pygame.K_r:
                restart_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    # player move
    playerX += playerX_change
    playerY += playerY_change

    # Player can't go out of screen
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
        # Game Over checker
        if is_collision(enemyX[i], enemyY[i], playerX, playerY):
            is_game_over = True
            high_score_list = high_score(score_val, 'Player')

        # enemies out of screen
        if is_game_over:
            for j in range(num_of_enemies):
                enemyY[j] = screenY * 10
            game_over_text(high_score_list)
            break

        else:
            enemyX[i] += enemyX_change[i]

            # enemies turn move if their touch wall
            if enemyX[i] <= 0:
                enemyX_change[i] = mov_speed
                enemyY[i] += mov_speed * 5
            elif enemyX[i] >= (screenX - 64):
                enemyX_change[i] = -mov_speed
                enemyY[i] += mov_speed * 5

            # when enemy was shot
            if is_collision(enemyX[i], enemyY[i], bulletX, bulletY) and bullet_vis:
                collision_sound = mixer.Sound('./include/sounds/explosion.wav')
                collision_sound.play()
                enemyY[i] = -1
                bulletY = playerY
                bullet_vis = False
                score_val += 1
                lvl = levelization(score_val, 12)
                enemyX[i] = random.randint(0, screenX - 66)

            # enemies can't go out of screen
            if enemyY[i] < 0:
                enemyY[i] = 0
            elif screenY * 5 > enemyY[i] > screenY + 64:
                enemyY[i] = 0

            enemy(enemyX[i], enemyY[i], i)

            # enemies can't be in the same place
            for j in range(num_of_enemies):
                if j != i:
                    if is_collision(enemyX[i], enemyY[i], enemyX[j], enemyY[j]):
                        enemyX[i] = random.randint(0, screenX - 66)
                        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_vis = False
    if bullet_vis:
        bullet(bulletX)
        bulletY -= mov_speed * 7.5

    # show everything
    player(playerX, playerY)
    show_score(textX, textY)
    show_lvl(lvl_txtX, lvl_txtY, lvl)
    pygame.display.update()
