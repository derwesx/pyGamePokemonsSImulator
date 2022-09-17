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
        for i in range(len(self.box)):
            for other in range(len(self.box)):
                if self.box[i].type == "fire" and self.box[other].type == "fire":
                    if self.box[i].damage + self.box[i].armor * 2 <= self.box[other].damage + self.box[other].armor * 2:
                        self.box[i], self.box[other] = self.box[other], self.box[i]
                elif self.box[i].type == "fire":
                    if self.box[other].damage + 3 > self.box[i].damage:
                        self.box[i], self.box[other] = self.box[other], self.box[i]
                    else:
                        if self.box[i].damage + self.box[i].armor * 2 <= self.box[other].damage + self.box[other].armor * 2:
                            self.box[i], self.box[other] = self.box[other], self.box[i]
                elif self.box[other].type == "fire":
                    if self.box[i].damage + 3 <= self.box[other].damage:
                        if self.box[i].damage + self.box[i].armor * 2 <= self.box[other].damage + self.box[other].armor * 2:
                            self.box[i], self.box[other] = self.box[other], self.box[i]
                else:
                    if self.box[i].damage + self.box[i].armor * 2 <= self.box[other].damage + self.box[other].armor * 2:
                        self.box[i], self.box[other] = self.box[other], self.box[i]
        need = self.box[0:count]
        self.box = self.box[count:]
        # print(self.self.box)
        return need