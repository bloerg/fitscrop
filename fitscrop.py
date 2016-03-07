#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from astropy.io import fits
## or
#import pyfits as fits




if __name__ == '__main__':

    #input parameter parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile", type=str, required=True, help="Path to a FITS file containing an image.")
    parser.add_argument("-o", "--outputfile", type=str, required=True, help="Path to a FITS file which will contain the cropped image.")
    parser.add_argument("-H", "--hdu", type=int, default=0, help="Number of the Header Data Unit containing the image within the input file. The first HDU has the number 0.")
    parser.add_argument("-c", "--coordinate_format", type=str, default="pixel", help="Format of the cropping coordinates (-l, -r, -t -b). One of {pixel, degree}.")
    parser.add_argument("-l", "--left", type=float, required=True, help="Left boundary coordinate for cropping.")
    parser.add_argument("-r", "--right", type=float, required=True, help="Right boundary coordinate for cropping.")
    parser.add_argument("-t", "--top", type=float, required=True, help="Top boundary coordinate for cropping.")
    parser.add_argument("-b", "--bottom", type=float, required=True, help="Bottom boundary coordinate for cropping.")
    args = parser.parse_args()    

    ## Check for output directory existence
    if not os.path.exists(os.path.dirname(args.outputfile)):
        sys.stderr.write("Error: output directory does not exist. Please create.\n")
    else:
        try:
            ## open input fits file
            f = fits.open(args.inputfile)
            ## stop processing if hdu parameter is out of boundary
            if ( len(f) < args.hdu + 1 ):
                sys.stderr.write("Error: HDU Parameter out of boundary. Input FITS file has only " + str(len(f)) + " HDU(s).\n")
            else:
                ## read fits header
                fits_header = f[args.hdu].header
                ## check if image is two dimensional
                if (fits_header['naxis'] == 2):
                    ## read fits image
                    fits_image = f[args.hdu].data
                else:
                    sys.stderr.write("Error: image has wrong dimensions. (NAXIS = " + str(fits_header['naxis']) + ")\n")
                
            ## close input fits file
            f.close()
        except:
            sys.stderr.write("Error: cannot open input file.\n")
    
    

