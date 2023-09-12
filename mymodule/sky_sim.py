#! /usr/bin/env python3 
"""
Determine Andromeda location in ra/dec degrees
"""
from random import uniform
from math import cos, pi, sin

def clip_to_radius():
    pass
# from wikipedia
def generate_sky_pos():
    RA = '00:22:44.3'
    DEC = '41:17:09'

    # convert to decimal degrees
    d, m, s = DEC.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = RA.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)

    nsrc = 1_000_000

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