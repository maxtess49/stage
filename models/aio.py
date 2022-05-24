# All in one algorithm
# Trying to make an algorithm which is the general case of gwo & slms (&abc)
import random

from models import mkp
from models.mkp import np


def pop_init_pseudo(population_size, list_items, list_constraints):
    """
    Initialize a population of "elite" solutions

    :param population_size: Size of the population
    :type population_size: int
    :param list_items: List of items for the MKP
    :type list_items: list of Item
    :param list_constraints: List of constraints for this knapsack
    :type list_constraints: list of int

    :rtype: list of Knapsack
    :return: The population
    """
    population = []

    for k in range(population_size):
        accumulated_resources = [0] * len(list_constraints)
        ks = mkp.Knapsack(list_constraints, list_items)
        for j in mkp.Knapsack.pseudo_utilities:
            # In descending of the pseudo utility

            # Test if all accumulated resources + new object are inferior to the constraints of the ks
            if random.uniform(0, 1) < 0.5 \
                    and False not in [x < y for x, y in
                                      zip([a + b for a, b in
                                           zip(accumulated_resources, list_items[j].weight)], ks.constraints)]:
                ks.ks[j] = 1
                # doesn't compute fitness as it is calculated via a method of ks
                # fitness = fit(ks)

                # Add all sizes of current item to the accumulated resources
                accumulated_resources = [x + y for x, y in zip(accumulated_resources, list_items[j].weight)]
        ks.fit()
        population += [ks]

    return population

def repair(individual, rand=False):
    """
    Repair the solution given

    :param individual: A solution to repair
    :type individual: Knapsack

    :rtype: None
    :return: Does not return anything, modify the individual given
    """
    resource_consumption = []
    for weight_i in range(len(individual.constraints)):
        resource_consumption += [sum([mkp.Knapsack.items[i].weight[weight_i] for i, val in
                                      enumerate(individual.ks) if val == 1])]

    for i in reversed(mkp.Knapsack.pseudo_utilities):
        # Test if all the constraints are respected
        if False in [res <= const for res, const in zip(resource_consumption, individual.constraints)]:
            if individual.ks[i] == 1:
                individual.ks[i] = 0
                resource_consumption = [res - weight for res, weight in
                                        zip(resource_consumption, mkp.Knapsack.items[i].weight)]
                individual.fitness -= mkp.Knapsack.items[i].profit
        else:
            break

    for i in mkp.Knapsack.pseudo_utilities:
        if individual.ks[i] == 0:
            if not (False in [res + weight <= const for res, const, weight in
                              zip(resource_consumption, individual.constraints, mkp.Knapsack.items[i].weight)]):

                individual.ks[i] = 1
                resource_consumption = [res + weight for res, weight in
                                        zip(resource_consumption, mkp.Knapsack.items[i].weight)]
                individual.fitness += mkp.Knapsack.items[i].profit

def select_best(population, num):
    return sorted(population, key=lambda x: x.fitness)[:num]

def aio(list_items, list_constraints, max_iteration=5000, population_size=20, num=1):
    pop = pop_init_pseudo(population_size, list_items, list_constraints)

    for individual in pop:
        individual.fit()

    bests = select_best(pop, num)

    for iteration in range(max_iteration):
        if len(bests) > 1:
            total_fit = 0
            for individual in bests:
                total_fit += individual.fit
            weights = [ind.fit / total_fit for ind in bests]
            

            #[alpha.ks[x] * weightA + beta.ks[x] * weightB + delta.ks[x] * weightD + np.random.normal(0, math.exp(-100 * iteration / 1)) for x in range(len(alpha.ks))]




# particle.velocity[dimension] = bestKnown.position[dimension] + random.random() * (bestKnown.position[dimension] - particle.position[dimension])