from gwo import *
from mkp import *


# Parameters
POPULATION_SIZE = 20
MAX_GENERATIONS = 5000


def multipurpose(init_pop, select, mutate, insert, items, sizes):

    for iteration in range(MAX_GENERATIONS):
        pop = init_pop(POPULATION_SIZE, items, sizes)

        bests = select(pop)

        mutate(pop, bests)

        insert(pop, bests)


items, knapsack, optimum = open_instance("../instances/gk/gk01.dat")
multipurpose(pop_init_pseudo, select_wolves, repair, "TODO", items[0], knapsack[0])
