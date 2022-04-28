import random

Step 3. Calculate the values of the SN individuals.
Step 4. Apply Eq. (6) to generate a new solution u i , and update the new solution using Eq. (7). If G ( u i )  G ( x i ) , then x i  u i and trail i =1; else, trail i  trail i  1 .
Step 5. Apply Eq. (3) to calculate for the probability values p i of the solutions x i .
Step 6. If rand< p i , produce a new solution u i using Eq. (6), and update the new solution by Eq. (7). If G ( u i )  G ( x i ) , then x i  u i and trail i =1; else, trail i  trail i  1 .
Step 7. If trail>Limit, produce a new solution to replace x i using Eq. (8).
Step 8. If the number of cycles is greater than the maximum number of cycles, stop the calculation and record the current optimal value, Otherwise, take the second step.

from mkp import *

def pop_init_abc(list_items, list_constraints, pop_size=100):
    population = []

    for k in range(pop_size):
        ks = Knapsack(list_constraints, list_items, "scaled")
        for i in range(len(list_items)):
            ks.ks[i] = random.randint(0, 1)
        population += [ks]
    return population

items, constraints, optimum = open_instance("instances/sac94/weing/weing1.dat")


SN = 50
LIMIT = 200
MAXCYCLE = 1500

def abc(item_list, constraints):
    pop = pop_init_abc(item_list, constraints)

    cycle = 0
    while cycle < MAXCYCLE:

        random.sample(pop, SN)



        cycle += 1