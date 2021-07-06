'''
This code creates the MVC by selecting an edge for the list of edges in the graph and removing all edges that have either of the two vertices connected to that edge. The both vertices are added to the output list.

The code runs until all edges are removed
'''
import random
import time

def ApproxAlgo(G, time, seed, sol_file, trace_file):
    # Generates a random seed and for the CreateMVC function
    random.seed(seed)

    vertices = CreateMVC(G, time, trace_file)
    output = open(sol_file, 'w')
    output.write(str(len(vertices)) + "\n")

    # Iterate through the chosen vertices to add to the output file
    i = 1
    for v in vertices:
        output.write(str(v))
        if i < len(vertices):
            output.write(",")
        i += 1

    output.write("\n")


def CreateMVC(G, time_limit, trace_file):
    start_time = time.perf_counter()

    output = open(trace_file, 'w')

    # Initalize the sets
    unusedEdges = G.E.copy()
    setVertices = set()

    running_time = 0

    # Go until all edges are covered  or time limit exceeded
    while running_time < time_limit and len(unusedEdges) != 0:
        # Randomly select and edge to remove and add the vertices to setVertices
        element = random.sample(unusedEdges, 1)[0]
        unusedEdges.remove(element)
        setVertices.add(element[0])
        setVertices.add(element[1])

        # filter the list of edges
        removeSet = set()
        for e in unusedEdges:
            if element[0] == e[0] or element[0] == e[1] or element[1] == e[0] or element[1] == e[1]:
                removeSet.add(e)
        for e in removeSet:
            unusedEdges.remove(e)

        curr_time = time.perf_counter()
        running_time = curr_time - start_time

    # Output time it took to finish the algorithm
    curr_time = time.perf_counter()
    running_time = curr_time - start_time
    output.write(str(running_time) + ", " + str(len(setVertices)) + "\n")

    return setVertices
