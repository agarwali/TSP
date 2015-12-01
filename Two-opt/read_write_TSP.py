#-------------------------------------------------------------------------------------------
# Name:     read_write_TSP.py
# Purpose:  Class to read and write files containing co-ordinates for nearest_neighbour.py
# Programmers: Ishwar Agarwal(Driver) & Xhafer Rama(Navigator)
# Acknowledgement: None
# Created:     10/13/15
#-------------------------------------------------------------------------------------------


class TspRW(object):

    def __init__(self, ls=[], cd=[]):
        self.header = []    # a list containing the header section of the file
        self.labels = ls    # a list containg all the labels of vertices
        self.coordinates = cd   # a list containg all the cordinates of vertices
        self.filename = 0   # the input file name

    def read_file(self, filename):
        '''
        Pre: An ASCII file where each line will be the vertex number, x-coordinate, and y-coordinate separated by spaces
        Post: Updates self.labels and self.coordinates by extracting the labels from the ASCII file
        '''
        f = open(filename, 'r')
        for i in range(6):
            self.header.append(f.readline())    # reads and stores the header section of the file
        line = f.readline()
        while line != 'EOF':
            sp_line = line.split()
            self.labels.append(sp_line[0])  # append the vertex number for each line to labels
            self.coordinates.append((int(sp_line[1]),int(sp_line[2])))  # forms tuples with the x and y coordinates at each line and appends to self.coordinates
            line = f.readline()
        self.filename = filename    # updates the filename

    def write_file(self):
        '''
        Writes an ASCII file where each line contains the number of a single vertex
        listed in the order of the tour
        '''
        w_filename = self.filename[0:len(self.filename)-3]+'tour'   # creates a new file ASCII file with .tour extension
        w = open(w_filename, 'w')
        
        # Start of writing header
        w.write(self.header[0][0:len(self.header[0])-4]+'tour\n')    
        w.write(self.header[2][0:len(self.header[2])-4]+'TOUR\n')
        w.write(self.header[3])
        w.write('TOUR_SECTION\n')
        # End of writing header
        
        # Writes vertex number, x-coordinate, and y-coordinate separated by spaces at each line
        for i in range(len(self.labels)):
            w.write(self.labels[i] + ' ' + str(self.coordinates[i][0]) + ' ' + str(self.coordinates[i][1]) + '\n')
        w.write('-1')   # writes -1 at the end


