from random import randint
from pygame.locals import *
from pygame import mixer
from fun import *
from consts import *
from classes import *
import pygame as pg
import time
import sys
import os

mixer.init()
mixer.music.load('../assets/music/main.mp3')

def get_color_map(x):
    R, G, B = 1, 1, 0
    if x > 50:
        R = 1 - 2 * (x - 50) / 100
    if x <= 50:
        G = 2 * x / 100
    return int(R * 255), int(G * 255), int(B * 255)


def draw_pokemon(pokemon):
    LOSTCOLOR = RED
    if pokemon.hp <= 0:
        LOSTCOLOR = HPGRAY
    pg.draw.rect(game, LOSTCOLOR, (pokemon.hitbox[0], pokemon.hitbox[1] - 14.5, pokemon.w, 14))
    pg.draw.rect(game, GREEN, (
        pokemon.hitbox[0], pokemon.hitbox[1] - 14.5,
        pokemon.w - pokemon.w / pokemon.maxHp * (pokemon.maxHp - pokemon.hp),
        14))
    hpText = pg.font.Font(None, 20)
    hpBarText = hpText.render(f'{pokemon.hp}/{pokemon.maxHp}', True, GHOSTWHITE)
    chanceText = pg.font.Font(None, 20)
    chanceBarText = chanceText.render(f'{int(pokemon.chance)}%', True, get_color_map(int(pokemon.chance)))
    infoText = pg.font.Font(None, 20)
    infoBarText = infoText.render(f'{pokemon.damage} | {pokemon.armor}', True, DSGRAY)
    game.blit(hpBarText, (pokemon.rect.x + 5, pokemon.rect.y - 14))
    game.blit(chanceBarText, (pokemon.rect.x + 5, pokemon.rect.y - 32))
    game.blit(infoBarText, (pokemon.rect.x + 35, pokemon.rect.y - 32))
    if IS_HITBOX_ON:
        pg.draw.rect(game, RED, (pokemon.hitbox[0], pokemon.hitbox[1], pokemon.hitbox[2], pokemon.hitbox[3]))
    game.blit(pokemon.image, pokemon.rect)


def draw_cooldown(trainer):
    pg.draw.rect(game, WHITE, (trainer.hitbox[0], trainer.hitbox[1] + trainer.h + 5, trainer.w, 7))
    pg.draw.rect(game, LIGHTGREEN, (
        trainer.hitbox[0], trainer.hitbox[1] + trainer.h + 5, trainer.w - trainer.w / 100 * (100 - trainer.cd), 7))


def draw_trainer_common(trainer):
    text = pg.font.Font(None, 20)
    hpBarText = text.render(f'   {trainer.name} | Wins: {trainer.wins}', True, GHOSTWHITE)
    game.blit(hpBarText, (trainer.rect.x + 5, trainer.rect.y - 14))
    if IS_HITBOX_ON:
        pg.draw.rect(game, RED, (trainer.hitbox[0], trainer.hitbox[1], trainer.hitbox[2], trainer.hitbox[3]))
    game.blit(trainer.image, trainer.rect)


def draw_trainer(trainer):
    draw_cooldown(trainer)
    draw_trainer_common(trainer)


def draw_trainer_smart(trainer):
    draw_trainer_common(trainer)


def draw_inventory(trainer):
    counter = 0
    for i in trainer.box:
        i.image = pg.transform.scale(i.image, (params[i.type + "sm"]))
        i.rect = i.image.get_rect(center=(trainer.rect.x - 30, trainer.rect.y + counter * 35))
        counter += 1
        i.w, i.h = params[i.type + "sm"]
        i.hitbox = (i.rect.x, i.rect.y, i.w, i.h)

        LOSTCOLOR = RED
        if i.hp <= 0:
            LOSTCOLOR = HPGRAY
        infoText = pg.font.Font(None, 12)
        infoBarText = infoText.render(f'{i.damage} | {i.armor}', True, DSGRAY)
        pg.draw.rect(game, LOSTCOLOR, (i.hitbox[0], i.hitbox[1] - 7.5, i.w, 7))
        pg.draw.rect(game, GREEN, (i.hitbox[0], i.hitbox[1] - 7.5, i.w - i.w / i.maxHp * (i.maxHp - i.hp), 7))
        game.blit(i.image, i.rect)
        if i.hp > 0:
            game.blit(infoBarText, (i.rect.x + 30, i.rect.y - 8.5))    

def predraw_inventory_smart(trainer):
    for i in trainer.battlebox:
        i.image = pg.image.load(f"../assets/images/{i.type}" + ".png").convert_alpha()
        i.image = pg.transform.scale(i.image, (params[i.type + "bg"]))


def draw_inventory_smart(trainer):
    counter = 0
    for i in trainer.battlebox:
        i.rect = i.image.get_rect(topleft=(trainer.rect.x + 210 + counter * 180, trainer.rect.y + 80))
        counter += 1
        i.w, i.h = params[i.type + "bg"]
        i.hitbox = (i.rect.x, i.rect.y, i.w, i.h)

        LOSTCOLOR = RED
        if i.hp <= 0:
            LOSTCOLOR = HPGRAY
        pg.draw.rect(game, LOSTCOLOR, (i.hitbox[0], i.hitbox[1] - 15.5, i.w, 15))
        pg.draw.rect(game, GREEN, (i.hitbox[0], i.hitbox[1] - 15.5, i.w - i.w / i.maxHp * (i.maxHp - i.hp), 15))
        infoText = pg.font.Font(None, 25)
        infoBarText = infoText.render(f'{i.damage} | {i.armor}', True, DSGRAY)
        if i.hp > 0:
            game.blit(infoBarText, (i.rect.x + 30, i.rect.y - 15.5))
        game.blit(i.image, i.rect)


pg.font.init()

firstTrainer = Trainer(1050, 150, "Enemy")
secondTrainer = SmartTrainer(150, 150, "You")

trainers.add(firstTrainer)
trainers.add(secondTrainer)

IS_GAME_STARTED = 0


def event_ecalc():
    global IS_HITBOX_ON, IS_GAME_STARTED
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        if i.type == pg.KEYDOWN:
            if i.key == pg.K_h:
                IS_HITBOX_ON = not IS_HITBOX_ON
            if i.key == pg.K_r:
                for p in mapPokemons:
                    p.kill()
            if i.key == pg.K_d:
                for p in mapPokemons:
                    p.hp -= 100
                for p in firstTrainer.box:
                    p.hp -= 100
                for p in secondTrainer.box:
                    p.hp -= 100
            if i.key == pg.K_SPACE:
                IS_GAME_STARTED = 1
            if i.key == pg.K_q:
                os.system("python3 controller.py")
                exit(0)
            if i.key == pg.K_g:
                if len(secondTrainer.box) > 0:
                    firstTrainer.box.append(secondTrainer.box[0])
                    secondTrainer.box = secondTrainer.box[1:]
            if i.key == pg.K_s:
                firstTrainer.box.sort()

totalPokemons = 0
total_wins = 0

def GAME_SIMULATE():
    mixer.music.play()
    pg.mixer.music.set_volume(0.2)
    global IS_GAME_STARTED, POKEMONS_COUNT, MAX_POKEMONS_ON_MAP, totalPokemons, total_wins
    firstTrainer.rect = firstTrainer.image.get_rect(center=(1050, 150))
    secondTrainer.rect = secondTrainer.image.get_rect(center=(150, 150))
    while True:
        while len(mapPokemons.sprites()) < MAX_POKEMONS_ON_MAP and totalPokemons < POKEMONS_COUNT:
            totalPokemons += 1
            mapPokemons.add(fun.get_random_pokemon())
        if len(mapPokemons.sprites()) == 0:
            break
        event_ecalc()
        if not IS_GAME_STARTED:
            game.fill(WHITE)
            text = pg.font.Font(None, 120)
            startText = text.render('Press SPACE to start', True, GREEN)
            game.blit(startText, (W / 2 - 450, H / 2 - 50))
            pg.display.update()
            pg.time.delay(20)
            continue
        game.fill(BACKGROUND)
        for i in mapPokemons:
            draw_pokemon(i)
            i.update()
        for i in trainers:
            draw_trainer(i)
            draw_inventory(i)
            i.update()

        for i in bullets:
            i.update()
            game.blit(i.image, i.rect)
        pg.display.update()
        pg.time.delay(10)

    game.fill(BACKGROUND)
    battle = Battle(firstTrainer, secondTrainer)
    if battle.players[0].battlebox == -1 or battle.players[1].battlebox == -1:
        return
    CTT = time.perf_counter()
    predraw_inventory_smart(battle.players[0])
    predraw_inventory_smart(battle.players[1])
    
    battle.players[0].rect = battle.players[0].image.get_rect(center=(150, 150))
    battle.players[1].rect = battle.players[1].image.get_rect(center=(150, 450))
    while True:
        event_ecalc()
        game.fill(BACKGROUND)
        if time.perf_counter() - CTT > ATTACK_INTERVAL:
            CTT = time.perf_counter()
            got = battle.simulateTurn()
            if got == 1:
                game.fill(BACKGROUND)
                text = pg.font.Font(None, 120)
                battle.players[0].wins += 1
                startText = text.render('First Player Won', True, GREEN)
                game.blit(startText, (W / 2 - 450, H / 2 - 50))
                secondTrainer.box = secondTrainer.box[POKEMONS_PER_FIGHT:]
                for i in battle.players[0].box:
                    i.hp = 100
                pg.display.update()
                pg.time.delay(2000)
                total_wins += 1
                return
            elif got == 2:
                game.fill(BACKGROUND)
                text = pg.font.Font(None, 120)
                battle.players[1].wins += 1
                startText = text.render('Second Player Won', True, GREEN)
                game.blit(startText, (W / 2 - 450, H / 2 - 50))
                firstTrainer.box = firstTrainer.box[POKEMONS_PER_FIGHT:]
                for i in battle.players[1].box:
                    i.hp = 100
                pg.display.update()
                pg.time.delay(2000)
                total_wins += 1
                return

        for i in battle.players:
            draw_trainer_smart(i)
            draw_inventory_smart(i) 

        for i in bullets:
            i.update()
            game.blit(i.image, i.rect)

        pg.display.update()
        pg.time.delay(10)

while True:
    totalPokemons = 0
    GAME_SIMULATE()