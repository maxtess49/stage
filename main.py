import csv
import random

import numpy as np

from models import gwo
from models import slms
from models import mkp
import os
# from models.frame import *


def main():
    # items, constraints, optimum = mkp.open_instance("./instances/chubeas/OR5x100/OR5x100.dat")

    result_file = "results.csv"
    create_res_file(result_file)

    list_algos = [gwo.gwo, slms.slms]

    path = "./instances/refaire"
    for root, directories, files in os.walk(path):
        for file in files:
            if not file.endswith(".dat"):
                break
            items, constraints, optimum = mkp.open_instance(os.path.join(root, file))

            for i in range(len(items)):
                for algo in list_algos:

                    max = 0
                    min = np.inf
                    mean = 0

                    with open('seeds.csv', 'r') as csvfile:
                        seeds = csv.reader(csvfile, delimiter=';')
                        n_seed = 1
                        for row in seeds:
                            for seed in row:
                                print(n_seed)
                                mkp.Knapsack.items = None
                                mkp.Knapsack.pseudo_utilities = None
                                random.seed(seed)
                                res = algo(items[i], constraints[i]).fitness

                                if res > max:
                                    max = res

                                if res < min:
                                    min = res

                                mean += res

                                n_seed += 1
                        mean = mean/len(row)

                        instanceName = file[:-4]
                        if len(optimum) > 1:
                            instanceName += "_" + str(i)
                    write_to_csv(max, min, mean, optimum[i], instanceName, algo.__name__, result_file)


# Need to add stats
# Probably ?
def write_to_csv(maxFit, minFit, mean, optimum, instance_name, algo_name, file):
    # Write to csv
    csv_file = open(file, "a", encoding="UTF8", newline="")
    writer = csv.writer(csv_file)
    writer.writerow([instance_name, algo_name, str(minFit), str(maxFit), str(mean), str(optimum)])
    csv_file.close()


def create_res_file(result_file):
    csv_file = open(result_file, "w", encoding="UTF8", newline="")
    writer = csv.writer(csv_file)
    # Write header
    writer.writerow(["instance", "min_fitness", "max_fitness", "mean", "optimum"])
    csv_file.close()


if __name__ == '__main__':
    main()
