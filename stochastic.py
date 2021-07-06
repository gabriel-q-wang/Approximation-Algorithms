"""
This code look for a minimum vertex cover.
Starting from a set of whole nodes in a given graph, iteratively remove a node as long as
the current set of nodes remains to be a vertex cover without the node. Keep iterations untill
either time is up or there is no more nodes we can remove.
"""
from parse_data import Graph
import time
import random
import sys
import matplotlib.pyplot as plt
import numpy as np
#import itertools

"""
this function counts the number of edges not covered by the candidate solution
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


def Stochastic(G, time_limit, seed, sol_file, trace_file):
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
    # make a list of nodes soted by its degree (lower degree --> higher degree)
    list_priority = make_priority_list(G)

    while len(list_priority) != 0 and time.time() - start < time_limit:
        v = random.sample(list_priority[0], 1)[0]
        vertex_cover.remove(v)
        if cost(G, vertex_cover) == 0:
            list_priority[0].remove(v)
            if len(list_priority[0]) == 0:
                list_priority.pop(0)
        else:
            list_priority[0].remove(v)
            if len(list_priority[0]) == 0:
                list_priority.pop(0)
            vertex_cover.add(v)
        runtime = time.time() - start
        output.write(str(runtime) + ", " + str(len(vertex_cover)) + "\n")
    return vertex_cover


"""
This function makes a list of nodes soted by its degree
Args:
    G: a graph
Return:
    a list of lists of nodes of the same degree sorted by its degree
    e.g. [[n1, n2, ...], [m1, m2, ..], ..., [s1, s2, ...]]
         n1, n2, ..., m1, m2, ..., s1, s2, ... all represent nodes
         deg(n1)=deg(n2) < deg(m1)=deg(m2) < deg(s1)=deg(s2)
"""


def make_priority_list(G):
    dic_priority = sorted(G.G.items(), key=lambda item: len(item[1]))
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
    return list_priority


"""
This function plots QRTD from the result of the algorithm
(fixed relative solution quality VS time)
Args:
    opt: optimal quality
    q1, q2, q3: relative solution quality (decimal number)
                e.g. 10 for q* = 10%
    start_time: cut-off time to start plotting
    end_time: cut-off time to end plotting
    tf1, tf2, tf3, tf4, tf5: a trace file output by this algorithm with different random seeds
"""


def qrtd(opt, q1, q2, q3, start_time, end_time, graph_name, tf1, tf2, tf3, tf4, tf5):
    target_quality1 = opt * (1 + q1 * 0.01)
    target_quality2 = opt * (1 + q2 * 0.01)
    target_quality3 = opt * (1 + q3 * 0.01)

    sample_size = 5
    cutoff = np.arange(start_time * 10000, end_time*10000)
    cutoff = cutoff / 10000.0
    fraction_list1 = np.zeros_like(cutoff)
    fraction_list2 = np.zeros_like(cutoff)
    fraction_list3 = np.zeros_like(cutoff)

    with open(tf1) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and quality <= target_quality1:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list1[i] = fraction_list1[i] + 1
                cont1 = 0
            if cont2 and quality <= target_quality2:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list2[i] = fraction_list2[i] + 1
                cont2 = 0
            if cont3 and quality <= target_quality3:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list3[i] = fraction_list3[i] + 1
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()
    print(fraction_list1)

    with open(tf2) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and quality <= target_quality1:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list1[i] = fraction_list1[i] + 1
                cont1 = 0
            if cont2 and quality <= target_quality2:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list2[i] = fraction_list2[i] + 1
                cont2 = 0
            if cont3 and quality <= target_quality3:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list3[i] = fraction_list3[i] + 1
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf3) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and quality <= target_quality1:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list1[i] = fraction_list1[i] + 1
                cont1 = 0
            if cont2 and quality <= target_quality2:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list2[i] = fraction_list2[i] + 1
                cont2 = 0
            if cont3 and quality <= target_quality3:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list3[i] = fraction_list3[i] + 1
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf4) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and quality <= target_quality1:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list1[i] = fraction_list1[i] + 1
                cont1 = 0
            if cont2 and quality <= target_quality2:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list2[i] = fraction_list2[i] + 1
                cont2 = 0
            if cont3 and quality <= target_quality3:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list3[i] = fraction_list3[i] + 1
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf5) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and quality <= target_quality1:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list1[i] = fraction_list1[i] + 1
                cont1 = 0
            if cont2 and quality <= target_quality2:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list2[i] = fraction_list2[i] + 1
                cont2 = 0
            if cont3 and quality <= target_quality3:
                for i in range(len(cutoff)):
                    if cutoff[i] >= runtime:
                        fraction_list3[i] = fraction_list3[i] + 1
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    fraction_list1 = fraction_list1 * 1.0 / sample_size
    fraction_list2 = fraction_list2 * 1.0 / sample_size
    fraction_list3 = fraction_list3 * 1.0 / sample_size

    title = 'QRTD' + ' (' + graph_name + ')'

    plt.plot(cutoff, fraction_list1, label='q*=' + str(q1)+'%')
    plt.plot(cutoff, fraction_list2, label='q*=' + str(q2)+'%')
    plt.plot(cutoff, fraction_list3, label='q*=' + str(q3)+'%')
    plt.title(title)
    plt.xlabel('run-time [CPU sec]')
    plt.ylabel('P(solve)')
    plt.legend()
    plt.show()


"""
This function plots SQD from the result of the algorithm
(fixed time VS relative solution quality)
"""


def sqd(opt, t1, t2, t3, end_q, graph_name, tf1, tf2, tf3, tf4, tf5):
    sample_size = 5
    qualities = np.arange(end_q)
    qualities = qualities
    fraction_list1 = np.zeros_like(qualities)
    fraction_list2 = np.zeros_like(qualities)
    fraction_list3 = np.zeros_like(qualities)

    q1 = [0, 0, 0]
    q2 = [0, 0, 0]
    q3 = [0, 0, 0]
    q4 = [0, 0, 0]
    q5 = [0, 0, 0]

    with open(tf1) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and runtime >= t1:
                q1[0] = quality
                cont1 = 0
            if cont2 and runtime >= t2:
                q1[1] = quality
                cont2 = 0
            if cont3 and runtime >= t3:
                q1[2] = quality
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf2) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and runtime >= t1:
                q2[0] = quality
                cont1 = 0
            if cont2 and runtime >= t2:
                q2[1] = quality
                cont2 = 0
            if cont3 and runtime >= t3:
                q2[2] = quality
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf3) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and runtime >= t1:
                q3[0] = quality
                cont1 = 0
            if cont2 and runtime >= t2:
                q3[1] = quality
                cont2 = 0
            if cont3 and runtime >= t3:
                q3[2] = quality
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf4) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and runtime >= t1:
                q4[0] = quality
                cont1 = 0
            if cont2 and runtime >= t2:
                q4[1] = quality
                cont2 = 0
            if cont3 and runtime >= t3:
                q4[2] = quality
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    with open(tf5) as book:
        cont1 = 1
        cont2 = 1
        cont3 = 1
        for line in book:
            l = line.split(',')
            runtime = float(l[0])
            quality = int(l[1])
            if cont1 and runtime >= t1:
                q5[0] = quality
                cont1 = 0
            if cont2 and runtime >= t2:
                q5[1] = quality
                cont2 = 0
            if cont3 and runtime >= t3:
                q5[2] = quality
                cont3 = 0
            if cont1 == 0 and cont2 == 0 and cont3 == 0:
                break
    book.close()

    qs = [q1, q2, q3, q4, q5]
    for i in range(len(qualities)):
        target_quality = opt * (1 + qualities[i] * 0.01)
        for q in qs:
            if q[0] <= target_quality:
                fraction_list1[i] = fraction_list1[i] + 1
        for q in qs:
            if q[1] <= target_quality:
                fraction_list2[i] = fraction_list2[i] + 1
        for q in qs:
            if q[2] <= target_quality:
                fraction_list3[i] = fraction_list3[i] + 1

    fraction_list1 = fraction_list1 * 1.0 / sample_size
    fraction_list2 = fraction_list2 * 1.0 / sample_size
    fraction_list3 = fraction_list3 * 1.0 / sample_size

    title = 'SQD' + ' (' + graph_name + ')'

    plt.plot(qualities, fraction_list1, label='t=' + str(t1)+'s')
    plt.plot(qualities, fraction_list2, label='t=' + str(t2)+'s')
    plt.plot(qualities, fraction_list3, label='t=' + str(t3)+'s')
    plt.title(title)
    plt.xlabel('relative solution quality [%]')
    plt.ylabel('P(solve)')
    plt.legend()
    plt.show()