from mkp import *
import random
import math

items, knapsack, optimum = open_instance("../instances/gk/gk01.dat")


# Accumulated resources as list of dimensions ?
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
        accumulated_resources = [0]*len(list_constraints)
        ks = Knapsack(list_constraints, list_items)
        for j in Knapsack.pseudo_utilities:
            # In descending of the pseudo utility

            # Test if all accumulated resources + new object are inferior to the constraints of the ks
            if random.random() < 0.5 \
                    and False not in [x < y for x, y in
                                      zip([a+b for a, b in
                                           zip(accumulated_resources, list_items[j].weight)], ks.constraints)]:
                ks.ks[j] = 1
                # doesn't compute fitness as it is calculated via a method of ks
                # fitness = fit(ks)

                # Add all sizes of current item to the accumulated resources
                accumulated_resources = [x+y for x, y in zip(accumulated_resources, list_items[j].weight)]
        ks.fit()
        population += [ks]

    return population


def pop_init_zero(population_size, list_items, list_constraints):
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
        ks = Knapsack(list_constraints, list_items)
        ks.ks = [0]*len(list_items)
        population += [ks]
    return population


def select_wolves(population):
    """
    Select the 3 best wolves

    :param population: Population in which we search
    :type population: list of Knapsack

    :rtype: (Knapsack, Knapsack, Knapsack)
    :return: The 3 best wolves
    """
    return sorted(population, key=lambda x: x.fitness)[:3]


def generate_prey(alpha, beta, delta):
    """
    Generate the solution we search (the prey)

    :param alpha: The alpha wolf
    :type alpha: Knapsack
    :param beta: The beta wolf
    :type beta: Knapsack
    :param delta: The delta wolf
    :type delta: Knapsack

    :rtype: list of float
    :return: The "prey" as a list of float
    """
    total_fitness = alpha.fitness + beta.fitness + delta.fitness

    if total_fitness != 0:
        weightA = alpha.fitness/total_fitness
        weightB = beta.fitness/total_fitness
        weightD = delta.fitness/total_fitness
    else:
        weightA = 0
        weightB = 0
        weightD = 0

    return [alpha.ks[x]*weightA+beta.ks[x]*weightB+delta.ks[x]*weightD
            for x in range(len(alpha.ks))]


# Generate a trial solution
def generate_sol(prey, individual, transform_function=math.tanh):
    """
    Generate a trial solution from the prey

    :param prey: The researched solution
    :type prey: list of float
    :param individual: The current individual
    :type individual: Knapsack
    :param transform_function: Transform function real to integer
    :type transform_function: typing.Callable

    :rtype: Knapsack
    :return: A trial solution
    """
    r = random.uniform(-2, 2)
    trial_list = [x - r * abs(x - y) for x, y in zip(prey, individual.ks)]
    trial = [1 if random.uniform(0, 1) < transform_function(x) else 0 for x in trial_list]

    ks = Knapsack(individual.constraints, individual.items)
    ks.ks = trial[:]

    return ks


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
        resource_consumption += [sum([Knapsack.items[i].weight[weight_i] for i, val in
                                      enumerate(individual.ks) if val == 1])]

    for i in reversed(Knapsack.pseudo_utilities):
        # Test if all the constraints are respected
        if False in [res <= const for res, const in zip(resource_consumption, individual.constraints)]:
            if individual.ks[i] == 1:
                individual.ks[i] = 0
                for j in range(len(Knapsack.items[i].weight)):
                    resource_consumption[j] -= Knapsack.items[i].weight[j]

    for i in Knapsack.pseudo_utilities:
        if not (False in [res+weight <= const for res, const, weight in
                          zip(resource_consumption, individual.constraints, Knapsack.items[i].weight)]):
            if individual.ks[i] == 0:
                individual.ks[i] = 1
                for j in range(len(Knapsack.items[i].weight)):
                    resource_consumption[j] += Knapsack.items[i].weight[j]
    individual.fit()

def gwo(max_iteration, list_items, list_constraints, population_size):
    """
    Binary grey wolf optimization algorithm

    :param max_iteration: Max n° of iterations
    :type max_iteration: int
    :param list_items: List of items of the problem
    :type list_items: list of Item
    :param list_constraints: List of constraints of the problem
    :type list_constraints: list of int
    :param population_size: Size of the population of wolves
    :type population_size: int

    :rtype: Knapsack, Knapsack, Knapsack
    :return: The best solution found
    """
    pop = pop_init_pseudo(population_size, list_items, list_constraints)
    alpha, beta, delta = select_wolves(pop)

    for iteration in range(max_iteration):
        # Estimate location of prey
        prey = generate_prey(alpha, beta, delta)

        for individual in pop:
            # Can remove the for loop with list comprehension
            # for item in individual.ks:
            trial_solution = generate_sol(prey, individual)

            repair(trial_solution)

            # Intensification I suppose
            if trial_solution.fitness > individual.fitness:
                individual.ks = trial_solution.ks[:]
                individual.fit()

                if trial_solution.fitness > alpha.fitness:
                    alpha.ks = trial_solution.ks[:]
                    alpha.fit()

                elif trial_solution.fitness > beta.fitness:
                    beta.ks = trial_solution.ks[:]
                    beta.fit()

                elif trial_solution.fitness > delta.fitness:
                    delta.ks = trial_solution.ks[:]
                    delta.fit()

            # If the new solution doesn't improve, we update the individual anyway if it isn't a leader
            # Diversification I suppose
            elif individual != alpha and individual != beta and individual != delta:
                individual.ks = trial_solution.ks[:]
                individual.fit()

        if iteration % 1000 == 0:
            print(str(iteration) + " : " + str(alpha.fitness))

    return alpha


sol = gwo(10000, items[0], knapsack[0], 20)
print(sol.fitness)
print(optimum)
