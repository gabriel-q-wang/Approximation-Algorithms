'''
Parse the Graph files and store in a custom class
'''
class Graph:

    def __init__(self):   
        self.G = {}
        self.V = set()
        self.E = set()   
        self.Num_V = 0
        self.Num_E = 0

    '''
    Open files and parse them to create graph object
    '''
    def parse_edges(self, filename):
        # Write this function to parse edges from graph file to create your graph object
        f = open(filename, "r")
        first_line = True
        for i, line in enumerate(f):
            
            line_list = line.split(' ')

            if not first_line:
                # dummy files appear to have different formats from the others
                # Therefore, their solutions will be different and must be excluded from the others
                if 'dummy' in filename:
                    line_list = list(map(int, line_list)) 
                    vertex = line_list.pop(0)
                else:
                    # First line isn't as important, what's important is every line following
                    # Map the line number to their edges
                    line_list.pop(-1)
                    line_list = list(map(int, line_list)) 
                    vertex = i
                # If a vertex hasn't been added to the graph object, add it
                if vertex not in self.G.keys():
                    self.G[vertex] = set()
                    self.V.add(vertex)
                # Add te proper edges to the graph, if new vertex is found, add as well
                for node in line_list:
                    self.G[vertex].add(node)
                    self.V.add(node)
                    self.E.add((vertex, node))

                    if node not in self.G.keys():
                        self.G[node] = {vertex}
                    else:
                        self.G[node].add(vertex)

            else:
                # Parse the first line to get the number of vertices and edges
                first_line = False
                line_list = list(map(int, line_list)) 
                num_v, num_e, weight = line_list
                self.Num_V = num_v
                self.Num_E = num_e

        f.close()
        
        
