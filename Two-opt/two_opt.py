# ---------------------------------------------------------------------------------------------
# Name:     two_opt.py
# Purpose:  Implement the 2-opt algorithm through a 2-opt class
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: Dr. Jan Pearce for the two opt pseudocode
# Created:     10/13/15
# ---------------------------------------------------------------------------------------------

from Graph import *
from GraphWorld import *
import random
import copy

class TwoOpt():

    def __init__(self):
        self.tour_vertices = []     # creates a sequential list of vertices for a given TSP tour
        self.tour_edges = []        # creates a list of edges for a particular tour
        self.costOfBestTour = float('inf')    # cost of best tour, initially infinity
        self.costOfTour = 0     # cost of one tour
        self.index1 = 0   # a randomly picked edge
        self.index2 = 0   # a randomly picked second edge
        self.labels = []    # a list of labels read from .tsp file
        self.coordinates = []   # a list of coordinates read from .tsp file
        self.tour = Graph()  # a graph object that contains a tour of TSP

        self.edge1 = None  # stores one of the two edges to be replaced as a result of 2-opt
        self.edge2 = None
        self.new_edge1 = None # stores one of the two new edges to be created after 2-opt
        self.new_edge2 = None

    def cal_distance_of_edge(self, edge):
        '''
        Returns the distance of an given edge
        '''
        vertex1 = edge[0]   # finds the first vertex for the edge
        vertex2 = edge[1]   # finds the second vertex of the edge
        return ((vertex1.pos[0]-vertex2.pos[0])**2+(vertex1.pos[1]-vertex2.pos[1])**2)**0.5     # return the distance
    
    def generate_rand_graph(self):
        '''
        Pre: A list if lables and coordinates
        Post: Updates self.tour with a randomly generated graph and
            and updates self.costOfTour with the cost of that generated tour
        '''
        copyOfLabels = copy.deepcopy(self.labels)   # creates a copy of labels
        copyofCoordinates = copy.deepcopy(self.coordinates) # creates a copy of coordinates

        self.tour_edges = []    # reset tour edges
        self.tour_vertices = [] # reset tour vertices

        i = random.randrange(0, len(copyOfLabels))  # generate a random first city
        start_city = Vertex(copyOfLabels.pop(i))
        start_city.pos = copyofCoordinates.pop(i)
        previous_city = start_city  # assign start city to previous city

        self.tour_vertices.append(start_city)   # append it to tour vertices

        for x in range(len(copyOfLabels)):  # find the next random naumber
            i = random.randrange(0, len(copyOfLabels))
            v = Vertex(copyOfLabels.pop(i)) # pop that vertex at that random number
            v.pos = copyofCoordinates.pop(i)    # pop out the coordinate for that vertex and create that new vertex
            self.tour_vertices.append(v)    # append it to the list
            e = Edge(previous_city, v)  # create a new edge between the previous city and new randomly generated city
            self.tour_edges.append(e)   # append the edge to edge list
            self.costOfTour += self.cal_distance_of_edge(e) # update the cost of the tour for travelling to the new city
            previous_city = v   # assign the new city to previous city

        e = Edge(previous_city, start_city)     # join the last edge to go back to the start city
        self.tour_edges.append(e)
        self.tour = Graph(self.tour_vertices, self.tour_edges)
        self.costOfTour += self.cal_distance_of_edge(e) # update teh cost of the tour for going back to the start city
    
    def generate_rand_vertices(self):
        '''
        Pre: self.tour is a randomly generated graph
        Post: Randomly select two indices from the vertex list, whose subsequent vertices are note same.
        '''
        index_list = list(xrange(len(self.tour_vertices)))  # creates an list of indices of tour_vertices
        ran_num = random.randrange(len(index_list)-1)   # finds a random index
        self.index1 = index_list[ran_num]

        # creates a new list separating the already selected index and the indices before and after the selected index.
        if self.index1 == 0:
            new_index_list = index_list[2:-1]
        elif self.index1 == len(index_list)-1:
            new_index_list = index_list[1:len(index_list)-2]
        else:
            new_index_list = index_list[ran_num+2:]+ index_list[:ran_num-1]

        ran_num_2 = random.randrange(len(new_index_list)-1)  # find a second random index from the new list
        self.index2 = new_index_list[ran_num_2]

    def find_random_edge(self):
        '''
        find the corresponding edges from the list of vertices using the randomly generated indices
        '''
        x1 = self.tour_vertices[self.index1-1]
        y1 = self.tour_vertices[self.index1]
        x2 = self.tour_vertices[self.index2-1]
        y2 = self.tour_vertices[self.index2]
        self.edge1 = Edge(x1, y1)
        self.edge2 = Edge(x2, y2)

    def remove_edges(self):
        """ 
        Pre: edge1 and edge2 should be given by generate random edges
        Post: Removes edge1 and edge2 from self.tour"""
        self.tour.remove_edge(self.edge1)
        self.tour.remove_edge(self.edge2)

    def find_new_edge(self):
        '''
        Switch (x1,y1) and (x2,y2) with (x1, x2) and (y1, y2) for creating two new edge
        '''
        x1 = self.tour_vertices[self.index1-1]
        y1 = self.tour_vertices[self.index1]
        x2 = self.tour_vertices[self.index2-1]
        y2 = self.tour_vertices[self.index2]
        self.new_edge1 = Edge(x1, x2)  # create a new edge by switching the vertices
        self.new_edge2 = Edge(y1, y2)

    def add_edge_reversely(self):
        '''
        Pre: self.new_edge1 and self.new_edge2 is present
        Post: Updates the self.tour with two newly generated edges
        '''
        self.tour.add_edge(self.new_edge1)
        self.tour.add_edge(self.new_edge2)

        # updates the self.tour_vertices such that vertices are in sequential order of a directed graph
        if self.index1 < self.index2:
            reverse_lis = self.tour_vertices[self.index1:self.index2]
            reverse_lis.reverse() # reverses the part of the vertices list in the middle of two chosen vertices
            self.tour_vertices = self.tour_vertices[:self.index1] + reverse_lis + self.tour_vertices[self.index2:]
        else:
            reverse_lis = self.tour_vertices[self.index2:self.index1]
            reverse_lis.reverse()
            self.tour_vertices = self.tour_vertices[:self.index2] + reverse_lis + self.tour_vertices[self.index1:]

