class Item:

    def __init__(self):
        self.profit = 0
        self.weight = []


    def __str__(self):
        return "Profit: " + str(self.profit) + " Weight: " + str(self.weight)

def open_instance(path):
    """
    Open the MKP instances and create the needed variables (nbr instances, objects, knapsack)

    :param path: The path to the file
    :return: Each item, the knapsack size and the optimum value of the problem (0 if unknown)
    """

    nbr_instances = 1
    items = []
    knapsack = []

    nbr_items = 0
    nbr_constraints = 0
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
                    items[instance][j].weight += [weight]
                    j += 1
                i += len(line)

            # Get knapsack sizes
            line = file.readline()[1:].split()
            knapsack += [[]]
            for size in line:
                knapsack[instance] += [int(size)]

            # For next iteration
            firstLine = file.readline()[1:].split(" ")[:-1]

    return (items, knapsack, optimum_value)

#open_instance("instances/sac94/hp/hp1.dat")
#open_instance("instances/chubeas/OR5x100/OR5x100.dat")