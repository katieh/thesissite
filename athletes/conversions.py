def meters_to_miles(meters):
	return meters / 1609.34

def miles_to_meters(miles):
	return miles * 1609.34

def meters_to_feet(meters):
	return meters * 3.28084

def feet_to_meters(feet):
	return feet * 0.3048

def meters_per_sec_to_min_per_mile(ms):
	if ms == 0:
		return 60

	min_per_mile = 1 / meters_per_sec_to_miles_per_sec(ms)

	if min_per_mile > 60:
		return 60

	return min_per_mile

def meters_per_sec_to_miles_per_sec(ms):
	return ms * 0.000621371192 * 60
