import numpy as np
from math import sqrt, atan
from karta import Point
from karta.raster import read_aai
from karta.crs import LonLatWGS84
from utm import from_latlon, to_latlon

def find_slope_pt(slon, slat, rlon, rlat, offset=1000):
    sx, sy, zs, ls = from_latlon(slat, slon)
    rx, ry, zr, lr = from_latlon(rlat, rlon)
    if not(zs == zr):
        raise NotImplementedError
    dist = sqrt((rx-sx)**2+(ry-sy)**2)
    slx = sx+(offset/dist)*(rx-sx)
    sly = sy+(offset/dist)*(ry-sy)
    return to_latlon(slx, sly, zs, ls)

class Bathymetry():
    def __init__(self, fn):
        self.bat = read_aai(fn)
        self.slope_offset = 1000
    def extent(self):
        return self.bat.extent

    def init_ray(self, src, rcv):
        sl_lat, sl_lon = find_slope_pt(*src, *rcv, self.slope_offset)
        depth_src = self.bat.sample(Point(*src, crs=self.bat.crs))
        depth_slope = self.bat.sample(Point(sl_lon, sl_lat, crs=self.bat.crs))
        init_angle = atan((depth_slope-depth_src)/self.slope_offset)
        return depth_src, init_angle