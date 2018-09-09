"""
BASICS

Functions to be imported in further programs
"""


import datetime
import numpy as np


# As a ratio from jan. to jan. 
inflation_table = {2010:1.015, 2011:1.0296, 2012:1.0174, 2013:1.015, 2014:1.0076, 2015:1.0073, 2016:1.0207, 2017:1.0211}
years_ava = inflation_table.keys()
# Maximum date taken into account
latest_date = datetime.datetime(2018, 1, 1, 0, 0, 0)
earliest_date = datetime.datetime(2010, 1, 1, 0, 0, 0)


# Given a certain date, computes the price in January 2018 according to inflation
# datex (datetime)
# original_price (float)
def inflation_adjuster(dat, original_price):

	if dat > latest_date:
		return original_price
	# Computes the day difference
	if dat < earliest_date:
		return original_price*reduce(lambda x, y: x*y, [inflation_table[z] for z in inflation_table.keys()])

	final_price = original_price
	# Computes the number of days until the end of the year
	# Assumes that inflation is linear
	curyear = dat.year
	next_year_jan1 = datetime.datetime(curyear+1, 1, 1, 0, 0, 0)
	decimal_inflation = np.sign(inflation_table[curyear])*abs(inflation_table[curyear]-1)
	left_year_inflation_decimal =  (decimal_inflation/(next_year_jan1 - datetime.datetime(curyear, 1, 1, 0, 0, 0)).days)*(next_year_jan1 - dat).days
	left_year_inflation = np.sign(left_year_inflation_decimal)*(1 + abs(left_year_inflation_decimal))
	# Computes the inflation for the years left until 2018
	years_left = [w for w in years_ava if w >  curyear]
	final_price *= left_year_inflation
	for yy in years_left:
		final_price*= inflation_table[yy]

	return final_price
