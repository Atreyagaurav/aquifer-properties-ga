from model import EquationModel, ErrorType
import numpy as np
import math
import random

import config


class Organism:
    def __init__(self, model, storativity, transmissivity):
        self.model = model
        self.storativity = storativity
        self.transmissivity = transmissivity
        model.set_aquifer_properties(storativity, transmissivity)
        self.estimated_drawdown = model.estimated_drawdown.to_numpy()
        self.error = model.get_error()

    def get_children(self, other, num_child=10):
        children = [
            self.get_child(other) for i in range(num_child)
        ]
        return children

    def get_child(self, other):
        snew = self._new_para(self.storativity,
                              other.storativity,
                              config.PARA_MIN_S,
                              config.PARA_MAX_S)
        tnew = self._new_para(
            self.transmissivity,
            other.transmissivity,
            config.PARA_MIN_T,
            config.PARA_MAX_T)
        return Organism(self.model, snew, tnew)

    def _new_para(self, para1, para2, min_para, max_para):
        crossover = config.GA_MAX_CROSSOVER * random.random()
        mutation = random.random() > config.GA_MUTATION_RATE
        new_para = crossover * para1 + (1-crossover) * para2
        if mutation:
            new_para *= (1 + 0.05 * (0.5 - random.random()))
        return new_para

    def __str__(self):
        return f'Organism(S={self.storativity}, T={self.transmissivity})'
        

class Population:
    def __init__(self,
                 size=config.GA_POPULATION_SIZE,
                 *model_args, **model_kwargs):
        self.generation = 1
        self.size = size
        self.model = EquationModel(*model_args, **model_kwargs)
        self.organisms = sorted([
            Organism(self.model,
                     math.pow(10,random.random()*(-12)-2),
                     math.pow(10,random.random()*(6)-3),
                     ) for i in range(size)],
                           key=lambda org: org.error)

    def next_generation(self):
        best = self.organisms[:config.GA_ELITE_CHOICE]
        # errors = np.array([o.error for o in self.organisms])
        # weights = 1/errors
        # weights /= sum(weights)
        next_gen = []
        for i in range(self.size):
            orgs = np.random.choice(best, size=2)
            next_gen.append(orgs[0].get_child(orgs[1]))
        self.organisms = sorted(next_gen,key=lambda org: org.error)
        self.generation += 1

    def get_organism_csv(self):
        print('rank,storativity,transmissivity,error')
        for i, org in enumerate(self.organisms):
            print(f'{i+1},{org.storativity},{org.transmissivity},{org.error}')
        

if __name__ == '__main__':
    p = Population(100)
    best_model = p.organisms[0]
    print("Press Ctrl+C to end.")
    print("*" * 100)
    i = 1
    while True:
        if p.organisms[0].error < best_model.error:
            best_model = p.organisms[0]
        if i % 5 == 0:
            print(f'Generation-{i} :: error= {best_model.error} current best = {best_model}')
        p.next_generation()
        i += 1

