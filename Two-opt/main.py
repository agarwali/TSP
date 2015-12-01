# ---------------------------------------------------------------------------------------------
# Name:     main.py
# Purpose:  Uses the Nearest Neighbour class and read_write_TSP to find the tour and plots
#           the tour using GraphWorld
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: Dr. Jan Pearce for the two opt pseudocode
# Created:     10/13/15
# ---------------------------------------------------------------------------------------------

from two_opt import TwoOpt
from GraphWorld import *
from read_write_TSP import TspRW
import time

def main():

    time.clock()
    object = TwoOpt()   # create a two-opt object

    read_write = TspRW()    # create a read_write object
    read_write.read_file(raw_input('Enter file to read from: '))    # reads all the coordinates of citties from an ASCII file
    object.labels = read_write.labels   # store the labels in a list
    object.coordinates = read_write.coordinates      # store the coordinates in this list

    numRound = int(raw_input('Enter the number of random graphs you want to generate: '))
    roundTimes = int(raw_input('Enter the number of times you want to swap edges: '))

    for i in range(numRound):
        object.generate_rand_graph()    # generate a random graph
        for i in range(roundTimes):
            object.generate_rand_vertices()    # randomly generate two indices which have no common connection
            object.find_random_edge()   # generate two random edges from the given indices
            object.find_new_edge()  # find the new edge if swap were to happen.

            dx_oldtour = object.cal_distance_of_edge(object.edge1) + object.cal_distance_of_edge(object.edge2)  # difference in cost before swapping using two-opt
            dx_newtour = object.cal_distance_of_edge(object.new_edge1) + object.cal_distance_of_edge(object.new_edge2)    # difference in cost after adding two edges.
            if dx_newtour < dx_oldtour:
                object.remove_edges()
                object.add_edge_reversely()
        if object.costOfBestTour > object.costOfTour:
            bestTour = object.tour
            bestTour_vertices = object.tour_vertices
            object.costOfBestTour = object.costOfTour

    # write the tour in .tour ASCII file
    read_write.coordinates = []
    read_write.labels = []
    for i in bestTour_vertices:
        read_write.coordinates.append(i.pos)
    for i in bestTour_vertices:
        read_write.labels.append(i.label)
    read_write.write_file()

    print 'Run time: ', time.clock()

    # The following two lines allows to switch the layout of the graph displayed
    # layout = CartesianLayout(bestTour)
    layout = RandomLayout(bestTour)
    # layout = CircleLayout(bestTour)
    # draw the graph
    gw = GraphWorld()
    gw.show_graph(bestTour, layout)
    gw.mainloop()



main()