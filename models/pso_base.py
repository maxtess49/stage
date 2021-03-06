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

    swarm.sort(key=lambda x: x.fitness, reverse=True)
    bestKnown = copy.deepcopy(swarm[0])

    num_fitness = 0

    while num_fitness < max_fit:
        for particle in swarm:
            for dimension in range(len(particle.position)):
                rand_cog = random.random()
                rand_soc = random.random()
                particle.velocity[dimension] = weights[dimension] * particle.velocity[dimension] \
                                               + cog_coef * rand_cog * (particle.best[dimension] - particle.position[dimension]) \
                                               + soc_coef * rand_soc * (bestKnown.position[dimension] - particle.position[dimension])

            particle.position = [1 if random.random() < abs(tanh(particle.position[i] + particle.velocity[i])) else 0
                                 for i in range(len(particle.position))]

            particle.fitness = fitness(particle.position, item_list, constraints)

            if particle.fitness > fitness(particle.best, item_list, constraints):
                particle.best = copy.deepcopy(particle.position)
            if particle.fitness > fitness(bestKnown.position, item_list, constraints):
                bestKnown = copy.deepcopy(particle)
        num_fitness += len(swarm)
        #print(bestKnown.fitness)

    return bestKnown


#items, knapsack, optimum = open_instance("instances/gk/gk08.dat")

#p = pso(items[0], knapsack[0], swarm_const, [random.random() for _ in range(len(items[0]))], max_fit=1000)
#print(p.fitness)
