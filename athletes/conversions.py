def meters_to_miles(meters):
	try:
		return meters / 1609.34
	except:
		return None

def miles_to_meters(miles):
	try:
		return miles * 1609.34
	except:
		return None

def meters_to_feet(meters):
	try:
		return meters * 3.28084
	except:
		return None

def feet_to_meters(feet):
	try:
		return feet * 0.3048
	except:
		return None

def meters_per_sec_to_min_per_mile(ms):
	try:
		if ms == 0:
			return 60

		min_per_mile = 1 / meters_per_sec_to_miles_per_sec(ms)

		if min_per_mile > 60:
			return 60

		return min_per_mile
	except:
		return None

def meters_per_sec_to_miles_per_sec(ms):
	try:
		return ms * 0.000621371192 * 60
	except:
		return None