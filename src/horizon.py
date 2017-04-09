from sys import argv
from json import load

def make_radial_func(params):
    'Closure for radial distance func'
    def radial_func(x,y):
        return radius
    return radial_func

def main(args):
    'main loop over constraints'
    try:
        fn = argv[1]
    except IndexError:
        print('Please provide config file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)
    
if __name__ == '__main__':
    main(argv)