class Item:
    profit = 0
    weight = []

    def __str__(self):
        return "Profit: " + str(self.profit) + "Weight: " + str(self.weight)


def open_instance(path):
    """
    Open the MKP instances and create the needed variables (nbr instances, objects, knapsack)

    :param path: The path to the file
    :return: The number of instances in the file, the objects and the knapsack size
    """

    nbr_instances = 1
    items = []
    knapsack = []

    nbr_items = 0
    nbr_constraints = 0
    optimum_value = 0

    with open(path, "r") as file:

        # Remove the first object of the line because it's a blank
        firstLine = file.readline()[1:]
        firstLine = firstLine.split(" ")

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
                line = file.readline()[1:].split()[:-1]
                for item_iter in range(len(line)-1):
                    item = Item()
                    item.profit = line[item_iter]
                    items[instance] += [item]
                i += len(line)

            # Get weights
            for i in range(nbr_constraints):
                for j in range(nbr_items):
                    line = file.readline()[1:].split()[:-1]
                    for item_iter in range(len(line)-1):
                        item.weight += [line[item_iter]]
                    i += len(line)

            # Get knapsack sizes
            file.readline()
            firstLine = file.readline()[1:].split(" ")
            print(firstLine[:-1])


open_instance("instances/chubeas/OR5x100/OR5x100.dat")
