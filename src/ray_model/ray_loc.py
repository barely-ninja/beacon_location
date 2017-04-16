from sys import argv
from json import load

def make_prop_model(vel_data, abs_data, z_step):
    'Closure for sound propagation model func'
    #Linear model vs depth and frequency
    def prop_model(ind):
        
    return model

def make_propagator(prop_m, z_grid):
    def propagator(i, beta, r, s, atts):
        c, a = *prop_m(i)
        radius = c[0]/(c[2]*cos(beta))
        beta_o = acos(c[1]*cos(beta)/c[0])
        dr = radius*(sin(beta)-sin(beta_o))
        ds = radius*(beta-beta_o)
        dabs = a[0]*ds+a[1]*radius*(dr+(beta_o-beta)*(radius*cos(beta)-z_grid[i]))
        dspr = 20*log10*(1+ds/s)
        return beta_o, dr, dabs, dspr
    return propagator

def tl(freq, depth_s, depth_r):
    DEPTH_SOFAR = 1000
    if depth_r > DEPTH_SOFAR:
    def ray_model(src, recv):
        return radius
    return radial_func

def main(args):
    'main loop over datapoints'
    try:
        fn = argv[1]
    except IndexError:
        print('Please provide config file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)
    
    
if __name__ == '__main__':
    main(argv)