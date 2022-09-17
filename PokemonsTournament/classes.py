from random import randint

def get_random_pokemon():
    tp = randint(1, 4)
    damage = randint(1, 5)
    armor = randint(1, 5)    
    if tp == 1:
        return WaterPokemon(randint(0, 1000), damage, armor)
    if tp == 2:
        return FirePokemon(randint(0, 1000), damage, armor)
    if tp == 3:
        return ElectricPokemon(randint(0, 1000), damage, armor)
    if tp == 4:
        return GrassPokemon(randint(0, 1000), damage, armor)

class Pokemon:
    def __init__(self, _nm, _dmg, _arm, _class = "none"):
        self.hp = 100
        self.name = _nm
        self.damage = _dmg
        self.armor = _arm
        self.type = _class

    def get_hp(self):
        return max(0, self.hp)

    def get_atk(self):
        return max(0, self.damage)

    def get_def(self):
        return max(0, self.armor)

    def get_name(self):
        return self.name

    def get_attacked(self, attackATM, armorATM, otherType):
        if self.type == "fire" and otherType == "water":
            attackATM *= 3
        if self.type == "fire" and otherType == "grass":
            armorATM //= 2
        if self.type == "water" and otherType == "electro":
            armorATM = 0
        strenght = max(1, attackATM - armorATM)
        self.hp -= strenght
        self.hp = max(self.hp, 0)


class GrassPokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm):
        super().__init__(_nm, _dmg, _arm, "grass")

class FirePokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm):
        super().__init__(_nm, _dmg, _arm, "fire")

class ElectricPokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm):
        super().__init__(_nm, _dmg, _arm, "electro")

class WaterPokemon(Pokemon):
    def __init__(self, _nm, _dmg, _arm):
        super().__init__(_nm, _dmg, _arm, "water")

class Battle:
    def __init__(self, trainer1, trainer2):
        self.teams = [trainer1.best_team(5), trainer2.best_team(5)]
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
        if secondPokemon == -1:
            return 1
        if not self.turn:
            self.damage_pokemon(firstPokemon, secondPokemon)
        else:
            self.damage_pokemon(secondPokemon, firstPokemon)
        self.turn = not self.turn
        return self.simulateTurn()

    def damage_pokemon(self, first_pokemon, second_pokemon):
        second_pokemon.get_attacked(first_pokemon.damage, first_pokemon.armor, first_pokemon.type)
