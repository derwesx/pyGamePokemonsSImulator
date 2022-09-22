import sys
import copy
import time
import pygame as pg
sys.setrecursionlimit(100000)

from classes import *
import pygame as pg
import random
NUMBER_OF_PLAYERS = 5
NUMBER_OF_TOURS = 10


import trainers.d
import trainers.f
import trainers.g
# import trainers.h
import trainers.i
import trainers.j

TRAINERS = []

TRAINERS.append(trainers.d.SmartTrainer(1))
TRAINERS.append(trainers.f.SmartTrainer(2))
TRAINERS.append(trainers.g.SmartTrainer(3))
# TRAINERS.append(trainers.h.SmartTrainer(4))
TRAINERS.append(trainers.i.SmartTrainer(5))
TRAINERS.append(trainers.j.SmartTrainer(6))


random.seed(144)

resultsTable = []
for i in range(NUMBER_OF_PLAYERS + 1):
    resultsTable.append([0, ] * (NUMBER_OF_PLAYERS + 1))

for i in range(NUMBER_OF_PLAYERS):
    resultsTable[0][i+1] = i + 1
    resultsTable[i+1][0] = i + 1

resultsLinear = [0, ] * NUMBER_OF_PLAYERS


W = 600
H = W

pg.init()
game = pg.display.set_mode((W, H))

WHITE = (255, 255, 255)
GHOSTWHITE = (248, 248, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PINK = (243, 58, 106)
GREEN = (0, 250, 154)
RED = (255, 127, 80)
DSGRAY = (20, 20, 20)
GRAY = (131, 126, 124)
HPGRAY = (64, 64, 64)
DARKGREEN = (48, 103, 84)
LIGHTGREEN = (34, 139, 34)
BACKGROUND = (244, 164, 96)

def draw_table():
    game.fill(BACKGROUND)
    X = W / (NUMBER_OF_PLAYERS + 1)
    for i in range(NUMBER_OF_PLAYERS + 1):
        for j in range(NUMBER_OF_PLAYERS + 1):
            pg.draw.rect(game, GHOSTWHITE, pg.Rect(i * X + 5, j * X + 5, X - 10, X - 10))
            font = pg.font.Font(None, int(X / 2))
            text = 0
            text_rect = 0
            if i == j and j == 0:
                text = font.render(f'{resultsTable[i][j]}', True, RED)
                text_rect = text.get_rect(center = (i * X + X / 2, j * X + X / 2)) 
            elif i == j:
                text = font.render(f'=', True, HPGRAY)
                text_rect = text.get_rect(center = (i * X + X / 2, j * X + X / 2)) 
            elif i == 0 or j == 0:
                text = font.render(f'{TRAINERS[i + j - 1].name}', True, DSGRAY)
                text_rect = text.get_rect(center = (i * X + X / 2, j * X + X / 2)) 
            else:
                text = font.render(f'{resultsTable[i][j]}', True, GRAY)
                text_rect = text.get_rect(center = (i * X + X / 2, j * X + X / 2)) 
            game.blit(text, text_rect)
    pg.display.update()
    pg.time.delay(20)

def draw_end_table():
    game.fill(BACKGROUND)
    X = W / (NUMBER_OF_PLAYERS + 1)
    for i in range(NUMBER_OF_PLAYERS + 1):
        for j in range(NUMBER_OF_PLAYERS + 1):
            pg.draw.rect(game, GHOSTWHITE, pg.Rect(i * X + 5, j * X + 5, X - 10, X - 10))
            font = pg.font.Font(None, int(X / 2))
            text = 0
            if j == NUMBER_OF_PLAYERS // 2:
                text = font.render(f'{resultsTable[i][j]}', True, PINK)
            else:
                text = font.render(f'{resultsTable[i][j]}', True, RED)
            text_rect = text.get_rect(center = (i * X + X / 2, j * X + X / 2)) 
            game.blit(text, text_rect)
    pg.display.update()
    pg.time.delay(20)

for tours in range(NUMBER_OF_TOURS):
    resultsTable[0][0] = tours + 1
    currentBox = []
    for i in range(25):
        currentBox.append(get_random_pokemon())
    for firstPlayerID in range(NUMBER_OF_PLAYERS):
        for secondPlayerID in range(NUMBER_OF_PLAYERS):
            print(firstPlayerID, secondPlayerID)
            if firstPlayerID == secondPlayerID:
                continue
            # print(firstPlayerID, secondPlayerID)

            firstTrainer = copy.deepcopy(TRAINERS[firstPlayerID])
            secondTrainer = copy.deepcopy(TRAINERS[secondPlayerID])
            firstTrainer.box = copy.deepcopy(currentBox)
            print("first trainer passed")
            secondTrainer.box = copy.deepcopy(currentBox)
            print("second trainer passed")
            idd = 0
            while len(firstTrainer.box) > 0:
                idd += 1
                currentBattle = Battle(firstTrainer, secondTrainer)
                print(f"battle started {idd}")
                currentBattleResult = currentBattle.simulateTurn()

                if currentBattleResult == 1:
                    resultsLinear[firstPlayerID] += 1
                    resultsTable[firstPlayerID+1][secondPlayerID+1] += 1
                else:
                    resultsLinear[secondPlayerID] += 1
                    resultsTable[secondPlayerID+1][firstPlayerID+1] += 1
            print(firstPlayerID, secondPlayerID)
    draw_table()
    lol = 1
    while lol:
        for i in pg.event.get():
            if i.type == pg.KEYDOWN:
                if i.key == pg.K_SPACE:
                    lol = 0

for i in range(NUMBER_OF_PLAYERS+1):
    for j in range(NUMBER_OF_PLAYERS+1):
        resultsTable[i][j] = ""


ok = [0, ] * NUMBER_OF_PLAYERS
for i in range(NUMBER_OF_PLAYERS):
    mx = -1
    id = 0
    for j in range(NUMBER_OF_PLAYERS):
        print(mx, resultsLinear[j])
        if resultsLinear[j] >= mx:
            mx = resultsLinear[j]
            id = j
    ok[id] = 1
    resultsLinear[id] = -10
    print(resultsLinear)
    print(ok)
    resultsTable[i][NUMBER_OF_PLAYERS // 2] = TRAINERS[id].name
    resultsTable[i][NUMBER_OF_PLAYERS // 2 + 1] = mx
draw_end_table()
lol = 1
while lol:
    for i in pg.event.get():
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_SPACE:
                lol = 0

pg.quit()
