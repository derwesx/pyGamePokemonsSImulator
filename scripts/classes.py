from random import randint
from random import choice
from pygame.locals import *
from pygame import mixer
import pygame as pg
import fun
from consts import *


def check_out_of_field(x, y):
    if x > W - 350 or y > H - 80 or y < 0 or x < 300:
        return True
    return False


def get_random_map_place():
    return (randint(100, W - 100), randint(100, H - 100))


class Pokemon(pg.sprite.Sprite):
    def __init__(self, _nm, _dmg, _arm, _x=0, _y=0, _class="none"):
        self.maxHp = MAX_POKEMON_HP
        self.hp = self.maxHp
        self.name = _nm
        self.damage = _dmg
        self.armor = _arm
        self.type = _class
        self.chance = randint(1, 93)
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"../assets/images/{_class}" + ".png").convert_alpha()
        self.image = pg.transform.scale(self.image, (params[self.type]))
        self.rect = self.image.get_rect(center=(_x, _y))
        self.w, self.h = params[self.type]
        self.hitbox = (self.rect.x, self.rect.y, self.w, self.h)

    def get_attacked(self, attack):
        if attack < 1:
            attack = 1
        self.hp -= attack

    def move(self, lx=-5, rx=5, ly=-5, ry=5):
        if rx < lx:
            lx, rx = rx, lx
        if ry < ly:
            ly, ry = ry, ly
        self.rect.x += randint(lx, rx)
        self.rect.y += randint(ly, ry)

    def update(self):
        self.hitbox = (self.rect.x, self.rect.y, self.w, self.h)
        if check_out_of_field(self.rect.x, self.rect.y):
            self.rect.x, self.rect.y = get_random_map_place()

    def reduce_hp_test(self):
        self.hp -= randint(1, 5)
        if self.hp < -100:
            self.hp = self.maxHp

    def __lt__(self, other):
        if self.type == "fire" and other.type == "fire":
            return self.damage + self.armor * 2 > other.damage + other.armor * 2
        elif self.type == "fire":
            if other.damage + 3 > self.damage:
                return False
            else:
                return self.damage + self.armor * 2 > other.damage + other.armor * 2
        elif other.type == "fire":
            if self.damage + 3 > other.damage:
                return True
            else:
                return self.damage + self.armor * 2 > other.damage + other.armor * 2
        else:
            return self.damage + self.armor * 2 > other.damage + other.armor * 2


class GrassPokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm, _x=0, _y=0):
        super().__init__(_nm, _dmg, _arm, _x, _y, "grass")

    def get_bonuses(self, attackATM, armorATM, otherType):
        if otherType == "fire":
            armorATM -= 2
        strenght = max(1, attackATM - armorATM)
        return strenght

    def attack(self, other):
        if self.hp > 0:
            attack = self.get_bonuses(self.damage, other.armor, other.type)
            other.get_attacked(attack)


class FirePokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm, _x=0, _y=0):
        super().__init__(_nm, _dmg, _arm, _x, _y, "fire")

    def get_bonuses(self, attackATM, armorATM, otherType):
        if otherType == "grass":
            attackATM += randint(2, 5)
        strenght = max(1, attackATM - armorATM)
        return strenght

    def attack(self, other):
        if self.hp > 0:
            attack = self.get_bonuses(self.damage, other.armor, other.type)
            other.get_attacked(attack)


class ElectricPokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm, _x=0, _y=0):
        super().__init__(_nm, _dmg, _arm, _x, _y, "electro")

    def get_bonuses(self, attackATM, armorATM, otherType):
        if otherType == "water":
            armorATM = 0
        strenght = max(1, attackATM - armorATM)
        return strenght

    def attack(self, other):
        if self.hp > 0:
            attack = self.get_bonuses(self.damage, other.armor, other.type)
            other.get_attacked(attack)


class WaterPokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm, _x=0, _y=0):
        super().__init__(_nm, _dmg, _arm, _x, _y, "water")

    def get_bonuses(self, attackATM, armorATM, otherType):
        if otherType == "fire":
            attackATM *= 3
        if otherType == "grass":
            armorATM //= 2
        strenght = max(1, attackATM - armorATM)
        return strenght

    def attack(self, other):
        if self.hp > 0:
            attack = self.get_bonuses(self.damage, other.armor, other.type)
            other.get_attacked(attack)


class Trainer(pg.sprite.Sprite):
    def __init__(self, x, y, tp):
        self.name = tp
        self.cd = 0
        self.wins = 0
        self.box = []
        _class = tp
        self.type = _class
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"../assets/images/{_class}" + ".png").convert_alpha()
        self.image = pg.transform.scale(self.image, (params[self.type]))
        self.rect = self.image.get_rect(center=(x, y))
        self.w, self.h = params[self.type]
        self.hitbox = (self.rect.x, self.rect.y, self.w, self.h)

    def add(self, pokemon):
        self.box.append(pokemon)

    def best_team(self, count):
        if count > len(self.box):
            return -1
        return self.box[0:count]

    def update_cooldown(self):
        if self.cd < 100:
            self.cd += randint(1, 2)

    def update(self):
        self.update_cooldown()
        if self.cd >= 100:
            if len(mapPokemons.sprites()):
                self.cd = 0
                id = randint(0, len(mapPokemons.sprites()) - 1)
                for i in mapPokemons:
                    if not id:
                        self.catch(i)
                        break
                    else:
                        id -= 1
            else:
                pass

    def catch(self, pok):
        bullet = Bullet(self.rect.x, self.rect.y, pok.rect.x, pok.rect.y, randint(0, 100), pok.name, self.name,
                        pok.type)
        bullets.add(bullet)

class SmartTrainer(Trainer):

    def best_team(self, count):
        if count > len(self.box):
            return -1
        self.box.sort()
        return self.box[0:count]

    def update(self):
        self.box.sort()
        self.update_cooldown()
        if self.cd >= 100:
            if len(mapPokemons.sprites()):
                self.cd = 0
                pokemon, bestdamage, chance = 0, 0, 0
                pokemon2, bestdamage2 = 0, 0
                for i in mapPokemons:
                    if i.damage == bestdamage and i.chance > chance:
                        pokemon, chance, bestdamage = i, i.chance, i.damage
                    if i.type != "fire":
                        if bestdamage2 < i.damage:
                            bestdamage2 = i.damage
                            pokemon2 = i
                    if i.chance < 10 and pokemon != 0:
                        continue
                    if i.damage > bestdamage:
                        bestdamage = i.damage
                        pokemon = i
                    if i.chance > chance and i.damage == bestdamage:
                        chance = i.chance
                        bestdamage = i.damage
                        pokemon = i
                    if chance < 10 and i.chance > 10:
                        chance = i.chance
                        bestdamage = i.damage
                        pokemon = i
                if pokemon2 != 0:
                    if pokemon2.damage + 3 > pokemon.damage:
                        self.catch(pokemon2)
                    else:
                        self.catch(pokemon)
                else:
                    self.catch(pokemon)
            else:
                pass

mixer.init()

class Bullet(pg.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, ch, pokname, trainername, _class):
        bulletSound = pg.mixer.Sound(f'../assets/music/{_class}.mp3')
        bulletSound.play()
        self.speed = 30
        self.chance = ch
        self.killname = pokname
        self.catchname = trainername
        self.type = _class
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"../assets/images/{_class}" + ".png").convert_alpha()
        self.image = pg.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect(center=(x1 + 150, y1 + 50))
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def update(self):
        x1 = self.rect.x
        y1 = self.rect.y
        x2 = self.x2
        y2 = self.y2
        if x1 < x2:
            x1 += self.speed
            x1 = min(x1, x2)
        else:
            x1 -= self.speed
            x1 = max(x1, x2)
        if y1 < y2:
            y1 += self.speed
            y1 = min(y1, y2)
        else:
            y1 -= self.speed
            y1 = max(y1, y2)
        self.rect.x = x1
        self.rect.y = y1
        if x1 == x2 and y1 == y2:
            for i in mapPokemons:
                if i.name == self.killname and self.chance <= i.chance:
                    for trainer in trainers:
                        if trainer.name == self.catchname:
                            trainer.box.append(i)
                    i.kill()
                    break
                elif i.name == self.killname:
                    i.chance *= 1.2
                    i.chance = min(i.chance, 100)
            self.kill()


class Battle:
    def __init__(self, trainer1, trainer2):
        self.players = [trainer1, trainer2]
        self.teams = [trainer1.best_team(POKEMONS_PER_FIGHT), trainer2.best_team(POKEMONS_PER_FIGHT)]
        self.players[0].battlebox = self.teams[0]
        self.players[1].battlebox = self.teams[1]
        self.turn = 0

    def simulateTurn(self):
        firstPokemon = -1
        secondPokemon = -1
        for i in self.teams[0]:
            if i.hp > 0:
                firstPokemon = i
                break
        for i in self.teams[1]:
            if i.hp > 0:
                secondPokemon = i
                break
        if firstPokemon == -1:
            return 2
        elif secondPokemon == -1:
            return 1
        if not self.turn:
            self.kill_pokemon(firstPokemon, secondPokemon)
        else:
            self.kill_pokemon(secondPokemon, firstPokemon)
        self.turn = not self.turn
        return 0

    def kill_pokemon(self, first_pokemon, second_pokemon):
        bullet = Bullet(first_pokemon.rect.x - first_pokemon.w / 4, first_pokemon.rect.y + first_pokemon.h / 2,
                        second_pokemon.rect.x - first_pokemon.w / 4, second_pokemon.rect.y + second_pokemon.h / 2, -1,
                        first_pokemon.name, second_pokemon.name, first_pokemon.type)
        bullets.add(bullet)
        first_pokemon.attack(second_pokemon)
