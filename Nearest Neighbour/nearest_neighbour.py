#-------------------------------------------------------------------------------------------------------------
# Name:     nearest_neighbour.py
# Purpose:  Contains Nearest Neighbour class for calculating a tour in TSP using nearest neigbour heuristic 
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: Dr. Jan Pearce for the nearest neighbour pseudocode
# Created:     10/13/15
#-------------------------------------------------------------------------------------------------------------


from Graph import *
from GraphWorld import *
import math
import copy

class Nearest_Neighbour(object):

    def __init__(self, labels=[], coordinates = []):
        self.cost_of_best_tour_so_far = float('inf')    # sets cost of best tour to infinity inititally
        self.cost_of_tour = 0   # cost of one tour
        self.labels = labels    # a list containing all the labels of the vertices
        self.best_label = []    # a list containing all the labels for for a given tour 
        self.best_label_so_far = [] # a list containing all the labels for the best possible tour
        self.all_coordinates = coordinates  # a list containing all the given coordinates
        self.coordinates = []   # a list containing the deep copy of the given coordinates
        self.best_coordinates = []  # a list containing the coordinates in the order of travel for a given tour
        self.best_coordinates_so_far = []   # a list containing the coordinates in the order of travel for the best possible tour
        self.unvisited_cities = []  # a list containing all the unvivited citites(list of Vertex objects)
        self.vertices = [Vertex(c) for c in self.labels]    # a list of all the cities generated using all the labels
        self.best_tour = Graph(self.vertices)   # a graph object containing a given tour
        self.best_tour_so_far = Graph(self.vertices)    # a graph object containing the best tour so far
        self.currentcity = None # Vertex object to contain the current city
        self.currentcity_coordinate = ()    # a tuple containing the coordinates for the current city
        self.startcity = None   # Vertex containing the start city
        self.nearestcity = None # Vertex containing the nearest city
        self.cost_to_nearest_city = float('inf')    # Cost of travelling to the nearest city

        for i in range(len(self.vertices)):
            self.vertices[i].pos = self.all_coordinates[i]

    def mark_unvisited_cities(self):
        '''
        Marks all cities unvisited by resetting the list of coordinates and vertices
        '''
        self.coordinates = copy.deepcopy(self.all_coordinates)  # adds all the coordinates back in self.coordiantes
        self.vertices = [Vertex(c) for c in self.labels]    # add all the vertices back in self.vertices 
        for i in range(len(self.vertices)):
            self.vertices[i].pos = self.all_coordinates[i]

    def empty_tour(self):
        '''
        Clears all the edges of the current tour
        '''
        self.best_tour = Graph(self.vertices)   # resets self.best_tour to an empty graph containing vertices
        self.best_label = []    # empties self.best_label
        self.best_coordinates =[]   # epmties self.best_coordinates


    def calculate_nearneighbor(self):
        """
        Pre: List of all unvisitied vertices
        Post: Update the nearest city and cost of travelling to the nearest city
        """
        for i in range(len(self.vertices)): # goes through each city
            v = self.coordinates[i] # finds the coordinate of the next city
            distance = ((self.currentcity_coordinate[0]-v[0])**2+(self.currentcity_coordinate[1]-v[1])**2)**0.5 # distance of travelling to the next city
            if distance < self.cost_to_nearest_city:    
                self.cost_to_nearest_city = distance    # if distance is less the update cost 
                self.nearestcity = self.vertices[i]     # upade nearest city
                
        
    def mark_visited(self):
        '''
        Pre: list of all unvisited citites
        Post: pop current city from self.vertices and self.labels and add the city to best_coordinates and best_label
        '''
        self.currentcity_coordinate = self.coordinates[self.vertices.index(self.currentcity)]   # gets the coordinate for current city before removing it from the list
        i = self.vertices.index(self.currentcity)   # gets index for the current city in the list of vertices
        self.vertices.pop(i)    # removes the vertex of current city from the self.vertices
        n = self.coordinates.pop(i) # removes the cooordinate of current city from self.coordinates
        self.best_label.append(self.currentcity.label)  # adds the current cities label to the best_label
        self.best_coordinates.append(n) # adds the current city to the list of best_coordinates


    def add_currcity_tour(self):
        """ 
        Pre:
        Post: creates an edge between current city and nearest city
        """
        e = Edge(self.currentcity, self.nearestcity)    # creates and edge between current city and nearest city
        self.best_tour.add_edge(e)  # adds the edge to the graph best_tour


    def add_tourCost(self):
        """
        Pre: Takes in two parameters, the nearest city and the current city
        Post: Calculates the tourCost (i.e. calculates the distance between currentcity and nearest city)"""
        self.cost_of_tour += self.cost_to_nearest_city  # updates tour_cost
        self.cost_to_nearest_city = float('inf')    # resets cost_to_nearest city to infinity