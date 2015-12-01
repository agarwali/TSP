# Runs
""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import string
import random
import math

from itertools import chain

try:
    from Gui import Gui, GuiCanvas
except ImportError:
    from swampy.Gui import Gui, GuiCanvas

from Graph import Vertex
from Graph import Edge
from Graph import Graph


class GraphCanvas(GuiCanvas):
    """a GraphCanvas is a canvas that knows how to draw Vertices
    and Edges"""

    def draw_vertex(self, v, r=0.45):
        """draw a Vertex as a yellow circle with radius (r)
        and text (v.label)"""
        tag = 'v%d' % id(self)

        try:
            color = v.color
        except:
            color = 'yellow'

        self.circle(v.pos, r, color, tags=tag)
        self.text(v.pos, v.label, 'black', tags=tag)
        return tag

    def draw_edge(self, e):
        """draw an Edge as a line between the positions of the
        Vertices it connects"""
        v, w = e
        tag = self.line([v.pos, w.pos])
        return tag


class GraphWorld(Gui):
    """GraphWorld is a Gui that has a Graph Canvas and control buttons.
	Some modifications made by Andres Berejnoi."""
    
    def __init__(self, title='GraphWorld',width=400,height=400,scaleFactor=20):
        Gui.__init__(self)
        self.title(title)
        self.setup(width,height,scaleFactor)

    def setup(self,width,height,scaleFactor):
        """Create the widgets."""
        self.ca_width = width
        self.ca_height = height
        xscale = self.ca_width / scaleFactor
        yscale = self.ca_height / scaleFactor
	#xscale = self.ca_width / 100
        #yscale = self.ca_height / 100

        # canvas
        self.col()
        self.canvas = self.widget(GraphCanvas, scale=[xscale, yscale],
                              width=self.ca_width, height=self.ca_height,
                              bg='white')
        
        # buttons
        self.row()
        self.bu(text='Clear', command=self.clear)
        self.bu(text='Quit', command=self.quit)
        self.endrow()

    def show_graph(self, g, layout):
        """Draws the Vertices and Edges of Graph (g) using the
        positions in Layout (layout).
        """

        # copy the positions from the layout into the Vertex objects
        for v in g.vertices():
            v.pos = layout.pos(v)
        
        # draw the edges and store the tags in self.etags, which maps
        # from Edges to their tags
        c = self.canvas
        self.etags = {}
        for v in g:
            self.etags[v] = [c.draw_edge(e) for e in g.out_edges(v)]

        # draw the vertices and store their tags in a list
        self.vtags = [c.draw_vertex(v) for v in g]

	
    def clear(self):
        """Delete all canvas items."""
        tags = chain(self.vtags, *self.etags.itervalues())
        for tag in tags:
            self.canvas.delete(tag)


class Layout(dict):
    """A Layout is a mapping from vertices to positions in 2-D space."""

    def __init__(self, g):
        for v in g.vertices():
            self[v] = (0, 0)

    def pos(self, v):
        """Returns the position of this Vertex as a tuple."""
        return self[v]

    def distance_between(self, v1, v2):
        """Computes the Euclidean distance between two vertices."""
        x1, y1 = self.pos(v1)
        x2, y2 = self.pos(v2)
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx**2 + dy**2)

    def sort_by_distance(self, v, others):
        """Returns a list of the vertices in others sorted in
        increasing order by their distance from v."""
        t = [(self.distance_between(v, w), w) for w in others]
        t.sort()
        return [w for (d, w) in t]


class CircleLayout(Layout):
    """Creates a layout for a graph with the vertices equally
    spaced around the perimeter of a circle."""

    def __init__(self, g, radius=9):
        """Creates a layout for Graph (g)"""
        vs = g.vertices()
        theta = math.pi * 2 / len(vs)
        for i, v in enumerate(vs):
            x = radius * math.cos(i * theta)
            y = radius * math.sin(i * theta)
            self[v] = (x, y)

class CartesianLayout(Layout):
	""" This class was added by Andres Berejnoi to work with the TSP class in the same folder.
	Creates a layout for a graph with the vertices in their cartesian positions
	assuming each vertex object has already an attribute .pos
	"""
	def __init__(self ,g, width=380, height=380, scaleFactor=21):
            """Sets up the layout for the graph using the already provided cartesian coordinates"""
            vs = g.vertices()
            
            #Calculating the limits of bounding box to center
            x_range = [v.pos[0] for v in vs]
            x_min = min(x_range)
            x_max = max(x_range)
            y_range = [v.pos[1] for v in vs]
            y_min = min(y_range)
            y_max = max(y_range)

            #Determining the range of the graph
            self.rangeX = abs(x_min) + abs(x_max)
            self.rangeY = abs(y_min) + abs(y_max)
            
            #print x_min,x_max,y_min,y_max
            centerBox = self._calculateBoxCenter(x_min,y_min,x_max,y_max)   #finds the center of bounding box
            self._center_graph(vs,centerBox)        #determines the layout of the graph
            
            #Applying scaling to make optimal use of screen:
            self.applyScaling(width,height,scaleFactor)

        def _determine_scaling(self,x_rangeWanted,y_rangeWanted,scaleFactor):
            """
            Determines the scaling coefficient to fit nodes to canvas.
            """
            #Calculates the biggest of the 
            #biggestWanted = max(x_rangeWanted,y_rangeWanted)
            target_width = float(x_rangeWanted)/scaleFactor
            target_height = float(y_rangeWanted)/scaleFactor
            #target = float(biggestWanted)/scaleFactor

            #calculates the bigger of self.rangeX and self.rangeY
            #realR = max(self.rangeX,self.rangeY)

            #calculating the value for reducing the coordinates to fit available screen
            #rdxFactor = target/realR
            rdxFactor_x = target_width/self.rangeX
            rdxFactor_y = target_height/self.rangeY
            return rdxFactor_x,rdxFactor_y
        
        def applyScaling(self,width,height,scaleFactor):
            """
            Adjusts the coordinates of each vertex to fit the desired canvas size.
            """
            rdxFactor_x,rdxFactor_y = self._determine_scaling(width,height,scaleFactor)
            for v in self:
                newX = self[v][0]*rdxFactor_x
                newY = self[v][1]*rdxFactor_y
                self[v] = (newX,newY)
                           
	def _calculateBoxCenter(self,minX,minY,maxX,maxY):
            """Takes the corners delimiting parameters of a box in 2D
            and determines its center.
            Return: a tuple containing the coordinates of the new center.
            """
            x_center = float(maxX+minX)/2
            y_center = float(maxY+minY)/2
            centerBox = (x_center,y_center)
            return centerBox
        
        def _center_graph(self,vs,centerBox):
            """
            Using the center of the graph nodes, and the list of nodes,
            it sets the positions in the layout with all the nodes centered.
            """
            for v in vs:
                if centerBox[0] > 0:
                    newX = (v.pos[0]-abs(centerBox[0]))
                else:
                    newX = (v.pos[0]+abs(centerBox[0]))
                if centerBox[1] > 0:
                    newY = (v.pos[1]-abs(centerBox[1]))
                else:
                    newY = (v.pos[1]+abs(centerBox[1]))
                self[v] = (newX,newY)
            
		
class RandomLayout(Layout):
    """Create a layout with each Vertex at a random position in
    [[-max, -max], [max`, max]]."""

    def __init__(self, g, max=10):
        """Creates a layout for Graph (g)"""
        self.max = max
        for v in g.vertices():
            self[v] = self.random_pos()

    def random_pos(self):
        """choose a random position and return it as a tuple"""
        x = random.uniform(-self.max, self.max)
        y = random.uniform(-self.max, self.max)
        return x, y

    def spread_vertex(self, v, others, min_dist=1.0):
        """Keep choosing random positions for v until it is at least
        min_dist units from the vertices in others.

        Each time it fails, it relaxes min_dist by 10%.
        """
        while True:
            t = [(self.distance_between(v, w), w) for w in others]
            d, w = min(t)
            if d > min_dist:
                break
            min_dist *= 0.9
            self[v] = self.random_pos()

    def spread_vertices(self):
        """Moves the vertices around until no two are closer together
        than a minimum distance."""
        vs = self.keys()
        others = vs[:]
        for v in vs:
            others.remove(v)
            self.spread_vertex(v, others)
            others.append(v)



def main(script, n='5', *args):

    # create n Vertices
    n = int(n)
    #labels = string.ascii_lowercase + string.ascii_uppercase
    #vs = [Vertex(c) for c in labels[:n]]

    v = Vertex('v')
    v.pos = (1110,-100)

    w = Vertex('w')
    w.pos = (20000,40)

    x = Vertex('x')
    x.pos = (100,-2000)

    y = Vertex('y')
    y.pos = (-15,15000)

    # create a graph and a layout
    g = Graph([v, w, x, y])
    g.add_all_edges()
    # layout = CircleLayout(g)
    # layout = RandomLayout(g)
    layout = CartesianLayout(g)

    # draw the graph
    gw = GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()


if __name__ == '__main__':
    import sys
    main(*sys.argv)


