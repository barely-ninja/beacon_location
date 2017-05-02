from math import pi, sqrt, log10, atan
from collections import namedtuple
from scipy.optimize import minimize_scalar
from ray import Ray

SoundProp = namedtuple('SoundProp', 'z c a')

def send_ray(ray, distance, z):
    result = next(ray)
    zf = result['z']>z
    pr_res = result
    while not result['r'] > distance:
        if zf and result['z'] == z:
            return result
        pr_res = result
        result = next(ray)
    return pr_res

def tl(result):
    s = result['r']
    labs = result['abs']
    tloss = 20*log10(s)+labs
    return tloss

class Rays():
    def __init__(self, ps, z_scale, iz_src, init_angle):
        self.props = [SoundProp(*row) for row in ps]
        self.beta = init_angle
        self.izs = iz_src
        self.z_scale = z_scale

    def have_ray(self, iz_rcv, distance):
        ray = Ray(self.beta, self.izs, self.props)
        result = send_ray(ray, distance, iz_rcv)
        if result['z'] < iz_rcv or tl(result) > 180:
            return False
        if result['z'] == iz_rcv and result['r'] < distance:
            return False
        return True

    def find_ray(self, iz_rcv, distance):

        def dist_func(beta):
            nonlocal self, distance, iz_rcv
            ray = Ray(beta, self.izs, self.props)
            result = send_ray(ray, distance, iz_rcv)
            dist = ((result['z']-iz_rcv)*self.z_scale)**2+(result['r']-distance)**2
            return dist

        max_ang = atan((iz_rcv-self.izs)*self.z_scale/distance)
        #print(self.izs, iz_rcv, distance, max_ang, self.beta)
        opt = minimize_scalar(dist_func, bounds=(max_ang-0.001, self.beta), method='bounded')
        beta = opt.x
        ray = Ray(beta, self.izs, self.props)
        result = send_ray(ray, distance, iz_rcv)
        return tl(result)

