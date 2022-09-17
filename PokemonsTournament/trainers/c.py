from random import randint

class Trainer():
    def __init__(self, tp):
        self.name = tp
        self.wins = 0
        self.box = []
        _class = tp
        self.type = _class

    def add(self, pokemon):
        self.box.append(pokemon)

class SmartTrainer(Trainer):
    def best_team(self, count):
        cnt = 0
        need = []
        while cnt < count:
            for i in range(len(self.box)):
                if randint(0, 10) < 3:
                    need.append(self.box[i])
                    del self.box[i]
                    cnt += 1
                    break
        return need