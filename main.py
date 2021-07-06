'''
Main file, used to run the executable
'''
import sys
import getopt
import copy
from parse_data import Graph
from genetic_algorithm import GeneticAlgo
from approximation_algorithm import ApproxAlgo
from stochastic import Stochastic
from BnB import BnBmain
import sys, getopt
import matplotlib.pyplot as plt
import numpy as np
import random 

def main(argv):
    inst = None
    alg = None
    time = None
    seed = None
    # Try to parse command line arguments
    try:
        opts, args = getopt.getopt(argv,"hi:a:t:s:",["inst=","alg=", "time=", 'seed='])
    except getopt.GetoptError:
        print('Proper usage: main.py --inst <filename> --alg [BnB|Approx|LS1|LS2] --time <cutoff in seconds> --seed <random seed>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Proper usage: main.py --inst <filename> --alg [BnB|Approx|LS1|LS2] --time <cutoff in seconds> --seed <random seed>')
            sys.exit()
        elif opt in ("-i", "--inst"):
            inst = arg
        elif opt in ("-a", "--alg"):
            if arg == 'BnB' or arg == 'Approx' or arg == 'LS1' or arg == 'LS2':
                alg = arg
            else:
                print('Proper usage: main.py --inst <filename> --alg [BnB|Approx|LS1|LS2] --time <cutoff in seconds> --seed <random seed>')
                sys.exit()
        elif opt in ("-t", "--time"):
            time = arg
        elif opt in ("-s", "--seed"):
            seed = arg

    if seed is not None:
        random.seed(seed)
    else:
        seed = '100'
        random.seed(seed)

    # Construct graph
    G = Graph()
    G.parse_edges(inst)
    # BnB uses its own graph structure, so pass in the original file
    original_inst = copy.deepcopy(inst)

    # Remove extraneous information from file name
    if 'DATA/' in inst:
        inst = inst.replace('DATA/','')

    if '.graph' in inst:
        inst = inst.replace('.graph','')

    # Set output files
    if alg != 'BnB':
        sol_file = 'output/'+inst+'_'+alg+'_'+time+'_'+seed+'.sol'
        trace_file = 'output/'+inst+'_'+alg+'_'+time+'_'+seed+'.trace'
    else:
        sol_file = 'output/'+inst+'_'+alg+'_'+time+'.sol'
        trace_file = 'output/'+inst+'_'+alg+'_'+time+'.trace'

    # Check and run which algorithm was selected from the command line arguments
    if alg == "LS1":
        GeneticAlgo(G, int(time), seed, sol_file, trace_file)
    elif alg == "Approx":
        ApproxAlgo(G, int(time), seed, sol_file, trace_file)
    elif alg == "LS2":
        Stochastic(G, int(time), seed, sol_file, trace_file)
    elif alg == "BnB":
        BnBmain(original_inst, int(time), sol_file, trace_file)


if __name__ == "__main__":
   main(sys.argv[1:])

