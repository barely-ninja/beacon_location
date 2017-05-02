from sys import argv
from json import load
from itertools import product
import numpy as np
from matplotlib.pyplot import show, savefig, close, imshow, gca
from ocean import Ocean
from rays import Rays
from bathy import Bathymetry
from bounds import Bound

def make_loss_model(files, bathy, freq, rcv, bnd):
    ocean = Ocean(files['c'], files['a'])
    min_depth = 280
    max_depth = 6000
    z_step = 10
    z = np.arange(min_depth, max_depth, z_step)
    params = [(z[i], *ocean.evaluate(z[i], freq)) for i in range(len(z))]
    lat_rcv, lon_rcv, depth_rcv = rcv
    coords_rcv = (lon_rcv, lat_rcv)
    def tl_func(coords_src):
        nonlocal bathy, coords_rcv, depth_rcv, params, z_step, bnd, min_depth

        def zind(depth):
            nonlocal min_depth, z_step
            return (int)((depth-min_depth) // z_step)
        
        if bnd.is_in(coords_src):
            return 0
        
        distance, depth_src, init_angle = bathy.init_ray(coords_src, coords_rcv)
        iz_src = zind(depth_src)
        iz_rcv = zind(depth_rcv)
        rays = Rays(params, z_step, iz_src, init_angle)
        if rays.have_ray(iz_rcv, distance):
            tl = rays.find_ray(iz_rcv, distance)
        else:
            tl = 0
        return tl
    return tl_func

def main(args):
    try:
        fn = args[1]
    except IndexError:
        print('Please specify input file name')
    with open(fn, 'rt') as cfg_file:
        cfg = load(cfg_file)

    bathy = Bathymetry(cfg['bathy'])
    area = bathy.extent()
    bnd = Bound(cfg['bound'])
    grid_step = cfg['grid_step']
    x_iter = np.arange(area[0]+grid_step, area[1]-grid_step, grid_step)
    y_iter = np.arange(area[2]+grid_step, area[3]-grid_step, grid_step)
    dim_lon = len(x_iter)
    dim_lat = len(y_iter)
    dim_dets = len(cfg['sig_loss'])
    tl_list = []
    for point in cfg['sig_loss']:
        tl_func = make_loss_model(cfg['model_fn'], bathy, point['freq'], point['coords'], bnd)
        tl_grid = [tl_func((x, y)) for x, y in product(x_iter, y_iter)]
        tl_list.append(np.array(tl_grid).reshape((dim_lon, dim_lat)).T)
    all_conds = np.stack(tl_list, axis=2)
    conds_true = np.logical_and(np.all(all_conds > 0, axis=2), np.all(all_conds < 160, axis=2))
    #tl_grid = [y for x, y in product(x_iter, y_iter)]
    #conds_true = np.array(tl_grid).reshape((dim_lon, dim_lat)).T
    imshow(conds_true, origin='lower', cmap='coolwarm')
    ax = gca()
    xticks = np.arange(0, dim_lon, 5)
    yticks = np.arange(0, dim_lat, 5)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels([round((x+1)*grid_step+area[0],3) for x in xticks])
    ax.set_yticklabels([round((y+1)*grid_step+area[2],3) for y in yticks])
    show()
if __name__ == '__main__':
    main(argv)