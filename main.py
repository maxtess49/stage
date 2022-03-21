import csv
import random
from models.gwo import gwo
from models.mkp import open_instance
from models.frame import *


def main():
    items, knapsack, optimum = open_instance("../instances/gk/gk01.dat")

    for i in range(len(knapsack)):
        with open('seeds.csv', 'r') as csvfile:
            seeds = csv.reader(csvfile, delimiter=';')
            for row in seeds:
                for seed in row:
                    random.seed(seed)
                    gwo(items[i], knapsack[i])


if __name__ == '__main__':
    main()
