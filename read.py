from astropy.table import Table
import numpy as np
import os
import sys

'''
# assert len(sys.argv) == 2
if len(sys.argv) != 2:
    print("Must pass path to LSLGA FITS file")
    exit(1)

catalog_path = sys.argv[1]
catalog_path = os.path.expanduser(catalog_path)
'''

catalog_path = 'data/LSLGA-v2.0.fits'
t = Table.read(catalog_path)

'''
print("Test 1")
for row in t:
    if float(row['PA']) >= 180 or float(row['PA'] <= 0):
        print("PA: {} GALAXY: {}".format(row['PA'], row['PA']))

print("Test 2")
for row in t:
    if float(row['PA']) > 180 or float(row['PA'] < 0):
        print("PA: {} GALAXY: {}".format(row['PA'], row['PA']))

exit()
'''

# Test with first several rows
# t = t[:40]

# indices_to_remove = []

ralo=228.36846888888888
rahi=228.40573111111112
declo=5.415868888888888
dechi=5.453131111111111

for i, row in enumerate(t, 0):

    RA = row['RA']
    DEC = row['DEC']

    if RA > ralo and RA < rahi and DEC > declo and DEC < dechi:
        print("GALAXY: {} PA: {}".format(row['GALAXY'], row['PA']))

'''

    # Remove galaxies not in DESI footprint
    if not row['IN_DESI']:
        indices_to_remove.append(i)

    # Remove galaxies with DEC above dr7 foorprint
    dec = row['DEC']
    if dec > 30 or dec < 0:
        indices_to_remove.append(i)

# Remove list duplicates and sort in reverse orderu
indices_to_remove = list(set(indices_to_remove))
indices_to_remove.sort(reverse = True)

# Run in reverse so indices not affected by removal
for i in indices_to_remove:
    t.remove_row(i)

# print(len(t))

# Generate URLs
for ra, dec in t['RA','DEC']:
    print("http://legacysurvey.org/viewer/jpeg-cutout?ra={:.4f}&dec={:.4f}&zoom=13&layer=decals-dr7".format(ra, dec))

url_list = [
    "http://legacysurvey.org/viewer/jpeg-cutout?ra={:.4f}&dec={:.4f}&zoom=13&layer=decals-dr7".format(ra, dec)
    for ra, dec in t['RA', 'DEC']
]

# for line in $(python3 read.py); do wget $line; done
'''