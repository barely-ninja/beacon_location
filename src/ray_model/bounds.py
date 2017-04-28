from karta import Point, Polygon, read_shapefile
from karta.crs import LonLatWGS84

class Bound():
    def __init__(self, fn):
        self.bnds = read_shapefile(fn)
    def is_in(self, pt):
        return self.bnds[0].contains(Point((*pt), crs=LonLatWGS84))

