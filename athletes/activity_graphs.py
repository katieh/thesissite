import json
import numpy as np
from .models import Activity
from .graph_themes import get_color, get_label

def get_field_histograms(activity, user):

	bins = 5

	## get the fields from the database
	keys = ['avg_speed', 'avg_hr', 'avg_cadence', 'elevation_gained']
	data = {}

	for key in keys:
		colunm_values = [x[key] for x in Activity.objects.filter(user=user).values(key) if x[key] != None]

		## put col values into bins
		hist = np.histogram(colunm_values, bins = bins)

		## format bins so they can be graphed
		values = []
		for i in range(bins):
			values.append({"x": hist[1][i], 
				"y": hist[0][i]})

		## find percent to pad on graph
		pad = (max(hist[1]) - min(hist[1])) * 0.1

		## create dict entry for histogram
		if key.replace('avg_', '') + '-histogram' not in data.keys():
			data[key.replace('avg_', '') + '-histogram'] = {}

		## add graph information
		data[key.replace('avg_', '') + '-histogram']['graph'] = [{
			"values": values,
			"key": get_label(key) + " Histogram",
			"color": get_color(key),
		}];

		## add metadata information
		data[key.replace('avg_', '') + '-histogram']['metadata'] = {
			'xmin': min(hist[1]) - 2 * pad,
			'xmax': max(hist[1]) - pad,
			'ymin': 0,
			'ymax': max(hist[0]) + 1
		}

	## return the data
	return json.dumps(data)



## returns a graphable json object of the activity for all variables tracked
def get_field_graphs(activity):

	## objects that will be graphable
	altitude = []
	speed = []
	heart_rate = []
	cadence = []

	if activity.num_records != None:
		N = activity.num_records
	else:
		N = 0

	for i in range(N):
		if activity.altitude != None:
			altitude.append({"x": activity.distance[i], "y": activity.altitude[i]})
		if activity.speed != None:
			speed.append({"x": activity.distance[i], "y": activity.speed[i]})
		if activity.heart_rate != None:
			heart_rate.append({"x": activity.distance[i], "y": activity.heart_rate[i]})
		if activity.cadence != None:
			cadence.append({"x": activity.distance[i], "y": activity.cadence[i]})


	data = {
		"altitude-graph": [
			{
			"values": altitude,
			"key": 'Altitude',
			"color": get_color("altitude")
			}
		],

		"speed-graph": [
			{
			"values": speed,
			"key": 'Speed',
			"color": get_color("speed")
			}
		],

		"heartrate-graph": [
			{
			"values": heart_rate,
			"key": 'Heart Rate',
			"color": get_color("heartrate")
			}
		],

		"cadence-graph": [
			{
			"values": cadence,
			"key": 'Cadence',
			"color": get_color("cadence")
			}
		]
	}

	return json.dumps(data)