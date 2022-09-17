from random import randint
import pygame as pg

# Game screen
W = 1200
H = 675

# Colors
WHITE = (255, 255, 255)
GHOSTWHITE = (248, 248, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PINK = (243, 58, 106)
GREEN = (0, 250, 154)
RED = (255, 127, 80)
DSGRAY = (47, 79, 79)
GRAY = (131, 126, 124)
HPGRAY = (64, 64, 64)
DARKGREEN = (48, 103, 84)
LIGHTGREEN = (34, 139, 34)
BACKGROUND = (244, 164, 96)
# Constants
SCALE_FACTOR = 1.2
SCALE_FACTOR_SM = 0.25
SCALE_FACTOR_BG = 1.25
MAX_POKEMON_HP = 100
MAX_POKEMONS_ON_MAP = 4
POKEMONS_COUNT = 10
POKEMONS_PER_FIGHT = 5
ATTACK_INTERVAL = 0.4

params = dict()

clases = ["fire", "electro", "water", "grass", "none", "You", "Enemy"]
params["fire"] = (90 * SCALE_FACTOR, 90 * SCALE_FACTOR)
params["electro"] = (80 * SCALE_FACTOR, 80 * SCALE_FACTOR)
params["water"] = (100 * SCALE_FACTOR, 100 * SCALE_FACTOR)
params["grass"] = (90 * SCALE_FACTOR, 90 * SCALE_FACTOR)
params["none"] = (80 * SCALE_FACTOR, 80 * SCALE_FACTOR)
params["You"] = (120 * SCALE_FACTOR, 150 * SCALE_FACTOR)
params["Enemy"] = (120 * SCALE_FACTOR, 150 * SCALE_FACTOR)

for i in clases:
    params[i + "sm"] = (params[i][0] * SCALE_FACTOR_SM, params[i][1] * SCALE_FACTOR_SM)
    params[i + "bg"] = (params[i][0] * SCALE_FACTOR_BG, params[i][1] * SCALE_FACTOR_BG)

# Debug Consts
IS_HITBOX_ON = 0
IS_GAME_STARTED = 0

# Game + Map + Pokemons Info


mapPokemons = pg.sprite.Group()
trainers = pg.sprite.Group()
bullets = pg.sprite.Group()

from classes import *

game = pg.display.set_mode((W, H))