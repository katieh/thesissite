## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file defines some template_filter functions
##				to be used in the HTML file
from django import template
import numpy as np

## get template library
register = template.Library()

## ------------------------------------------------------------ ##
## input:	distance in meters,
## output:	distance in miles
## ------------------------------------------------------------ ##
@register.filter
def meters_to_miles(distance):

	try:
		return "%.2f" % (float(distance) * 0.000621371192)

	except:
		print "meters to miles didn't receive a float"
		return distance



## ------------------------------------------------------------ ##
## input:	speed in meters per second
## output:	pace in minutes per mile
## ------------------------------------------------------------ ##
@register.filter
def mps_to_time_per_mile(mps):
	
	try:
		miles_per_minute = float(mps) * 0.000621371192 * 60
		minutes_per_mile = 1 / miles_per_minute
		return "%d:%02d" % (int(minutes_per_mile), np.round((minutes_per_mile - int(minutes_per_mile)) * 60))

	except:
		print "mps to time per mile did not receive a float"
		return mps