'''
Unused, now use Stochastic.py
'''
from parse_data import Graph
import time
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
#import itertools 

"""
Args:
    G: a graph
    C: candidate solution (a set of nodes)
Return: 
    cost: # E not covered by C
         (if cost==0 -> C is a vertex cover)
"""
def cost(G, C):
    cost = 0
    for e in G.E:
      if e[0] not in C and e[1] not in C:
        cost = cost + 1
    return cost


"""
Args:
    G: a graph
    time_limit: cuttoff time
    seed: random seed
Return: 
    vertex_cover: vertex cover
"""
def HillClimbing(G, time_limit, seed, sol_file, trace_file):
    random.seed(seed)
    mvc = find_mvc(G, time_limit, seed, trace_file)

    output = open(sol_file, 'w')
    output.write(str(len(mvc)) + "\n")
    i = 1
    for v in mvc:
        output.write(str(v))
        if i < len(mvc):
            output.write(",")
        i += 1

    output.write("\n")


  
"""
Args:
    G: a graph
    time_limit: cuttoff time
    seed: random seed
Return: 
    vertex_cover: vertex cover
"""
def find_mvc(G, time_limit, seed, trace_file):
    start = time.time()

    output = open(trace_file, 'w')

    # initialization (a set of all the nodes in G)
    vertex_cover = G.V.copy()
    # make a list of nodes soted by its degree
    dic_priority = sorted(G.G.items(), key = lambda item : len(item[1]))
    list_priority = []
    curr_size = -1
    curr_idx = -1
    for key in dic_priority:
        neighbors = key[1]
        if curr_size < len(neighbors):
            list_priority.append([])
            curr_idx = curr_idx + 1
            curr_size = len(neighbors)
        list_priority[curr_idx].append(key[0])

    
    #cont = False
    while len(list_priority) != 0 and time.time() - start < time_limit:
        v = random.sample(list_priority[0], 1)[0]
        vertex_cover.remove(v)
        if cost(G, vertex_cover) == 0:
            list_priority[0].remove(v)
            #cont = True
            if len(list_priority[0]) == 0:
                list_priority.pop(0)
        else:
            list_priority[0].remove(v)
            if len(list_priority[0]) == 0:
                list_priority.pop(0)
            vertex_cover.add(v)
        runtime = time.time() - start
        output.write(str(runtime) + ", " + str(len(vertex_cover)) + "\n")
    #if not cont:
    print(cost(G, vertex_cover))
    return vertex_cover
