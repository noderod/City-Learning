"""
BASICS

Final visualizing tool which shows and saves the final plots for each city.
"""


from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as Frontier
import numpy as np
import gc
import shapefile as sf
from uszipcode import ZipcodeSearchEngine
import csv



# All cities are provided as a dictionary so that it is easy to add new one sin the future
CITIES = {

    'New York': {
        'Name': 'New York', 'State': 'NY', 'lolelon': -74.25, 'lolelat': 40.47, 'uprelon': -73.65,
        'uprelat': 40.89, 'latlat0':40.67, 'lonlon0': -74.21, 'shp_path': 'NewNYzips/nyu_2451_34509',
        'shp_nickname': 'nyzips', 'Firehouses_coords': 'NewNYzips/FDNY_Firehouse_Listing.csv'}

}


# Given an RGB value in base 256 (standard), returns it as a ratio (needed by matplotlib)
# regreblu (arr): Standard RGB form

def rat_RGB(regeblu):

    return tuple([lolol/256 for lolol in regeblu])


# Computes the linear interpolation between 2 arrays given a ratio
# st_arr, en_arr (arr): Starting and ending arrays representing vector quantities
# ratrat (float): Ratio

def linear_interpol(st_arr, en_arr, ratrat):

    return list(ratrat*(np.array(en_arr) - np.array(st_arr)) + np.array(st_arr))


# RGB colors
BLUE_rgb = [0, 0, 256]
RED_rgb = [256, 0, 0]
GREEN_rgb = [0, 256, 0]
WHITE_rgb = [256, 256, 256]
YELLOW = [241, 244, 66]


# Firehouses



#search = ZipcodeSearchEngine()



# Creates a new map per city
for Actual_city, CITY in CITIES.items():


    ####################
    # INSPECTIONS

    # Probability of passing an inspection
    ####################
    plt.figure(figsize=(10.5, 8))
    #plt.figure(figsize = (10.7, 8)) # New figure for each new plot

    print('Now processing: ', Actual_city)


    map = Basemap(llcrnrlon= CITY['lolelon'],llcrnrlat= CITY['lolelat'],urcrnrlon=CITY['uprelon'],urcrnrlat=CITY['uprelat'],
                 resolution='h', projection='tmerc', lat_0 = CITY['latlat0'], lon_0 = CITY['lonlon0'])
    map.drawmapboundary(fill_color='aqua')
    map.fillcontinents(color='linen',lake_color='aqua')
    map.drawcoastlines()
    map.drawrivers()
    GIS_zips = map.readshapefile(CITY['shp_path'], CITY['shp_nickname'])


    #######
    # Plots all the fire stations on the map
    fitat_lon = []
    fitat_lat = []


    with open(CITY['Firehouses_coords']) as FD_locs:

        reader_loc = csv.DictReader(FD_locs)
        for row in reader_loc:
            # Some rows may be empty, if that is the case, do not use those points
            try:
                fitat_lon.append(float(row['Longitude']))
                fitat_lat.append(float(row['Latitude']))

            except:
                pass

    xx,yy = map(fitat_lon, fitat_lat)
    map.plot(xx, yy, 'bd', markersize=6, label = 'FDNY Firehouses')

    del fitat_lat, fitat_lon
    gc.collect()

    shape = sf.Reader("NewNYzips/nyu_2451_34509.shp")
    # Let's try plotting a polygon

    thiscol = rat_RGB([0, 0, 256])

    # PROBABILITY OF PASSING INSPECTION

    # Finds the min, max probabilities to interpolate the rest between them
    Allprobs = []
    with open('NewNYzips/Probability_Inspections.csv') as prins:

        reader = csv.DictReader(prins)
        for arrow in reader:
            Allprobs.append(float(arrow['P(Passing)']))

        lowest_ins = min(Allprobs)
        upper_ins = max(Allprobs)

    del Allprobs
    print(lowest_ins, upper_ins)


    # Already anaRED zipcodes
    checked_zips = []
    # Reads the shapefiles one by one
    shape = sf.Reader("NewNYzips/nyu_2451_34509.shp")
    for one_zip in shape.shapeRecords():

        bbord = one_zip.shape.__dict__['points'] # Zipcode borders
        Border_zip = Frontier(bbord)

        # Program will assume no data unless it is provided
        gradgrad = 'darkgrey'


        with open('NewNYzips/Probability_Inspections.csv') as prins:

            reader = csv.DictReader(prins)
            for arrow in reader:

                this_zip = arrow['Postcode']
                zz_lon = float(arrow['Longitude'])
                zz_lat = float(arrow['Latitude'])

                if this_zip in checked_zips:
                    continue

                zip_center = Point(zz_lon, zz_lat)

                if Border_zip.contains(zip_center):

                    checked_zips.append(this_zip)
                    passin = float(arrow['P(Passing)'])
                    gradgrad = rat_RGB(linear_interpol(RED_rgb, BLUE_rgb, passin))

                    # No need to keep have found the zipcode
                    break

        # Plots the zipcode with color assigned
        Zip_coords = []
        for pairco in bbord:
            poxx, poyy = map(pairco[0], pairco[1])
            Zip_coords.append((poxx,poyy))

        polzip = Polygon(Zip_coords, facecolor = gradgrad, edgecolor = 'k', linewidth = 1)
        plt.gca().add_patch(polzip)


    # Saves the result
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.savefig(Actual_city.replace(' ', '_')+'___original', frameon = False, bbox_inches='tight')


    ##################
    # INCIDENTS

    # Probability of incidents (only fire/chemical/explosion related are considered)
    # per inhabitant
    ##################


    gc.collect()


plt.show()
