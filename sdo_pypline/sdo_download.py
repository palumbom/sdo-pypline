import numpy as np
import pandas as pd
import datetime as dt
import astropy.units as u
import argparse, warnings
import os, sys, pdb, time, glob
from sunpy.net import Fido, attrs as a
from sunpy.time import TimeRange
from astropy.units.quantity import AstropyDeprecationWarning
import pdb

def download_data(outdir=None, start=None, end=None, sample=None, overwrite=False):
    # set time attributes for search
    start += 'T00:00:00'
    end += 'T24:00:00'
    trange = a.Time(start, end)
    sample = a.Sample(sample * u.hour)
    provider = a.Provider("JSOC")

    pdb.set_trace()

    # set attributes for HMI query
    instr1 = a.Instrument.hmi
    physobs = (a.Physobs.los_velocity | a.Physobs.los_magnetic_field | a.Physobs.intensity)

    # set attributes for AIA query
    level = a.Level(1)
    instr2 = a.Instrument.aia
    wavelength = a.Wavelength(1700. * u.AA)

    # get query for HMI and download data, retry failed downloads
    vel, mag, con = Fido.search(trange, instr1, physobs, provider, sample)
    hmi_files = Fido.fetch(vel, mag, con, path=outdir, overwrite=overwrite, progress=False)
    while len(hmi_files.errors) > 0:
        hmi_files = Fido.fetch(hmi_files, path=outdir, overwrite=overwrite, progress=False)

    # get query for AIA and download data
    aia = Fido.search(trange, instr2, wavelength, level, provider, sample)
    aia_files = Fido.fetch(aia, path=outdir, overwrite=overwrite, progress=False)
    while len(aia_files.errors) > 0:
        aia_files = Fido.fetch(aia_files, path=outdir, overwrite=overwrite, progress=False)
    pdb.set_trace()
    return

def main():
    # supress warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=AstropyDeprecationWarning)

    # initialize argparser
    parser = argparse.ArgumentParser(description='Download SDO data from JSOC',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('outdir', type=str, help='full directory path for file writeout')
    parser.add_argument('start', type=str, help='starting date formatted as YYYY/MM/DD')
    parser.add_argument('end', type=str, help='ending date formatted as YYYY/MM/DD')
    parser.add_argument('sample', type=int, help='cadence of sampling in hours')

    # parse the command line arguments
    args = parser.parse_args()
    outdir = args.outdir
    start = args.start
    end = args.end
    sample = args.sample

    # now download the data
    files = download_data(outdir=outdir, start=start, end=end, sample=sample, overwrite=False)
    return None

if __name__ == '__main__':
    main()
