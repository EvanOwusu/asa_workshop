#! /usr/bin/env python3 
"""
Determine Andromeda location in ra/dec degrees
"""
from numpy.random import uniform
from math import cos, pi, sin
import argparse
import mymodule
import logging
import numpy as np

NSRC = 5000000

def clip_to_radius():
    pass
# from wikipedia


def get_radec():        
    """
    Generate the ra & dec coordinates of Andromeda
    in decimal degrees. ra is the right ascension in the sky, and
    dec is the declination.

    Returns
    -------
    ra : float
        The RA, in degrees, for Andromeda
    dec : float
        The DEC, in degrees for Andromeda
    """
    # from wikipedia
    andromeda_ra = '00:42:44.3'
    andromeda_dec = '41:16:09'

    d, m, s = andromeda_dec.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = andromeda_ra.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)
    return ra,dec


def skysim_parser():
    """
    Configure the argparse for skysim

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser for skysim.
    """
    parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-')
    parser.add_argument('--ra', dest = 'ra', type=float, default=None,
                        help="Central ra (degrees) for the simulation location")
    parser.add_argument('--dec', dest = 'dec', type=float, default=None,
                        help="Central dec (degrees) for the simulation location")
    parser.add_argument('--out', dest='out', type=str, default='catalog.csv',
                        help='destination for the output catalog')
    parser.add_argument('--logging', type=str, default=logging.INFO,
                        help='Logging level from (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    return parser



def make_stars(ra, dec, nsrc=NSRC):
    """
    Generate NSRC stars within 1 degree of the given ra/dec

    Parameters
    ----------
    ra,dec : float
        The ra and dec in degrees for the central location.
    nsrc : int
        The number of star locations to generate
    
    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates.
    """
    ras = []
    decs = []
    for _ in range(nsrc):
        ras.append(ra +uniform(-1,1))
        decs.append(dec + uniform(-1,1))
    return ras, decs


def main():
    parser = skysim_parser()
    parser.add_argument('--version', action='version', version=f'%(prog)s {mymodule.__version__}')
    options = parser.parse_args()
    # configure logging
    loglevels = {'DEBUG':logging.DEBUG, 
                 'INFO':logging.INFO, 
                 'WARNING':logging.WARNING, 
                 'ERROR':logging.ERROR, 
                 'CRITICAL':logging.CRITICAL
                 }

    logging.basicConfig(
        format="%(name)s:%(levelname)s %(message)s",
        level=loglevels[options.logging])
    log = logging.getLogger("sky_sim")

    # if ra/dec are not supplied the use a default value
    if None in [options.ra, options.dec]:
        ra, dec = get_radec()
    else:
        ra = options.ra
        dec = options.dec
    
    ras, decs = make_stars(ra,dec)

def clip_to_radius(ra, dec, ras, decs):
    """
    Clip the ra/dec values to within 1 degree of the given ra/dec
    """
    output_ras = []
    output_decs = []
    for ra_i, dec_i in zip(ras, decs):
        if (ra_i - ra)**2 + (dec_i - dec)**2 < 1:
            output_ras.append(ra_i)
            output_decs.append(dec_i)
    return output_ras, output_decs


    # now write these to a csv file for use by my other program
    with open(options.out,'w') as f:
        print("id,ra,dec", file=f)
        for i in range(len(ras)):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)
    log.info(f"Wrote {options.out}")