#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
from astropy.io import fits
## or
#import pyfits as fits




if __name__ == '__main__':

    #input parameter parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", type=str, required=True, help="Path to a FITS file containing an image.")
    parser.add_argument("-o", "--outputdir", type=str, required=True, help="Path to a FITS file which will contain the cropped image.")
    parser.add_argument("-H", "--hdu", type=int, default=0, help="Number of the Header Data Unit containing the image within the input file.")
    parser.add_argument("-c", "--coordinate_format", type=str, default="pixel", help="Format of the cropping coordinates (-l, -r, -t -b). One of {pixel, degree}.")
    parser.add_argument("-l", "--left", type=float, required=True, help="Left boundary coordinate for cropping.")
    parser.add_argument("-r", "--right", type=float, required=True, help="Right boundary coordinate for cropping.")
    parser.add_argument("-t", "--top", type=float, required=True, help="Top boundary coordinate for cropping.")
    parser.add_argument("-b", "--bottom", type=float, required=True, help="Bottom boundary coordinate for cropping.")
    args = parser.parse_args()    

    
    try:
        f = fits.open(args.inputfile)
    except:
        sys.stderr.write("Error: cannot open input file.\n")

    
    f.close()
