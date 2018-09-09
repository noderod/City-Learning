"""
BASICS

Cleans the Seattle fleet data in an easier to deal format by assigning numbers to brands and car types.
Adjusts car prices for inflation to January 2018 prices.

"""

from base_functions import inflation_adjuster
import csv
import datetime
from functools import reduce
import json
import math
import numpy as np


# Returns a datetime object object from MM/DD/YYYY
# date_from_table (str)
def fleet_date(date_from_table):
	return datetime.datetime.strptime(date_from_table, "%m/%d/%Y")



# As a check, prints how many vehicle brands and types there are
vbrands = []
vtypes = []

fleet_data = csv.DictReader(open("seattle_sold_fleet.csv"))
for row in fleet_data:
	# Saves only the first 5 terms
	brand = row["MAKE"][:5]
	descri = row["DESCRIPTION"]

	if brand not in vbrands:
		vbrands.append(brand)
	if (descri not in vtypes) and ('PATROL' not in descri):
		vtypes.append(descri)


vbrands = sorted(vbrands)
a = 1
BRANDS = {}
for brad in vbrands:
	BRANDS[brad] = a
	a +=1 


# Vehicle types are reconverted to better approximate those used in NYC for the second data analysis
# Seattle: NY
NYC_type_transformation = {
	"FIRE PUMPER":"FIRE",
	"SEDAN":"4DSD",
	"PASSENGER VAN":"VAN",
	"VAN":"VAN",
	"TRUCK SERVICE BODY":"PICK",
	"TRACTOR":"TRAC",
	"TRAILER":"TRLR",
	"PICKUP": "PICK",
	"SUV":"SUBN",
	"MOTORCYCLE":"MCY",
	"SWEEPER":"RD/S",
	"TRUCK - CRANE":"TR/C",
	"UTILITY":"UTIL",
	"CEMENT MIXER":"CMIX",
	"DELIVERY":"DELV",
	"TRUCK - DUMP":"DUMP",
	"TRUCK - FLATBED":"FLAT",
	"BUS":"BUS",
	"TANK":"TANK"
}


# Saves brand information as a JSON
with open("vehicle_brands.json", 'w') as brand_file:
	json.dump(BRANDS, brand_file, indent = 2, sort_keys=True)

# Saves NYC Type into into JSON as well
NYTypes = {}
b = 1
for x in sorted(NYC_type_transformation.keys()):
	NYTypes[NYC_type_transformation[x]] = b
	b += 1

with open("vehicle_types.json", 'w') as vtype_file:
	json.dump(NYTypes, vtype_file, indent = 2, sort_keys=True)


# Simple types, sorted
simple_descrip = sorted(NYC_type_transformation.keys(), reverse=True)


# Saves the current data to another CSV file so that it is easier to process it in the future
# Price is approximated to the closest thousand dollars
with open("car_prices_numeric.csv", 'w') as cardat:
	fleet_data = csv.DictReader(open("seattle_sold_fleet.csv"))
	for row in fleet_data:

		bnum = BRANDS[row['MAKE'][:5]]
		descri = row["DESCRIPTION"]
		if not (any(sd in descri for sd in simple_descrip)):
			# Type is not interesting
			continue

		# Finds the closest description
		for desc in simple_descrip:
			if desc in descri:
				break

		car_price = inflation_adjuster(fleet_date(row["SALE_DATE"]), float(row["SALE_PRICE"]))/1000
		# Ignore prices higher than $20,000 because they are relatively few and will not impact the next analysis with parking
		if car_price > 20:
			continue
		# Years are taken logarithmically from 2018
		cardat.write("%d, %d, %d, %d\n"  % (2018-int(row["YEAR"]), bnum, NYTypes[NYC_type_transformation[desc]], int(round(car_price))))
