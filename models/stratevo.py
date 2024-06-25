import copy
import random
from inspect import signature

from models import mkp
from models.mkp import np
#import mkp
#from mkp import np
import math

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


def repair(individual, rand=0.0):
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

    pseudo_shuffle = mkp.Knapsack.pseudo_utilities
    if rand > 0.0 and rand <= 1.0:
        sample = random.sample(range(len(pseudo_shuffle)), int(rand * len(pseudo_shuffle)))
        for i in range(len(sample)):
            r = random.randrange(len(pseudo_shuffle))
            to_move = pseudo_shuffle[i]
            pseudo_shuffle = np.delete(pseudo_shuffle, i)
            pseudo_shuffle = np.insert(pseudo_shuffle, r, to_move)
            # pseudo_shuffle.insert(r, pseudo_shuffle.pop(i))

    for i in reversed(pseudo_shuffle):
        # Test if all the constraints are respected
        if False in [res <= const for res, const in zip(resource_consumption, individual.constraints)]:
            if individual.ks[i] == 1:
                individual.ks[i] = 0
                resource_consumption = [res - weight for res, weight in
                                        zip(resource_consumption, mkp.Knapsack.items[i].weight)]
                individual.fitness -= mkp.Knapsack.items[i].profit
        else:
            break

    for i in pseudo_shuffle:
        if individual.ks[i] == 0:
            if not (False in [res + weight <= const for res, const, weight in
                              zip(resource_consumption, individual.constraints, mkp.Knapsack.items[i].weight)]):
                individual.ks[i] = 1
                resource_consumption = [res + weight for res, weight in
                                        zip(resource_consumption, mkp.Knapsack.items[i].weight)]
                individual.fitness += mkp.Knapsack.items[i].profit


def select_best(population, num):
    return sorted(population, key=lambda x: x.fitness)[len(population) - num:][::-1]


def select_random(population, num):
    return random.sample(population, num)


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
    trial = [1 if random.uniform(0, 1) < abs(transform_function(x)) else 0 for x in trial_list]

    ks = mkp.Knapsack(individual.constraints, individual.items)
    ks.ks = trial[:]

    ks.fit()

    return ks


def bestMoyPond(bests, iteration, max_iteration):
    total_fit = 0
    for individual in bests:
        total_fit += individual.fitness
    weights = [ind.fitness / total_fit for ind in bests]

    newObjective = []
    for x in range(len(bests[0].ks)):
        current_x = 0
        for n_individual in range(len(bests)):
            current_x += bests[n_individual].ks[x] * weights[n_individual]
        current_x += np.random.normal(0, math.exp(-100 * iteration / max_iteration))
        newObjective += [current_x]

    newObjective = [math.tanh(x) for x in newObjective]

    child = copy.deepcopy(bests[0])
    child.ks = newObjective
    child.fit()
    return child


def bitflip(individual):
    for i in range(len(individual.ks)):
        if random.random() < 1/len(individual.ks):
            if individual.ks[i] == 1:
                individual.ks[i] = 0
            else:
                individual.ks[i] = 1


def repair_bit(individual):
    repair(individual)
    bitflip(individual)


def bit_repair(individual):
    bitflip(individual)
    repair(individual)


def uniform(parents):
    child = [0]*len(parents[0].ks)
    cross = 1/len(parents)
    for i in range(len(child)):
        r = random.random()
        somme = cross
        n_parent = 0
        while r > somme:
            n_parent += 1
            somme += cross
        child[i] = parents[n_parent].ks[i]

    knap_child = copy.deepcopy(parents[0])
    knap_child.ks = child

    return knap_child


def stratevo(population, num_parents, num_parents_combine, num_children, mutation_method, combination_method, selection="plus", max_iter=100000):
    '''
    Evolution strategy algorithm (μ/ρ,λ)-ES / (μ/ρ+λ)-ES
    Keep in mind ρ≤μ for both, and μ<λ for comma selection

    :param population: The population to work with
    :param num_parents: Number of parents to select from the population (μ)
    :param num_parents_combine: Number of parents to combine (ρ)
    :param num_children: Number of children to produce (λ)
    :param mutation_method: mutation method
    :param combination_method: method for parents crossover
    :param selection: comma (children only) or plus (children + parents) selection
    :param max_iter: number of fitness evaluation (100k / num_children because we want 100k fitness evaluations and we evaluate only children)

    :return: The best individual
    '''

    if selection != "plus":
        if num_parents > num_children:
            print("μ>λ in a comma selection situation /!\\")
            exit()

    max_iterations = int(max_iter/num_children)
    for iteration in range(max_iterations):
        parents = select_best(population, num_parents)
        children = []
        for _ in range(num_children):
            curr_parents = select_random(parents, num_parents_combine)
            if len(signature(combination_method).parameters) > 1:
                child = combination_method(curr_parents, iteration, max_iterations)
            else:
                child = combination_method(curr_parents)
            mutation_method(child)
            child.fit()
            children += [child]
        if selection == "plus":
            population += children
        else:
            population = children

    return select_best(population, 1)[0]

def es_base(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 10, bitflip, uniform)

def es_repair(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 10, bit_repair, uniform)

def es_prey(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 10, bit_repair, bestMoyPond)

def es_repair_inv(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 10, repair_bit, uniform)

def es_prey_inv(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 10, repair_bit, bestMoyPond)

def es_15_off(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 15, bitflip, uniform)

def es_20_off(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 20, bitflip, uniform)

def es_25_off(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 25, bitflip, uniform)

def es_15_off_repair(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 15, bit_repair, uniform)

def es_20_off_repair(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 20, bit_repair, uniform)

def es_25_off_repair(items, constraints):
    population = pop_init_pseudo(50, items, constraints)
    return stratevo(population, 10, 2, 25, bit_repair, uniform)


# random.seed(10)
# items, knapsack, optimum = mkp.open_instance("../instances/sac94/weish/weish01.dat")
# population = pop_init_pseudo(50, items[0], knapsack[0])
# res = stratevo(population, 10, 2, 10, bitflip, uniform, max_iter=1000)#es_base(items, knapsack)
# #res = stratevo(population, 10, 2, 10, repair_bit, bestMoyPond)
# print(res.ks)
# print(res.fitness)
# print(optimum)
#
# random.seed(10)
# population = pop_init_pseudo(50, items[0], knapsack[0])
# res = stratevo(population, 10, 2, 10, repair_bit, bestMoyPond, max_iter=1000)#es_base(items, knapsack)
# print(res.ks)
# print(res.fitness)
# print(optimum)