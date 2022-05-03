import copy
import random
from math import tanh

from models.mkp import *
from models.gwo import pop_init_pseudo

# Can come & go in both direction for each dimension
minVel = -1
maxVel = 1


class Particle:
    def __init__(self, vector, minVelocity, maxVelocity, fitness_start):
        self.position = copy.deepcopy(vector)
        self.velocity = [random.uniform(minVelocity, maxVelocity) for _ in range(len(vector))]
        self.best = copy.deepcopy(vector)
        self.fitness = fitness_start


def fitness(position, items_list, constraints):
    for weight_i in range(len(constraints)):
        if constraints[weight_i] < sum([items_list[i].weight[weight_i] for i, val in enumerate(position) if val == 1]):
            return 0

    return sum([items_list[i].profit for i, val in enumerate(position) if val == 1])

def repair(individual, constraints):
    """
    Repair the solution given

    :param individual: A solution to repair
    :type individual: Knapsack

    :rtype: None
    :return: Does not return anything, modify the individual given
    """
    resource_consumption = []
    for weight_i in range(len(constraints)):
        resource_consumption += [sum([Knapsack.items[i].weight[weight_i] for i, val in
                                      enumerate(individual.position) if val == 1])]

    for i in reversed(Knapsack.pseudo_utilities):
        # Test if all the constraints are respected
        if False in [res <= const for res, const in zip(resource_consumption, constraints)]:
            if individual.position[i] == 1:
                individual.position[i] = 0
                resource_consumption = [res - weight for res, weight in
                                        zip(resource_consumption, Knapsack.items[i].weight)]
                individual.fitness -= Knapsack.items[i].profit
        else:
            break

    for i in Knapsack.pseudo_utilities:
        if individual.position[i] == 0:
            if not (False in [res + weight <= const for res, const, weight in
                              zip(resource_consumption, constraints, Knapsack.items[i].weight)]):

                individual.position[i] = 1
                resource_consumption = [res + weight for res, weight in
                                        zip(resource_consumption, Knapsack.items[i].weight)]
                individual.fitness += Knapsack.items[i].profit

def pso(item_list, constraints, cog_coef=2.0, soc_coef=2.0, max_fit=100000):
    """
    Main PSO algorithm

    :param item_list: Items of mkp
    :type item_list: list of Item
    :param constraints: List of constraints for mkp
    :type constraints: list of int
    :param swarm: Population
    :type swarm: list of Particle
    :param cog_coef: Cognition coefficient - Typical values are in [1,3]
    :type cog_coef: float
    :param soc_coef: Social coefficient - Typical values are in [1,3]
    :type soc_coef: float
    :param weights: Weights for velocity
    :type weights: list of float
    :param max_fit: Max numbers of fitness evaluations
    :type max_fit: int

    :rtype: Particle
    :return: The best particle
    """

    pop = pop_init_pseudo(20, item_list, constraints)
    for ind in pop:
        ind.fitness = fitness(ind.ks, item_list, constraints)
    pop.sort(key=lambda x: x.fitness, reverse=True)

    swarm = []
    for ind in pop:
        swarm += [Particle(ind.ks, minVel, maxVel, ind.fitness)]

    weights = [random.random() for _ in range(len(item_list))]
    i_weights = [1 - weights[i] for i in range(len(weights))]

    swarm.sort(key=lambda x: x.fitness, reverse=True)
    bestKnown = copy.deepcopy(swarm[0])

    num_fitness = 0

    while num_fitness < max_fit:
        for particle in swarm:
            for dimension in range(len(particle.position)):

                ## TO CHANGE ACCORDING TO BOTH ALGORITHM ###################################################
                rand_cog = random.random()
                rand_soc = random.random()
                # Based on metaphor-based algorithms
                particle.velocity[dimension] = particle.best[dimension] + random.random() * (particle.best[dimension] - particle.position[dimension])

                # Based on pso (Particle Swarm Optimization for the Multidimensional Knapsack Problem)
                # particle.velocity[dimension] = weights[dimension] * rand_cog * (particle.best[dimension]) + i_weights[dimension] * rand_soc * (bestKnown.position[dimension] - particle.position[dimension])

            particle.position = [1 if random.random() < abs(tanh(particle.position[i] + particle.velocity[i])) else 0
                                 for i in range(len(particle.position))]

            #repair(particle, constraints)

            ################################################################################################

            particle.fitness = fitness(particle.position, item_list, constraints)

            if particle.fitness > fitness(particle.best, item_list, constraints):
                particle.best = copy.deepcopy(particle.position)
            if particle.fitness > fitness(bestKnown.position, item_list, constraints):
                bestKnown = copy.deepcopy(particle)
        num_fitness += len(swarm)
        #print(bestKnown.fitness)

    return bestKnown


# items, knapsack, optimum = open_instance("instances/gk/gk08.dat")
#
# # pop = pop_init_random(20, items[0], knapsack[0])
# pop = pop_init_pseudo(20, items[0], knapsack[0])
# for ind in pop:
#     #ind.fit()
#     ind.fitness = fitness(ind.ks, items[0], knapsack[0])
# pop.sort(key=lambda x: x.fitness, reverse=True)
#
# swarm_const = []
# for ind in pop:
#     swarm_const += [Particle(ind.ks, minVel, maxVel, ind.fitness)]
#
# p = pso(items[0], knapsack[0], swarm_const, [random.random() for _ in range(len(items[0]))], max_fit=1000)
# print(p.fitness)