
from colour import Color
from datetime import datetime

def graph_date(date):
	return (date.date() - datetime(1970,1,1).date()).total_seconds() * 1000 + 86400

def get_colors(count):
	## ---------- COLORS FOR GRAPH! ------------ ##
	red = Color('#f37736')
	purple = Color('#a64ca6')
	try:
		user_colors = list(red.range_to(purple, count))
	except:
		user_colors = []

	return user_colors

## NOTE: could turn this into a dict
## color pallet from:
## http://www.color-hex.com/color-palette/700
def get_color(key):
	if "acute_distance" in key:
		return "#00aedb"

	elif "distance_ratio" in key:
		return "#800080"

	elif "sRPE_ratio" in key:
		return "#4b3832"


	elif "chronic_distance" in key:
		return '#006883'

	elif "acute_sRPE" in key:
		return '#d11141'

	elif "chronic_sRPE" in key:
		return '#8a223c'

	elif "count" in key:
		return "#7f7f7f"

	elif "altitude" in key or "elevation" in key:
		if "max" in key:
			return '#006883'
		else:
			return '#00aedb'

	elif "speed" in key:
		if "max" in key:
			return '#006a35'
		else:
			return '#00b159'

	elif "heartrate" in key or "hr" in key or "heart_rate" in key:
		if "max" in key:
			return '#7d0a27'
		else:
			return '#d11141'

	elif "cadence" in key:
		if "max" in key:
			return '#aa5325'
		else:
			return '#f37735'

	elif "sentiment_" in key:
		if "pos" in key:
			return '#00b159'

		elif "neg" in key:
			return 	'#d11141'

		else:
			return '#00aedb'

	elif "performance" in key:
		return "#00b159"

	elif "injury" in key:
		return "#d11141"


	else:
		raise KeyError("Requesting key that does not have a set color")

def get_label(key):
	if "altitude" in key or "elevation" in key:
		return 'Altitude'

	elif "speed" in key:
		return 'Speed'

	elif "heartrate" in key or "hr" in key or "heart_rate" in key:
		return 'Heart Rate'

	elif "cadence" in key:
		return 'Cadence'

	else:
		raise KeyError("Requesting key that does not have a set label")