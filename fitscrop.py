#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
from astropy import wcs
from astropy.io import fits
## or
#import pyfits as fits


def convert_coordinates_to_pix(coordinate_format, fits_header, (left, right, top, bottom)):
    if (coordinate_format == "pixel"):
        return (left, right, top, bottom)
    if (coordinate_format == "degree"):
        w = wcs.WCS(fits_header)
        boundaries = [[left, top], [right, bottom]]
        [[pix_left, pix_top], [pix_right, pix_bottom]] = w.wcs_world2pix([[left, top], [right, bottom]] , 1)
        return (pix_left, pix_right, pix_top, pix_bottom)
        

def fitscrop(fits_image, (left, right, top, bottom)):
    if (left < 0.0 or len(fits_image[0]) < right or top < 0.0 or len(fits_image[1]) < bottom):
        sys.stderr.write("Warning: image coordinates out of boundary. Returning empty FITS image.\n")
    return fits_image[int(bottom):int(top), int(left):int(right)]



if __name__ == '__main__':

    #input parameter parsing
    parser = argparse.ArgumentParser()
    coordinates = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("-i", "--inputfile", type=str, required=True, help="Path to a FITS file containing an image.")
    parser.add_argument("-o", "--outputfile", type=str, required=True, help="Path to a FITS file which will contain the cropped image.")
    parser.add_argument("-H", "--hdu", type=int, default=0, help="Number of the Header Data Unit containing the image within the input file. The first HDU has the number 0.")
    parser.add_argument("-c", "--coordinate_format", type=str, default="pixel", help="Format of the cropping coordinates (-l, -r, -t -b). One of {pixel, degree}.")
    coordinates.add_argument("-C", "--center", nargs=3, type=float, help="Cropping coordinates (RA in degree or x in pixel, DEC in degree or y in pixel, Radius in arcsec or pixel). Unit depending on the -c flag.")
    coordinates.add_argument("-B", "--boundary", nargs=4, type=float, help="Cropping boundary coordinates (Left, Right, Top, Bottom in degree or pixel. Unit depending on the -c flag.")

    
    args = parser.parse_args()    

    if ( args.boundary != None ):
        args_left = args.boundary[0]
        args_right = args.boundary[1]
        args_top = args.boundary[2]
        args_bottom = args.boundary[3]
    if ( args.center != None):
        radius_degrees = args.center[2] / 3600.0
        args_left = args.center[0] + radius_degrees
        args_right = args.center[0] - radius_degrees
        args_top = args.center[1] + radius_degrees
        args_bottom = args.center[1] - radius_degrees
            
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

                    pixel_coordinates = convert_coordinates_to_pix(args.coordinate_format, fits_header, (args_left, args_right, args_top, args_bottom))
                    ## do the cropping
                    f[args.hdu].data = fitscrop(fits_image, pixel_coordinates)
                    ## write to output file
                    try:
                        f.writeto(args.outputfile)
                    except:
                        sys.stderr.write("Error: cannot write to output file.\n")
                else:
                    sys.stderr.write("Error: image has wrong dimensions. (NAXIS = " + str(fits_header['naxis']) + ")\n")
            ## close input fits file
            f.close()
        except:
            sys.stderr.write("Error: cannot open input file.\n")
    
    

