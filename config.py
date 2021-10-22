import random
import math


# for reproducibility
RANDOM_SEED = 100
random.seed(RANDOM_SEED)

# for numerical  calculations  in model
THEIS_CALC_LIMIT = 1e-6
THEIS_MAX_ITERATIONS = 20

# parameters for model
PARA_MAX_LOG_S = -2
PARA_MIN_LOG_S = -14
PARA_MAX_LOG_T = 3
PARA_MIN_LOG_T = -3
PARA_MAX_S = math.pow(10,PARA_MAX_LOG_S)
PARA_MIN_S = math.pow(10,PARA_MIN_LOG_S)
PARA_MAX_T = math.pow(10,PARA_MAX_LOG_T)
PARA_MIN_T = math.pow(10,PARA_MIN_LOG_T)

# for genetic algorithm
GA_GENERATIONS = 100
GA_NUM_CHILD = 20
GA_ELITE_CHOICE = 10
GA_POPULATION_SIZE = GA_NUM_CHILD * GA_ELITE_CHOICE
GA_ELITE_RATIO = GA_ELITE_CHOICE / GA_POPULATION_SIZE
GA_MUTATION_RATE = 0.01
GA_MAX_CROSSOVER = 0.3

# data
DATA_FILE_PATH = "./data/observed-data.csv"
DATA_DISCHARGE = 8.155
DATA_RADIUS = 582