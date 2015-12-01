#---------------------------------------------------------------------------------------------
# Name:     main.py
# Purpose:  Uses the Nearest Neighbour class and read_write_TSP to find the tour and plots
#           the tour using GraphWorld
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: Dr. Jan Pearce for the nearest neighbour pseudocode
# Created:     10/13/15
#---------------------------------------------------------------------------------------------

from nearest_neighbour import Nearest_Neighbour
from Graph import *
from GraphWorld import *
from read_write_TSP import TspRW


def main():
    read_write = TspRW()    # create a read_write object
    read_write.read_file(raw_input('Enter file to read from: '))    # reads all the coordinates of citties from an ASCII file
    l = read_write.labels   
    c = read_write.coordinates
    handle = Nearest_Neighbour(l, c)    # create a Nearest_neigbour class from the given vertices
    
    # for each vertex
    for i in handle.vertices:
        handle.mark_unvisited_cities()  # mark all the citites unvisited
        handle.empty_tour() # empties the tour
        handle.startcity = i    # set the city to start city
        handle.currentcity = handle.startcity   # sets the start city to current city
        handle.mark_visited()   # marks the city visited
        
        # while there is an unvisited city
        while len(handle.coordinates)!= 0:  
            handle.calculate_nearneighbor() # find the nearest neighbour for the current city
            handle.add_currcity_tour()  # adds the current city to the tour
            handle.add_tourCost()   # adds the cost to the tour
            handle.currentcity = handle.nearestcity # sets nearest city to current city
            handle.mark_visited()   # marks the current city visited
        e = Edge(handle.currentcity, handle.startcity)  # creates the last edge between the current and start city
        handle.best_tour.add_edge(e)    # add that last edge to best tour
        
        # updates best_tour_so_far if the last tour was lest costly
        if handle.cost_of_tour < handle.cost_of_best_tour_so_far :  
            handle.cost_of_best_tour_so_far = handle.cost_of_tour
            handle.best_tour_so_far = handle.best_tour
            handle.best_label_so_far = handle.best_label
            handle.best_coordinates_so_far = handle.best_coordinates

    # write the coordinates to an ASCII file with .tour extension
    read_write.coordinates = handle.best_coordinates_so_far
    read_write.labels = handle.best_label_so_far
    read_write.write_file()

    # print handle.best_tour_so_far
    # print handle.cost_of_best_tour_so_far
    # print handle.best_label_so_far
    # print handle.best_coordinates_so_far

    # for i in range(len(handle.best_label_so_far)):
    #     handle.best_label_so_far[i].pos = handle.best_coordinates_so_far

    # The following two lines allows to swtich the layout of the graph displayed
    layout = CartesianLayout(handle.best_tour_so_far)
    # layout = RandomLayout(handle.best_tour_so_far)

    # draw the graph
    gw = GraphWorld()
    gw.show_graph(handle.best_tour_so_far, layout)
    gw.mainloop()

main()