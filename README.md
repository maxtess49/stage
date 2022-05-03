# Welcome to the jungle
## Project of my internship at LERIA 

### Objectives: 
    - Implement bGWO, SLMS
      - A binary grey wolf optimizer for the multidimensional knapsack problem
        (Kaiping Luo, Qiuhong Zhao)
      - A binary moth search algorithm based on self-learning for multidimensional knapsack problems  
        (Yanhong Feng, Gai-Ge Wang)

    - Develop a kind of general metaheuristics algorithm from those

### TODO
- General algorithm

### DOING
- General algorithm
  - [ ] Get a framework working
  - [ ] (optionnal) make it with the deap library
    - [ ] Make MKP model

### DONE
- Implementation of the Multi dimensional Knapsack Problem
  - [X] Initialization of instances
  - [X] Model
  - [X] Fitness function
  - [X] Pseudo utility

- bGWO
  - [X] Make an algorithm from scratch
    - [X] Initialisation pseudo utility
    - [X] Initialisation 0
    - [X] Initialisation random
    - [X] Identify leaders (init)
    - [X] Estimate the position of the prey (selection part 1 ?)
    - [X] Generate solution (selection)
    - [X] Repair (mutate)
    - [X] Update population (Insertion)
    - [X] Frame
  - [X] find where to generalize

- SLMS
    - [X] Make an algorithm from scratch
    - [X] Initialisation random
    - [X] Generate initial solution
    - [X] Generate solution
      - [X] Repair
    - [X] find where to generalize

- PSO
  - [X] Make a simple PSO 
    - [X] Modify it to try to get better results
    - [ ] Use parts of metaphor based algorithm to make a general pso algorithm resembling both gwo & slms
      - [X] use different formulas
      - [ ] Change the framework of the pso to look like gwo & slms


### Dependencies
- numpy
- scipy

See requirements.txt

### Launch
### \TODO