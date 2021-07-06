'''
This code look for a minimum vertex cover.
Uses genetic algorithms to search and optimize solutions.
Uses the python package DEAP for genetic algorithm tools
https://deap.readthedocs.io/en/master/
'''
import random
from deap import base, creator, tools, algorithms
import numpy
import matplotlib.pyplot as plt
import copy
import time

'''
Cost function used for local search
However, added an extra component to be used for multi-objective optimization
Try to minimize the number of edges uncovered
Also try to minimize the number of vertices used
'''
def cost(soln, graph):
    if len(soln) == 0:
        return (10000000000, 10000000000)

    graph_edges = graph.E
    noncovered = 0
    for edge in graph_edges:
        u, v = edge

        if u not in soln and v not in soln:
            noncovered += 1
    return (noncovered, len(soln))

'''
Initial the individual as the package intends
All individuals are considered set of vertices
'''
def initiate(container, func, n):
    initial_set = set()
    while len(initial_set) < n:
        initial_set.add(func())
    return container(initial_set)
'''
Crossover function used for genetic algorithms
Two individuals swap half the vertices that are unique to them
'''
def mate(individual1, individual2):
    if len(individual1) == 0 or len(individual2) == 0:
        return (individual1, individual2)
    new_ind_1 = copy.deepcopy(individual1)
    new_ind_2 = copy.deepcopy(individual2)
    # Find the unique vertices in each set
    ind_1_unique = new_ind_1.difference(new_ind_2) 
    ind_2_unique = new_ind_2.difference(new_ind_1)
    # Find the number of vertices to transfer
    num_1_transfer = int(len(ind_2_unique)/2)
    num_2_transfer = int(len(ind_1_unique)/2)
    # Exchange the vertices in the first individual
    for i in range(num_1_transfer):
        new_ind_1.remove(random.sample(new_ind_1, 1)[0])
        rand_choice = random.choice(tuple(ind_2_unique))
        ind_2_unique.remove(rand_choice)
        new_ind_1.add(rand_choice)
    # Exchange the vertices in the first individual  
    for i in range(num_2_transfer):
        new_ind_2.remove(random.sample(new_ind_2, 1)[0])
        rand_choice = random.choice(tuple(ind_1_unique))
        ind_1_unique.remove(rand_choice)
        new_ind_2.add(rand_choice)
    # Return two new individuals
    return (new_ind_1, new_ind_2)

'''
Mutation function for genetic algorithms
1/3 chance of the following possible mutations

1. Remove a random vertice
2. Add a random vertice
3. Replace a random vertice
'''
def mutate(individual1, low, up):
    if len(individual1) == 0:
        return (individual1,)
    roll = random.random()
    if roll <= 0.333333: # Replace
        new_ind = copy.deepcopy(individual1)
        new_ind.remove(random.sample(new_ind, 1)[0])
        new_ind.add(random.randint(low, up))
    elif roll <= 0.666666: # Remove
        new_ind = copy.deepcopy(individual1)
        new_ind.remove(random.sample(new_ind, 1)[0])
    else: # Add
        new_ind = copy.deepcopy(individual1)
        new_ind.add(random.randint(low, up))

    return (new_ind,)

'''
Genetic Algorithm Implemented from the DEAP Package
Needed to modify the original source code in order to properly write to the trace file
All of the other code is the same
'''
def modified_eaSimple(population, toolbox, cxpb, mutpb, stats=None,
             halloffame=None, trace_file=None, time_limit=None):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.
    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population
    :returns: A class:`~deap.tools.Logbook` with the statistics of the
              evolution
    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution. The
    logbook will contain the generation number, the number of evaluations for
    each generation and the statistics if a :class:`~deap.tools.Statistics` is
    given as argument. The *cxpb* and *mutpb* arguments are passed to the
    :func:`varAnd` function. The pseudocode goes as follow ::
        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
            evaluate(offspring)
            population = offspring
    As stated in the pseudocode above, the algorithm goes as follow. First, it
    evaluates the individuals with an invalid fitness. Second, it enters the
    generational loop where the selection procedure is applied to entirely
    replace the parental population. The 1:1 replacement ratio of this
    algorithm **requires** the selection procedure to be stochastic and to
    select multiple times the same individual, for example,
    :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
    Third, it applies the :func:`varAnd` function to produce the next
    generation population. Fourth, it evaluates the new individuals and
    compute the statistics on this population. Finally, when *ngen*
    generations are done, the algorithm returns a tuple with the final
    population and a :class:`~deap.tools.Logbook` of the evolution.
    .. note::
        Using a non-stochastic selection method will result in no selection as
        the operator selects *n* individuals from a pool of *n*.
    This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.
    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """
    start_time = time.perf_counter()
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    
    
    population.sort(key=lambda x: x.fitness, reverse=True)

    fitness_list = str(population[0].fitness)[1:-1].split(", ")
    curr_best_fitness = float(fitness_list[0]) + float(fitness_list[1])

    output = open(trace_file, 'w')
    curr_time = time.perf_counter()
    running_time = curr_time - start_time
    output.write(str(running_time) + ", " + str(int(float(fitness_list[1]))) + "\n")

    random.shuffle(population)
    # Begin the generational process
    gen = 1
    while running_time < time_limit:
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
            
        curr_time = time.perf_counter()
        running_time = curr_time - start_time
        
        population.sort(key=lambda x: x.fitness, reverse=True)
        fitness_list = str(population[0].fitness)[1:-1].split(", ")
        gen_best_fitness = float(fitness_list[0]) + float(fitness_list[1])
        if gen_best_fitness < curr_best_fitness:
            curr_best_fitness = gen_best_fitness
            output.write(str(running_time) + ", " + str(int(float(fitness_list[1]))) + "\n")

        random.shuffle(population)

        gen += 1

    return population, logbook

'''
Main function to define our definition of an individual
Initiates the population and sets the objectives we are trying to minimize
Calls the above helper functions
'''
def GAMain(G, time, seed, trace_file):
    random.seed(seed)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,-1.0))
    creator.create("Individual", set, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("vertex", random.randint, 1, G.Num_V)
    toolbox.register("individual", initiate, creator.Individual, toolbox.vertex, n=G.Num_V)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", cost, graph=G)
    toolbox.register("mate", mate)
    toolbox.register("mutate", mutate, low=1, up=G.Num_V)
    toolbox.register("select", tools.selTournament, tournsize=2)

    pop = toolbox.population(n=1000)
    pareto = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    
    pop, logbook = modified_eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.5, stats=stats, halloffame=pareto, trace_file=trace_file, time_limit=time)

    return pop, logbook, pareto


'''
Write the best individual found into the solution file
'''
def GeneticAlgo(G, time, seed, sol_file, trace_file):
    pop, log, pareto = GAMain(G, time, seed, trace_file)
    pop.sort(key=lambda x: x.fitness, reverse=True)

    fitness_list = str(pop[0].fitness)[1:-1].split(", ")
    output = open(sol_file, 'w')
    output.write(str(int(float(fitness_list[1]))) + "\n" + str(set(pareto[0]))[1:-1] + "\n")
    


