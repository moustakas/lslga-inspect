from astropy.table import Table
import os
import sys
import wget
from PIL import Image, ImageDraw

catalog_path = 'data/LSLGA-v2.0.fits'
t = Table.read(catalog_path)

test_galaxy = None

# Obtain a test galaxy
for i, row in enumerate(t):
    catalog = 'NGC'
    if row['GALAXY'][0:len(catalog)] == catalog:
        test_galaxy = row
        break

if test_galaxy is not None:

    GALAXY = test_galaxy['GALAXY']

    RA = test_galaxy['RA']
    DEC = test_galaxy['DEC']

    PA = test_galaxy['PA']
    D25 = test_galaxy['D25'] # diameter in arcminutes
    BA = test_galaxy['BA']

    pix_scale = 0.5
    img_width = 400
    img_height = 400
    
    img_url = (
        "http://legacysurvey.org/viewer/jpeg-cutout"
        "?ra={:.4f}"
        "&dec={:.4f}"
        "&layer=decals-dr7"
        "&pixscale={}"
        "&width={:.0f}"
        "&height={:.0f}"
    ).format(RA, DEC, pix_scale, img_width, img_height)

    img_path = wget.download(img_url, 'tmp/{}.jpg'.format(GALAXY))

    img = Image.open(img_path)
    draw = ImageDraw.ImageDraw(img)

    draw.ellipse((150, 150, 250, 250), fill=None, outline=(0, 0, 255), width=2)

    img.save(img_path)

    img.show()
    
# pixscale: arcseconds/pixel
# default; 0.262 arcsec/pix

# http://legacysurvey.org/viewer/jpeg-cutout?ra=149.6670&dec=28.8776&pixscale=.5&layer=decals-dr7&width=100&height=100

# https://github.com/legacysurvey/decals-web/blob/master/map/views.py
# See get_tile, maybe (render_into_wcs, create_scaled_image)

# https://github.com/moustakas/legacyhalos/blob/master/py/legacyhalos/html.py
# See addbar, for adding a scale bar

# TODO: Examine the galaxy zoo system and how this will integrate...
# TODO: For the dependencies build:
    # put into /usr/share (default for astrometry.net, for example)
    # could also put other stuff into the conda environment (using --prefix=/path/to/dir, for example)
    # Just make a nice, clean conda environment, not located in the directory or anything...
    # Keep the checked out code separate from the libs
# NOTE: ipython