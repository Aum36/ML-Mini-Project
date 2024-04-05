# Importing Modules
import numpy as np
import random
# Use 'conda install shapely' to import the shapely library.
from shapely.geometry import Polygon, Point
# Define the desired polygon 

poly = Polygon([(42.038588, -111.069844), (42.649184, -96.604851),(33.606807, -94.462420),(37.013355, -109.022082)])

def polygon_random_points (poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds
    points = []
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    return points
# Choose the number of points desired. This example uses 20 points. 
points = polygon_random_points(poly,1300)
# Printing the results.
for p in points:
    print(str(p.x)+","+str(p.y))

