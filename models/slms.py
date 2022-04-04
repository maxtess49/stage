import math
# import mkp
import random
from models import mkp


def pop_init_random(population_size, list_items, list_constraints):
    """
    Initialize a population of "elite" solutions randomly

    :param population_size: Size of the population
    :type population_size: int
    :param list_items: List of items for the MKP
    :type list_items: list of Item
    :param list_constraints: List of constraints for this knapsack
    :type list_constraints: list of int

    :rtype: list of mkp.Knapsack
    :return: The population
    """
    population = []

    for k in range(population_size):
        ks = mkp.Knapsack(list_constraints, list_items, "scaled")
        for i in range(len(list_items)):
            ks.ks[i] = random.uniform(0, 1)
        population += [ks]
    return population


# Generate a trial solution
def generate_sol(individual, transform_function=math.tanh):
    """
    Generate a trial solution from the moths

    :param individual: The current individual
    :type individual: Knapsack
    :param transform_function: Transform function real to integer
    :type transform_function: typing.Callable

    :rtype: Knapsack
    :return: A trial solution
    """

    individual.ks = [1 if random.uniform(0, 1) < abs(transform_function(x)) else 0 for x in individual.ks]
    return individual


def repair(individual):
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


# Generation of solution
def calc_step(length, beta):
    """
    Calculate a step s for Lévy flight as seen in
    Nature-Inspired Metaheuristic Algorithms Second Edition - Xin-She Yang

    :param length: Number of items
    :type length: int
    :param beta: The index ?
    :type beta: float

    :rtype: list of int
    :return: The step s for each item
    """
    sigma = (math.gamma(1 + beta) * math.sin((math.pi * (beta - 1) / 2)) /
             math.gamma(beta / 2) * (beta - 1) * 2 ** ((beta - 2) / 2)) ** (1 / (beta - 1))

    u = [0] * length
    v = [0] * length
    for i in range(length):
        u[i] = random.uniform(0, 1) * sigma
        v[i] = random.uniform(0, 1)
    step = [u / abs(v) * (1 / (beta - 1)) for u, v in zip(u, v)]

    return step


def levyFlight(individuals, scaleFactor, beta=1.5):
    """
    Calculate the Lévy flight for each moth in population and mutate them

    :param individuals: A population
    :type individuals: list of mkp.Knapsack
    :param scaleFactor: The scale factor
    :type scaleFactor: float
    :param beta: The index
    :type beta: float

    :return: None
    """

    s = calc_step(len(mkp.Knapsack.items), beta)
    for i in range(len(individuals)):
        L = ((beta - 1) * math.gamma(beta - 1) * math.sin(math.pi * (beta - 1) / 2)) \
            / (math.pi * s[i] ** beta)
        individuals[i].ks = [item + scaleFactor * L for item in individuals[i].ks]


# Generation of solution
def sl(individuals, learningTime, scaleFactor, phi, best):
    """
    Self learning algorithm mutate each moth in population

    :param individuals: The population to move
    :type individuals: list of mkp.Knapsack
    :param learningTime: Nbr of iteration for computing
    :type learningTime: float
    :param scaleFactor: A scale factor ?
    :type scaleFactor: float
    :param phi: Acceleration factor
    :type phi: float
    :param best: Best known moth
    :type best: mkp.Knapsack

    :return: None
    """
    for i in range(len(individuals)):
        for j in range(learningTime):
            new = mkp.Knapsack(individuals[i].constraints, individuals[i].items)
            # Randomly chose a better individual
            if i == 0:
                random_better = random.choice(individuals[:i + 1])
            else:
                random_better = random.choice(individuals[:i])
            # Update the position of the moth according to the best individual and a better individual
            if random.uniform(0, 1) < 0.5:
                new.ks = [scaleFactor * (random_better.ks[item] + phi * (best.ks[item] - individuals[i].ks[item]))
                          for item in range(len(mkp.Knapsack.items))]
            else:
                new.ks = [scaleFactor * (random_better.ks[item] + (1 / phi) * (best.ks[item] - individuals[i].ks[item]))
                          for item in range(len(mkp.Knapsack.items))]
            new.fit()
            if new.fitness > individuals[i].fitness:
                individuals[i] = new
        individuals[i] = new


def slms(list_items, list_constraints, maxFit=100000, maxStep=1.0, phi=0.618):
    """
    Main moth search algorithm

    :param list_items: List of all the items for the problem
    :type list_items: list of mkp.Item
    :param list_constraints: List of all the constraints of the Knapsack
    :type list_constraints: list of int
    :param maxFit: max number of call to fitness function
    :type maxFit: int
    :param maxStep: Maximum step for Lévy flight
    :type maxStep: float
    :param phi: Acceleration factor
    :type phi: float
    :return:
    """

    population = pop_init_random(50, list_items, list_constraints)

    for individual in population:
        generate_sol(individual)
        repair(individual)
        individual.fit()
    population.sort(key=lambda x: x.fitness, reverse=True)
    bestInd = population[0]

    i = 0
    generation = 1
    while i < maxFit:
        # Have to change in case population length is odd
        pop_1 = population[:int(len(population) / 2)]
        pop_2 = population[int(len(population) / 2):]

        levyFlight(pop_1, (maxStep / generation ** 2))
        sl(pop_2, 1, random.uniform(0, 1), phi, bestInd)

        population = pop_1 + pop_2

        for individual in population:
            generate_sol(individual)
            repair(individual)
            individual.fit()
        population.sort(key=lambda x: x.fitness, reverse=True)

        i += len(population)
        generation += 1

        bestInd = population[0]

        if generation % 500 == 0:
            print("generation: " + str(generation) + " best fitness: " + str(population[0].fitness))

    return population[0]


# items, knapsack, optimum = mkp.open_instance("../instances/chubeas/OR5x100/OR5x100.dat")
# items, knapsack, optimum = mkp.open_instance("../instances/gk/gk01.dat")
# random.seed(10)
# sol = slms(items[0], knapsack[0], maxFit=100000)
# print(sol.fitness)
# print(optimum)
