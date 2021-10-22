import config
import utilities
import numpy as np
import pandas as pd
import itertools

from genetic_alg import Population


NUM_DIV = 5
num_child = np.linspace(5, 20, NUM_DIV, dtype=int)
elite_choice = np.linspace(5, 20, NUM_DIV, dtype=int)
mutation_rat = np.linspace(5, 20, NUM_DIV)/100
mutation_change = np.linspace(5, 40, NUM_DIV)/200
crossover = np.linspace(5, 20, NUM_DIV) / 40 

index = itertools.product(range(NUM_DIV), repeat=5)


df = pd.DataFrame([], columns=['sn','population','elite_rate', 'crossover', 'mutation', 'filename', 'error', 'generations'])
for c, ind in enumerate(index):
    config.GA_NUM_CHILD = num_child[ind[0]]
    config.GA_ELITE_CHOICE = num_child[ind[1]]
    config.GA_MUTATION_RATE = mutation_rat[ind[2]]
    config.GA_MUTATION_CHANGE = mutation_change[ind[3]]
    config.GA_MAX_CROSSOVER = crossover[ind[4]]
    config.GA_POPULATION_SIZE = config.GA_NUM_CHILD * config.GA_ELITE_CHOICE
    config.GA_ELITE_RATIO = config.GA_ELITE_CHOICE / config.GA_POPULATION_SIZE
    log_file = f'./data/models/{"_".join(map(str, ind))}.csv'
    
    df.loc[c,:] = [
        c,
        config.GA_NUM_CHILD,
        config.GA_ELITE_RATIO,
        config.GA_MAX_CROSSOVER,
        config.GA_MUTATION_RATE,
        log_file,
        0,
        0
    ]
    
    utilities.reset_seed()
    p = Population()
    best_model = p.organisms[0]
    ga_df = pd.DataFrame([], columns=['generation',
                                      'S_best',
                                      'T_best',
                                      'mae_best',
                                      'S',
                                      'T',
                                      'mae'])
    last_change = 0
    for i in range(config.GA_GENERATIONS):
        if p.organisms[0].error < best_model.error:
            best_model = p.organisms[0]
            last_change = i
        if i % 5 == 0:
            print(f'Generation-{i} :: error= {best_model.error} current best = {best_model}')
        ga_df.loc[i, :] = [i,
                           best_model.storativity,
                           best_model.transmissivity,
                           best_model.error,
                           p.organisms[0].storativity,
                           p.organisms[0].transmissivity,
                           p.organisms[0].error
                           ]
        ga_df.to_csv(log_file, index=False)
        p.next_generation()
    df.loc[c, 'error'] = best_model.error
    df.loc[c, 'generations'] = last_change
    df.to_csv("./data/models.csv", index=False)

