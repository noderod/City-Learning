"""
BASICS

Final visualizing tool which shows and saves the final plots for each city.
"""


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
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


# Firehouses



#search = ZipcodeSearchEngine()



# Creates a new map per city
for Actual_city, CITY in CITIES.items():


    ####################
    # INSPECTIONS

    # Probability of passing an inspection
    ####################

    plt.figure(figsize = (10.7, 8)) # New figure for each new plot

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
    print(len(fitat_lat))

    del fitat_lat, fitat_lon
    gc.collect()

    shape = sf.Reader("NewNYzips/nyu_2451_34509.shp")
    #first feature of the shapefile
    feature = shape.shapeRecords()[42]
    first = feature.shape.__dict__['points'] # But remember (Latitude, Longitude)
    print(first) # (GeoJSON format)

    # Keep reading until error arises
    # Assume zipcodes are sorted -inf --> +inf
    # Check each zipcode against the CSV file with inspection information



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
