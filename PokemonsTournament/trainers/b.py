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
        need = self.box[0:count]
        self.box = self.box[count:]
        return need