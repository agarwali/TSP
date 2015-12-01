# ---------------------------------------------------------------------------------------------
# Name:     TSP.py
# Purpose:  Implement the Branch and Bound algorithm through a BNB class
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: None
# Created:     11/22/15
# ---------------------------------------------------------------------------------------------

from Graph import *
from math import sqrt

class BNB():

    def __init__(self, coordinates):
        self.coordinates = coordinates   # a list of coordinates in lexographical order
        self.tour = []  # a tour list that stores the optimal solution in order
        self.tourGraph = Graph(coordinates) # a graph object containing the optimal solution
    
    def distance(self, v1, v2):
        '''
        Precondition: Two vertex objects should be passed as parameters
        Postcondition: Calculates and returns distance between two vertices
        '''
        # uses the ditance formula: sqrt of (y2 - y1)^2 + (x2 - x1)^2
        d1 = v2.pos[1]*1.0 - v1.pos[1]*1.0 # y2 - y1
        d2 = v2.pos[0]*1.0 - v1.pos[0]*1.0  # x2 - x1
        dis = sqrt(d1**2 + d2**2)
        return dis
        
    def compute_bound(self, v):
        '''
        Precondition: a vertex object should be passed as parameter
        Postcondition: Calculates and returns the lower bound for the vertx v,
        by computing the smallest edge in and out of v
        '''
        bound = self.distance(self.tour[-1], v) # the distance of the edge coming in to V
        
        # this part finds the distance of smallest edge going out of v
        nextBound = float('inf')
        for vertex in self.coordinates:
            newBound = 0.0  # initilaze a newBound float type variable
            if v != vertex:
                newBound = self.distance(v, vertex)
                if newBound < nextBound: # if a smaller edge is found next bound is new bound
                    nextBound = newBound
                else:
                    pass
            else:
                pass
        
        bound += nextBound  # adds the smallest edge out of V to bound
            
        return bound
        
    def chop(self):
        '''
        Precondition: None
        Conceptually this function does pruning part of Branch and Bound Algorithm
        It checks all the next possible nodes in the tour and returns the node 
        with lowest bound. So it conceptually prunes all other nodes that can
        never lead to an optimal solution.
        '''
        bestBound = float('inf')
        bestVertex = None

        if len(self.coordinates) == 1:
            return self.coordinates[0]

        for vertex in self.coordinates:
            tempBound = self.compute_bound(vertex)
            if tempBound < bestBound:
                bestBound = tempBound
                bestVertex = vertex
        return bestVertex

    def explore(self):
        '''
        This function calls the chop function at every node and stores the
        next node in self.tour and self.tourGraph
        '''
        # adds the starting point or root node in self.tour
        startVertex = self.coordinates.pop(0)
        self.tour.append(startVertex)
        currentVertex = startVertex
        
        # find all other nodes in the tour
        while len(self.coordinates) != 0:
            nextVertex = self.chop() # finds the next node by pruning all other possible nodes
            self.tour.append(nextVertex) # adds the new node to self.tour
            self.coordinates.remove(nextVertex) # removes the found node using the remove function
            
            edge = Edge(currentVertex, nextVertex) # adds an edge between the least bound between two nodes
            self.tourGraph.add_edge(edge) # adds the edge to the graph

            currentVertex = nextVertex # sets the previous node to the new node that has least bound

        lastEdge = Edge(currentVertex, startVertex) # adds the last edge to the starting vertex
        self.tourGraph.add_edge(lastEdge)