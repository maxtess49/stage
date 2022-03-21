from gwo import *
from mkp import *


# Parameters
POPULATION_SIZE = 20
P_CROSSOVER = 0.0
P_MUTATION = 1.0
MAX_GENERATIONS = 5000


def multipurpose(init_pop, select, mutate, insert):
    pop = init_pop()

    bests = select()

    mutate(pop, bests)

    insert(pop, best)