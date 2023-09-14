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

# NSRC = 5000000

# def clip_to_radius():
#     pass
# # from wikipedia


# def get_radec():        
#     """
#     Generate the ra & dec coordinates of Andromeda
#     in decimal degrees. ra is the right ascension in the sky, and
#     dec is the declination.

#     Returns
#     -------
#     ra : float
#         The RA, in degrees, for Andromeda
#     dec : float
#         The DEC, in degrees for Andromeda
#     """
#     # from wikipedia
#     andromeda_ra = '00:42:44.3'
#     andromeda_dec = '41:16:09'

#     d, m, s = andromeda_dec.split(':')
#     dec = int(d)+int(m)/60+float(s)/3600

#     h, m, s = andromeda_ra.split(':')
#     ra = 15*(int(h)+int(m)/60+float(s)/3600)
#     ra = ra/cos(dec*pi/180)
#     return ra,dec


# def skysim_parser():
#     """
#     Configure the argparse for skysim

#     Returns
#     -------
#     parser : argparse.ArgumentParser
#         The parser for skysim.
#     """
#     parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-')
#     parser.add_argument('--ra', dest = 'ra', type=float, default=None,
#                         help="Central ra (degrees) for the simulation location")
#     parser.add_argument('--dec', dest = 'dec', type=float, default=None,
#                         help="Central dec (degrees) for the simulation location")
#     parser.add_argument('--out', dest='out', type=str, default='catalog.csv',
#                         help='destination for the output catalog')
#     parser.add_argument('--logging', type=str, default=logging.INFO,
#                         help='Logging level from (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
#     return parser



# def make_stars(ra, dec, nsrc=NSRC):
#     """
#     Generate NSRC stars within 1 degree of the given ra/dec

#     Parameters
#     ----------
#     ra,dec : float
#         The ra and dec in degrees for the central location.
#     nsrc : int
#         The number of star locations to generate
    
#     Returns
#     -------
#     ras, decs : list
#         A list of ra and dec coordinates.
#     """
#     ras = []
#     decs = []
#     for _ in range(nsrc):
#         ras.append(ra +uniform(-1,1))
#         decs.append(dec + uniform(-1,1))
#     return ras, decs


# def main():
#     parser = skysim_parser()
#     parser.add_argument('--version', action='version', version=f'%(prog)s {mymodule.__version__}')
#     options = parser.parse_args()
#     # configure logging
#     loglevels = {'DEBUG':logging.DEBUG, 
#                  'INFO':logging.INFO, 
#                  'WARNING':logging.WARNING, 
#                  'ERROR':logging.ERROR, 
#                  'CRITICAL':logging.CRITICAL
#                  }

#     logging.basicConfig(
#         format="%(name)s:%(levelname)s %(message)s",
#         level=loglevels[options.logging])
#     log = logging.getLogger("sky_sim")

#     # if ra/dec are not supplied the use a default value
#     if None in [options.ra, options.dec]:
#         ra, dec = get_radec()
#     else:
#         ra = options.ra
#         dec = options.dec
    
#     ras, decs = make_stars(ra,dec)

# def clip_to_radius(ra, dec, ras, decs):
#     """
#     Clip the ra/dec values to within 1 degree of the given ra/dec
#     """
#     output_ras = []
#     output_decs = []
#     for ra_i, dec_i in zip(ras, decs):
#         if (ra_i - ra)**2 + (dec_i - dec)**2 < 1:
#             output_ras.append(ra_i)
#             output_decs.append(dec_i)
#     return output_ras, output_decs


#     # now write these to a csv file for use by my other program
#     with open(options.out,'w') as f:
#         print("id,ra,dec", file=f)
#         for i in range(len(ras)):
#             print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)
#     log.info(f"Wrote {options.out}")

#! /usr/bin/env python
"""
Simulate a catalog of stars near to the Andromeda constellation
"""

import argparse
import math
import random

NSRC = 5_000_000


def get_radec():
    """
    Generate the ra/dec coordinates of Andromeda
    in decimal degrees.

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
    ra = ra/math.cos(dec*math.pi/180)
    return ra, dec


def crop_to_circle(ras, decs, ref_ra, ref_dec, radius):
    """
    Crop an input list of positions so that they lie within radius of
    a reference position

    Parameters
    ----------
    ras,decs : list(float)
        The ra and dec in degrees of the data points
    ref_ra, ref_dec: float
        The reference location
    radius: float
        The radius in degrees
    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates that pass our filter.
    """
    ra_out = []
    dec_out = []
    for i in range(len(ras)):
        if (ras[i]-ref_ra)**2 + (decs[i]-ref_dec)**2 < radius**2:
            ra_out.append(ras[i])
            dec_out.append(ras[i])
    return ra_out, dec_out


def make_positions(ra, dec, nsrc=NSRC):
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
        ras.append(ra + random.uniform(-1, 1))
        decs.append(dec + random.uniform(-1, 1))
    # apply our filter
    ras, decs = crop_to_circle(ras, decs, ra, dec, 1)
    return ras, decs


def skysim_parser():
    """
    Configure the argparse for skysim

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser for skysim.
    """
    parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-')
    parser.add_argument('--ra', dest='ra', type=float, default=None,
                        help="Central ra (degrees) for the simulation location")
    parser.add_argument('--dec', dest='dec', type=float, default=None,
                        help="Central dec (degrees) for the simulation location")
    parser.add_argument('--out', dest='out', type=str, default='catalog.csv',
                        help='destination for the output catalog')
    return parser

def main():
    parser = skysim_parser()
    options = parser.parse_args()
    # if ra/dec are not supplied the use a default value
    if None in [options.ra, options.dec]:
        ra, dec = get_radec()
    else:
        ra = options.ra
        dec = options.dec
    
    ras, decs = make_stars(ra,dec, NSRC)

    # Turn our list of floats into NumPy arrays
    ras = np.array(ras)
    decs = np.array(decs)
    # We stack the arrays together, and use savetxt with a comma delimiter
    np.savetxt(options.out, np.stack((ras, decs), axis = -1), delimiter=",")
    print(f"Wrote {options.out}")