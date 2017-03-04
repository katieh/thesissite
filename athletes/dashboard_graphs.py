from .models import Weeks, get_y_value_fields
from .graph_themes import get_color
import numpy as np
import collections
import datetime
from colour import Color

def get_tag_graphs(tags):
	tag_graphs = {}
	red = Color('red')
	purple = Color('purple')

	unique_tags = np.unique([x['tag'] for x in tags.values('tag')])

	## make sentiment graph if we have any notes saved
	for tag in unique_tags:

		x_val = [(x['date'].replace(tzinfo=None) - datetime.datetime(1970,1,1)).total_seconds() * 1000 for x in tags.filter(tag=tag).values('date')]
		y_val = [x['value'] for x in tags.filter(tag=tag).values('value')]

		tag_graphs[tag] = map_to_graph(x_val, y_val)

	# get an object with sentiments
	data = {}

	# get sentiments graph
	data['sentiment'] = []

	for sentiment in [x for x in unique_tags if "sentiment_" in x]:
		data['sentiment'].append({
				"values": tag_graphs[sentiment],
				"key": str(sentiment),
				"color": get_color(sentiment)

			})

	# get user tags graph
	data['user_tags'] = []
	user_tags = [x for x in unique_tags if "sentiment_" not in x]

	try:
		user_colors = list(red.range_to(purple, len(user_tags)))
	except:
		user_colors = []

	for user_tag in user_tags:
		data['user_tags'].append({
				"values": tag_graphs[user_tag],
				"key": str(user_tag),
				"color": user_colors[user_tags.index(user_tag)].hex
			})

	return data


def get_week_graphs(weeks):

	weeks = {datetime.datetime.strptime(x, '%m/%d/%Y'):y for x,y in weeks.items()}

	## modified from: http://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
	ordered_weeks = collections.OrderedDict(sorted(weeks.items()))

	field_graphs = {}

	# always graph against the week
	x_val = [(x - datetime.datetime(1970,1,1)).total_seconds() * 1000 for x in ordered_weeks.keys()]

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
