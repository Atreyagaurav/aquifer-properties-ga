from model import EquationModel, ErrorType
import math
import random
random.seed(100)

class Organism:
    MUTATION_RATE = 0.1
    MAX_CROSSOVER = 0.4
    MAX_LOG_S = -3
    MIN_LOG_S = -9
    MAX_LOG_T = 3
    MIN_LOG_T = -3
    
    def __init__(self, model, storativity, transmissivity):
        self.model = model
        self.storativity = storativity
        self.transmissivity = transmissivity
        model.set_aquifer_properties(storativity, transmissivity)
        self.error = model.get_error()

    def get_children(self, other, num_child=10):
        children = [
            self.get_child(other) for i in range(num_child)
        ]
        return children

    def get_child(self, other):
        snew = math.exp(self._new_para(
            math.log(self.storativity),
            math.log(other.storativity),
            Organism.MIN_LOG_S, Organism.MAX_LOG_S))
        tnew = math.exp(self._new_para(
            math.log(self.transmissivity),
            math.log(other.transmissivity),
            Organism.MIN_LOG_S, Organism.MAX_LOG_S))
        return Organism(self.model, snew, tnew)

    def _new_para(self, para1, para2, min_para, max_para):
        crossover = Organism.MAX_CROSSOVER * random.random()
        mutation = random.random() > Organism.MUTATION_RATE
        if mutation:
            new_para = crossover * min_para + (1-crossover) * max_para
        else:
            new_para = crossover * para1 + (1-crossover) * para2
        return new_para

    def __str__(self):
        return f'Organism(S={self.storativity}, T={self.transmissivity})'
        

class Population:
    GENERATION = 0
    ELITE_RATIO = 0.1
    
    def __init__(self, size, data_file):
        self.size = size
        self.model = EquationModel(8.155, 582, data_file)
        self.organisms = sorted([
            Organism(self.model,
                     math.exp(random.random()*(Organism.MAX_LOG_S-Organism.MIN_LOG_S)),
                     math.exp(random.random()*(Organism.MAX_LOG_T-Organism.MIN_LOG_T)),
                     ) for i in range(size)],
                           key=lambda org: org.error)

    def next_generation(self):
        best = self.organisms[:int(Population.ELITE_RATIO * self.size)]
        next_gen = []
        for org in best:
            next_gen += [org.get_child(other) for other in best]
        self.organisms = sorted(next_gen,key=lambda org: org.error)

    def get_csv(self):
        print('rank,storativity,transmissivity,error')
        for i, org in enumerate(self.organisms):
            print(f'{i+1},{org.storativity},{org.transmissivity},{org.error}')
        

if __name__ == '__main__':
    p = Population(100, "./data.csv")
    for i in range(10):
        print(p.organisms[0].error)
        p.next_generation()

