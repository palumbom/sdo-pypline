import numpy as np
import matplotlib.pyplot as plt
import os, pdb, glob, time, argparse
from os.path import exists, split, isdir, getsize

# bring functions into scope
from sdo_pypline.paths import root
from sdo_pypline.sdo_io import *
from sdo_pypline.sdo_process import *

# multiprocessing imports
from multiprocessing import get_context
import multiprocessing as mp

# use style
plt.style.use(str(root) + "/" + "my.mplstyle"); plt.ioff()

def get_parser_args():
    # initialize argparser
    parser = argparse.ArgumentParser(description="Analyze SDO data")
    parser.add_argument("--clobber", action="store_true", default=False)
    parser.add_argument("--globexp", type=str, default="")

    # parse the command line arguments
    args = parser.parse_args()
    clobber = args.clobber
    globexp = args.globexp
    return clobber, globexp

def main():
    # define sdo_data directories
    indir = "/Users/michael/Desktop/sdo_data/"
    if not isdir(indir):
        indir = "/storage/home/mlp95/scratch/sdo_data/"

    # sort out input/output data files
    clobber, globexp = get_parser_args()
    files = organize_input_output(indir, clobber=clobber, globexp=globexp)
    con_files, mag_files, dop_files, aia_files = files

    # set mu threshold, number of mu rings
    n_rings = 10
    mu_thresh = 0.1
    plot = False

    # get number of cpus
    try:
        from os import sched_getaffinity
        print(">>> OS claims %s CPUs are available..." % len(sched_getaffinity(0)))
        ncpus = len(sched_getaffinity(0)) - 1
    except:
        # ncpus = np.min([len(con_files), mp.cpu_count()])
        ncpus = 1

    # process the data either in parallel or serially
    if ncpus > 1:
        # prepare arguments for starmap
        items = []
        for i in range(len(con_files)):
            items.append((con_files[i], mag_files[i], dop_files[i], aia_files[i], mu_thresh, n_rings))

        # run in parellel
        print(">>> Processing %s epochs with %s processes..." % (len(con_files), ncpus))
        t0 = time.time()
        pids = []
        with get_context("spawn").Pool(ncpus, maxtasksperchild=4) as pool:
            # get PIDs of workers
            for child in mp.active_children():
                pids.append(child.pid)

            # run the analysis
            pool.starmap(process_data_set_parallel, items, chunksize=8)

        # find the output data sets
        datadir = str(root / "data") + "/"
        tmpdir = datadir + "tmp/"
        outfiles1 = glob.glob(tmpdir + "intensities_*")
        outfiles2 = glob.glob(tmpdir + "disk_stats_*")
        outfiles3 = glob.glob(tmpdir + "velocities_*")
        outfiles4 = glob.glob(tmpdir + "mag_stats_*")

        # stitch them together on the main process
        stitch_output_files(datadir + "intensities.csv", outfiles1, delete=True)
        stitch_output_files(datadir + "disk_stats.csv", outfiles2, delete=True)
        stitch_output_files(datadir + "velocities.csv", outfiles3, delete=True)
        stitch_output_files(datadir + "mag_stats.csv", outfiles4, delete=True)

        # print run time
        print("Parallel: --- %s seconds ---" % (time.time() - t0))
    else:
        # run serially
        print(">>> Processing %s epochs on a single process" % len(con_files))
        t0 = time.time()
        for i in range(len(con_files)):
            process_data_set(con_files[i], mag_files[i], dop_files[i], aia_files[i],
                             mu_thresh=mu_thresh, n_rings=n_rings)

        # print run time
        print("Serial: --- %s seconds ---" % (time.time() - t0))
    return None

if __name__ == "__main__":
    main()
