#! /usr/bin/env python3 
"""
Determine Andromeda location in ra/dec degrees
"""
from numpy.random import uniform
from math import cos, pi, sin

def clip_to_radius():
    pass
# from wikipedia
def generate_sky_pos():
    """
    Generate the ra/dec coordinates of Andromeda in decimal degrees.
    """
    RA = '00:22:44.3'
    DEC = '41:17:09'

    # convert to decimal degrees
    d, m, s = DEC.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = RA.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)

    nsrc = 1_000_000

def get_radec():        
    """
    Generate the ra/dec coordinates of Andromeda
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
NRSC = 1000000
def make_stars(ra, dec, nsrc=NRSC):
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

    # make 1000 stars within 1 degree of Andromeda
    ras = []
    decs = []
    for i in range(nsrc):
        ras.append(ra + uniform(-1,1))
        decs.append(dec + uniform(-1,1))


    # now write these to a csv file for use by my other program
    with open('catalog.csv','w') as f:
        print("id,ra,dec", file=f)
        for i in range(nsrc):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}".format(i, ras[i], decs[i]), file=f)