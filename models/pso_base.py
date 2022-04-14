import copy
import random
from math import tanh

from gwo import repair
from mkp import *
from slms import pop_init_random
from gwo import pop_init_pseudo

# Can come & go in both direction for each dimension
minVel = -1
maxVel = 1


class Particle:
    def __init__(self, vector, minVelocity, maxVelocity, fitness):
        self.position = vector
        self.velocity = [random.uniform(minVel, maxVel) for _ in range(len(vector))]
        self.best = vector
        self.fitness = fitness


def fitness(position, items_list, constraints):
    for weight_i in range(len(constraints)):
        if constraints[weight_i] >= sum([items_list[i].weight[weight_i] for i, val in enumerate(position) if val == 1]):
            return sum([items_list[i].profit for i, val in enumerate(position) if val == 1])
        else:
            return 0

def pso(item_list, constraints, swarm, weights, cog_coef=2.0, soc_coef=2.0, max_fit=100000):
    """
    Main PSO algorithm

    :param item_list: Items of mkp
    :type item_list: list of Item
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

    swarm.sort(key=lambda x: x.fitness, reverse=True)
    bestKnown = swarm[0]

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
            num_fitness += len(swarm)

            if particle.fitness > fitness(particle.best, item_list, constraints):
                particle.best = copy.deepcopy(particle.position)
            if particle.fitness > fitness(bestKnown.position, item_list, constraints):
                bestKnown = copy.deepcopy(particle)

    swarm.sort(key=lambda x: x.fitness, reverse=True)
    return swarm[0]


items, knapsack, optimum = open_instance("instances/sac94/hp/hp1.dat")

# pop = pop_init_random(20, items[0], knapsack[0])
pop = pop_init_pseudo(20, items[0], knapsack[0])
for ind in pop:
    #ind.fit()
    ind.fitness = fitness(ind.ks, items[0], knapsack[0])
pop.sort(key=lambda x: x.fitness, reverse=True)

swarm_const = []
for ind in pop:
    swarm_const += [Particle(ind.ks, minVel, maxVel, ind.fitness)]

p = pso(items[0], knapsack[0], swarm_const, [random.random() for _ in range(len(items[0]))], max_fit=1000)

print(p.fitness)
