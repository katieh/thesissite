
## NOTE: could turn this into a dict
## color pallet from:
## http://www.color-hex.com/color-palette/700
def get_color(key):
	if "acute_distance" in key:
		return "#00aedb"

	elif "chronic_distance" in key:
		return '#006883'

	elif "acute_sRPM" in key:
		return '#d11141'

	elif "chronic_sRPM" in key:
		return '#7d0a27'

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

	elif "performance":
		return "#00b159"

	elif "injury":
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