import random
Step 4. Apply Eq. (6) to generate a new solution u i , and update the new solution using Eq. (7). If G ( u i )  G ( x i ) , then x i  u i and trail i =1; else, trail i  trail i  1 .
Step 5. Apply Eq. (3) to calculate for the probability values p i of the solutions x i .
Step 6. If rand< p i , produce a new solution u i using Eq. (6), and update the new solution by Eq. (7). If G ( u i )  G ( x i ) , then x i  u i and trail i =1; else, trail i  trail i  1 .
Step 7. If trail>Limit, produce a new solution to replace x i using Eq. (8).
Step 8. If the number of cycles is greater than the maximum number of cycles, stop the calculation and record the current optimal value, Otherwise, take the second step.

from mkp import *

def pop_init_abc(list_items, list_constraints, pop_size=100):
    population = []

    for k in range(pop_size):
        ks = Knapsack(list_constraints, list_items, None)
        for i in range(len(list_items)):
            ks.ks[i] = random.randint(0, 1)
        population += [ks]
    return population

def fitness(individual, items_list, constraints):
    for weight_i in range(len(constraints)):
        if constraints[weight_i] < sum([items_list[i].weight[weight_i] for i, val in enumerate(individual.ks) if val == 1]):
            return 0

    fit = sum([items_list[i].profit for i, val in enumerate(individual.ks) if val == 1])

    tot_weights = 0
    for dimension in range(len(constraints)):
        weights = sum([items_list[i].weight[dimension] for i, val in enumerate(individual.ks) if val == 1])
        tot_weights = weights - constraints[dimension]

    return -fit + ((10**-20) * max(0, tot_weights))

items, constraints, optimum = open_instance("instances/sac94/weing/weing1.dat")


SN = 50
LIMIT = 200
MAXCYCLE = 1500

def abc(item_list, constraints):
    pop = pop_init_abc(item_list, constraints)

    # for ind in pop:
    #     fit = fitness(ind, item_list, constraints)
    #
    #     if fit >= 0:
    #         fit = 1 / 1 + fit
    #     else:
    #         fit = 1 + abs(fit)
    #     ind.fitness  = fit

    cycle = 0
    while cycle < MAXCYCLE:

        sn_individuals = random.sample(pop, SN)

        for ind in sn_individuals:
            fit = fitness(ind, item_list, constraints)

            if fit >= 0:
                fit = 1 / 1 + fit
            else:
                fit = 1 + abs(fit)
            ind.fitness = fit

        sn_individuals.sort(key=lambda x: x.fitness, reverse=True)
        new_solution = [sn_individuals[0].ks[i] + random.uniform(-1, 1) * (sn_individuals[0].ks[i] - random.choice(sn_individuals[1:].ks[i]))
                        for i in range(len(sn_individuals.ks))]

        cycle += 1