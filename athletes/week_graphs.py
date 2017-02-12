from .models import Weeks, get_y_value_fields
from .graph_themes import get_color
import collections


def get_week_graphs(weeks):


	## modified from: http://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
	ordered_weeks = collections.OrderedDict(sorted(weeks.items()))

	field_graphs = {}

	# always graph against the week
	x_val = [float(x) for x in ordered_weeks.keys()]

	# get a graphable representation of every colunm of weeks
	for field in get_y_value_fields():

		# get a list of the y_values
		y_val = [ordered_weeks[x][field] for x in ordered_weeks]

		field_graphs[field] = map_to_graph(x_val, y_val)


	# get an object with all the data we want to graph
	data = {
		"count": [
			{
				"values": field_graphs["count"],
				"key": "Runs per Week",
				"color": get_color("count")
			}
		],
		"distance": [
			{
				"values": field_graphs["total_distance"],
				"key": "Total Distance",
				"color": get_color("total_distance")
			}
		],
		"speed": [
			{
				"values": field_graphs["avg_avg_speed"],
				"key": "Average Speed",
				"color": get_color("avg_avg_speed")
			},
			{
				"values": field_graphs["max_speed"],
				"key": "Max Speed",
				"color": get_color("avg_max_speed")
			}
		],
		"hr": [
			{
				"values": field_graphs["avg_avg_hr"],
				"key": "Average Heart Rate",
				"color": get_color("avg_avg_hr")
			},
			{
				"values": field_graphs["max_hr"],
				"key": "Max Heart Rate",
				"color": get_color("max_hr")
			}
		],
		"cadence": [
			{
				"values": field_graphs["avg_avg_cadence"],
				"key": "Average Cadence",
				"color": get_color("avg_avg_cadence")
			},
			{
				"values": field_graphs["max_cadence"],
				"key": "Max Cadence",
				"color": get_color("max_cadence")
			}
		],
		"elevation": [
			{
				"values": field_graphs["avg_elevation_gained"],
				"key": "Average Elevation Gained",
				"color": get_color("avg_elevation_gained")
			},
			{
				"values": field_graphs["total_elevation_gained"],
				"key": "Total Elevation Gained",
				"color": get_color("max_total_elevation_gained")
			}
		]
	}

	return data

def map_to_graph(x, y):
	values = []

	for i, j in zip(x, y):
		values.append({"x": i, "y": j})

	return values
