from random import randint
from consts import *
from classes import *
import pygame as pg


def get_random_pokemon():
    tp = randint(1, 4)
    # Name, Damage, Armor, X, Y
    if tp == 1:
        damage = randint(8, 12)
        armor = randint(0, 5)
        return WaterPokemon(randint(0, 1000), damage, armor, randint(100, W - 100),
                            randint(100, H - 100))
    if tp == 2:
        damage = randint(8, 14)
        armor = randint(3, 5)
        return FirePokemon(randint(0, 1000), damage, armor, randint(100, W - 100),
                           randint(100, H - 100))
    if tp == 3:
        damage = randint(10, 15)
        armor = randint(0, 3)
        return ElectricPokemon(randint(0, 1000), damage, armor, randint(100, W - 100),
                               randint(100, H - 100))
    if tp == 4:
        damage = randint(8, 11)
        armor = randint(3, 6)
        return GrassPokemon(randint(0, 1000), damage, armor, randint(100, W - 100),
                            randint(100, H - 100))