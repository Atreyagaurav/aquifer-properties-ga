from model import EquationModel, ErrorType
import numpy as np
import math
import random
random.seed(100)

class Organism:
    MUTATION_RATE = 0.3
    MAX_CROSSOVER = 0.4
    MAX_LOG_S = 1e-3
    MIN_LOG_S = 1e-9
    MAX_LOG_T = 1e3
    MIN_LOG_T = 1e-3
    
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
        snew = self._new_para(self.storativity,
                              other.storativity,
                              Organism.MIN_LOG_S, Organism.MAX_LOG_S)
        tnew = self._new_para(
            self.transmissivity,
            other.transmissivity,
            Organism.MIN_LOG_S, Organism.MAX_LOG_S)
        return Organism(self.model, snew, tnew)

    def _new_para(self, para1, para2, min_para, max_para):
        crossover = Organism.MAX_CROSSOVER * random.random()
        mutation = random.random() > Organism.MUTATION_RATE
        new_para = crossover * para1 + (1-crossover) * para2
        if mutation:
            new_para *= (1 + 0.05 * (0.5 - random.random()))
        return new_para

    def __str__(self):
        return f'Organism(S={self.storativity}, T={self.transmissivity})'
        

class Population:
    GENERATION = 0
    ELITE_RATIO = 0.1
    
    def __init__(self, size, *model_args, **model_kwargs):
        self.size = size
        self.model = EquationModel(*model_args, **model_kwargs)
        self.organisms = sorted([
            Organism(self.model,
                     math.pow(10,random.random()*(-12)-2),
                     math.pow(10,random.random()*(6)-3),
                     ) for i in range(size)],
                           key=lambda org: org.error)

    def next_generation(self):
        best = self.organisms[:int(Population.ELITE_RATIO * self.size)]
        next_gen = []
        for org in best:
            next_gen += [org.get_child(other) for other in best]
        self.organisms = sorted(next_gen,key=lambda org: org.error)

    def get_organism_csv(self):
        print('rank,storativity,transmissivity,error')
        for i, org in enumerate(self.organisms):
            print(f'{i+1},{org.storativity},{org.transmissivity},{org.error}')
        

if __name__ == '__main__':
    p = Population(100, discharge=8.155, radius=582, data_file="./data.csv")
    for i in range(100):
        print(p.organisms[0].error)
        p.next_generation()

