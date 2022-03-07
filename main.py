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
            line = file.readline()[1:].split()
            knapsack += [[]]
            for size in line:
                knapsack[instance] += [int(size)]

            # For next iteration
            firstLine = file.readline()[1:].split(" ")[:-1]

    return items, knapsack, optimum_value


class Knapsack:
    """
    Class Knapsack represents a multidimensional 0-1 knapsack as a binary list
    where a 0 represents the lack of an item, and 1 the presence of an item
    """

    items = None

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

    @staticmethod
    def set_items(list_items):
        """
        Set the class variable items

        :param list_items: The list of the different items of the problem
        :type list_items: list
        """
        Knapsack.items = list_items

    def set_knapsack(self, ks):
        self.ks = ks

    def fit(self):
        """
        Calculate the fitness of the knapsack

        :rtype: int
        :return: The fitness of the knapsack, or 0 if the constraints are not respected
        """
        if self.respect_constraints():
            # Sum of all profits of the items in the knapsack
            return sum([Knapsack.items[i].profit for i, val in enumerate(self.ks) if val == 1])
        else:
            return 0

    # Several ways of doing it
    def pseudo_utility(self):
        # TODO
        pass

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
