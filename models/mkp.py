import numpy as np
from scipy.optimize import linprog


class Item:
    """
    Class Item represents each item of the knapsack problem with its profit and weights for each dimension
    """

    def __init__(self):
        self.profit = 0
        self.weight = []

    def __str__(self):
        return "Profit: " + str(self.profit) + " Weight: " + str(self.weight)


def open_instance(path):
    """
    Open the MKP instances and create the needed variables (nbr instances, objects, knapsack)

    :param path: The path to the file
    :type path: string

    :rtype: (list, list, int)
    :return: Each item, the knapsack size and the optimum value of the problem (0 if unknown)
    """

    nbr_instances = 1
    items = []
    knapsack = []

    optimum_value = 0

    with open(path, "r") as file:

        # Remove the first object of the line if it's a blank
        firstLine = file.readline().split(" ")
        if firstLine[0] == "":
            firstLine = firstLine[1:]

        # Get nbr of instances if defined
        if firstLine[1] == "\n":
            nbr_instances = int(firstLine[0])
            firstLine = file.readline()[1:].split(" ")

        # Get all instances
        for instance in range(nbr_instances):
            items += [[]]
            nbr_items = int(firstLine[0])

            nbr_constraints = int(firstLine[1])
            optimum_value = int(firstLine[2])

            # Get profits
            i = 0
            while i < nbr_items:
                line = file.readline()[1:].split()
                for profit in line:
                    item = Item()
                    item.profit = int(profit)
                    items[instance] += [item]
                i += len(line)

            i = 0
            j = 0
            # Get weights
            while i < nbr_items * nbr_constraints:
                line = file.readline()[1:].split()
                for weight in line:
                    if j % nbr_items == 0:
                        j = 0
                    items[instance][j].weight += [int(weight)]
                    j += 1
                i += len(line)

            # Get knapsack sizes
            i = 0
            while i < nbr_constraints:
                line = file.readline()[1:].split()
                knapsack += [[]]
                for size in line:
                    knapsack[instance] += [int(size)]
                i += len(line)

            # For next iteration
            firstLine = file.readline()[1:].split(" ")[:-1]

    return items, knapsack, optimum_value


class Knapsack:
    """
    Class Knapsack represents a multidimensional 0-1 knapsack as a binary list
    where a 0 represents the lack of an item, and 1 the presence of an item

    items: list of Item \n
    pseudo_utilities: list of int (represents the descending order of the pseudo utility)

    """

    items = None
    pseudo_utilities = None

    def __init__(self, size, list_items):
        """
        :param size: List of constraints for the knapsack
        :type size: list of int
        :param list_items: The list of the different items of the problem
        :type list_items: list of Item
        """
        self.constraints = size
        self.ks = [0] * len(list_items)
        if Knapsack.items is None:
            Knapsack.items = list_items
        if Knapsack.pseudo_utilities is None:
            Knapsack.pseudo_utilities = Knapsack.pseudo_utility(self)
        self.fitness = 0

    @staticmethod
    def set_items(list_items):
        """
        Set the class variable items

        :param list_items: The list of the different items of the problem
        :type list_items: list
        """
        Knapsack.items = list_items

    def set_knapsack(self, ks):
        """
        Set the knapsack list

        :param ks: A binary list representing a knapsack
        :type ks: list of int
        """
        self.ks = ks

    def fit(self):
        """
        Calculate the fitness of the knapsack
        """
        if self.respect_constraints():
            # Sum of all profits of the items in the knapsack
            self.fitness = sum([Knapsack.items[i].profit for i, val in enumerate(self.ks) if val == 1])
        else:
            self.fitness = 0

    # Several ways of doing it
    def pseudo_utility(self):
        """
        Compute the pseudo utility of each item (linear relaxation of MKP)

        :rtype: list of float
        :return: The pseudo utility of each Item
        """

        # constraints + ones
        constraints = np.concatenate((self.constraints, np.ones(len(Knapsack.items))))
        # weights of items
        weight = np.array([item.weight for item in Knapsack.items])
        # inverse of weight + identity matrix
        i_weight = - np.concatenate((weight, np.eye(len(Knapsack.items))), axis=1)
        # Inverse of profits
        i_profit = - np.array([item.profit for item in Knapsack.items])

        # Compute the linear relaxation of MKP
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
        result = linprog(constraints, i_weight, i_profit, method="revised simplex")
        # print(result)

        if result.success:
            shadow_price = result.x[:len(self.constraints)]
            pseudo_utilities = (-i_profit).T / (np.matmul(shadow_price.T, weight.T))

            return (- pseudo_utilities).argsort()
        else:
            return None

    def respect_constraints(self):
        """
        Check the constraints on the knapsack

        :rtype: bool
        :return: A boolean True if the constraints are respected, False otherwise
        """
        for weight_i in range(len(self.constraints)):
            # Sum of all weight of the items in the knapsack for the dimension weight_i
            if self.constraints[weight_i] < \
                    sum([Knapsack.items[i].weight[weight_i] for i, val in enumerate(self.ks) if val == 1]):
                return False
        return True
