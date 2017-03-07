from .models import get_y_value_fields
from .graph_themes import get_color
import numpy as np
import collections
from datetime import datetime, timedelta
from colour import Color
import json

def get_tag_graphs(tags, weeks):
	tag_graphs = {}
	red = Color('#f37736')
	purple = Color('#a64ca6')

	unique_tags = np.unique([x['tag'] for x in tags.values('tag')])

	## get all tag graphs
	for tag in unique_tags:

		x_val = [(x['date'].date() - datetime(1970,1,1).date()).total_seconds() * 1000 for x in tags.filter(tag=tag).order_by('date').values('date')]
		y_val = [x['value'] for x in tags.filter(tag=tag).order_by('date').values('value')]

		tag_graphs[tag] = map_to_graph(x_val, y_val)

	## get week graph with all 0s
	x_val = [((datetime.combine(x, datetime.min.time()) - datetime(1970,1,1)).total_seconds() + 86400) * 1000 for x in weeks.keys()]

	y_val = [0] * len(x_val)
	zero_weeks = map_to_graph(x_val, y_val)

	## define unique USER tags
	user_tags = [x for x in unique_tags if x != "injury" and x != "performance"]

	## get colors
	try:
		user_colors = list(red.range_to(purple, len(user_tags)))
	except:
		user_colors = []

	# get an object with sentiments
	data = {}

	# get sentiments graph
	data['user_tags'] = []

	for tag in user_tags:
		data['user_tags'].append({
				"values": tag_graphs[tag],
				"key": str(tag),
				"color": get_color(tag) if "sentiment" in tag else user_colors[user_tags.index(tag)].hex
			})

	# data['user_tags'].append({
	# 	"values": zero_weeks,
	# 	"key": "",
	# 	"color": "#FFFFFF"
	# 	})

	# get user tags graph
	data['performance_injury'] = []

	# http://stackoverflow.com/questions/642763/find-intersection-of-two-lists
	for tag in set.intersection({'injury', 'performance'}, unique_tags):
		print tag
		data['performance_injury'].append({
				"values": tag_graphs[tag],
				"key": str(tag),
				"color": get_color(tag)
			})

	# data['performance_injury'].append({
	# 	"values": zero_weeks,
	# 	"key": "",
	# 	"color": "#FFFFFF"
	# 	})

	return data

def add_week(weeks, key):

		weeks[key] = {}
		weeks[key]['count'] = 0
		weeks[key]['acute_distance'] = 0
		weeks[key]['chronic_distance'] = 0
		weeks[key]['acute_sRPE'] = 0
		weeks[key]['chronic_sRPE'] = 0

def get_week_graphs(activities):

	weeks = dict()
	all_weeks = [(x['start_time'] - timedelta(days=x['start_time'].weekday())).date() for x in activities.values('start_time')]

	for activity in activities:

		activity_week = (activity.start_time - timedelta(days=activity.start_time.weekday())).date()

		# add week if we need to
		if activity_week not in weeks.keys():

			# add new week
			add_week(weeks, activity_week)

			week_below = activity_week - timedelta(days=7)
			week_above = activity_week + timedelta(days=7)

			# add any weeks we need to below
			if min(weeks.keys()) < week_below:
				while week_below not in weeks.keys():
					add_week(weeks, week_below)
					week_below = week_below - timedelta(days=7)

			# add any weeks we need to above
			if max(weeks.keys()) > week_above: 
				while week_above not in weeks.keys():
					add_week(weeks, week_above)
					week_above = week_above + timedelta(days=7)

		# add activity data to the appropriate week
		if activity.tot_dist != None:
			weeks[activity_week]['acute_distance'] += activity.tot_dist

		if activity.RPE != None and activity.tot_time != None:
			weeks[activity_week]['acute_sRPE'] += activity.sRPE

		weeks[activity_week]['count'] += 1

	for week in weeks:

		count = 0
		for i in range(1, 5):
			past_week = week - timedelta(days=7*i)

			if past_week in weeks:
				count += 1
				weeks[week]['chronic_distance'] += weeks[past_week]['acute_distance']
				weeks[week]['chronic_sRPE'] += weeks[past_week]['acute_sRPE']

		if count > 0:
			weeks[week]['chronic_distance'] /= count
			weeks[week]['chronic_sRPE'] /= count


	## modified from: http://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
	ordered_weeks = collections.OrderedDict(sorted(weeks.items()))

	field_graphs = {}

	# always graph against the week
	x_val = [((datetime.combine(x, datetime.min.time()) - datetime(1970,1,1)).total_seconds() + 86400) * 1000 for x in ordered_weeks.keys()]

	# get a graphable representation of every colunm of weeks
	for field in ['acute_distance', 'chronic_distance', 'acute_sRPE', 'chronic_sRPE']:

		# get a list of the y_values
		y_val = [ordered_weeks[x][field] for x in ordered_weeks]

		field_graphs[field] = map_to_graph(x_val, y_val)


	# get an object with all the data we want to graph
	data = {
		"distance": [
			{
				"values": field_graphs["acute_distance"],
				"key": "Weekly Mileage",
				"color": get_color("acute_distance")
			},
			{
				"values": field_graphs["chronic_distance"],
				"key": "Mean Mileage (past month)",
				"color": get_color("chronic_distance")
			}
		],
		"sRPE": [
			{
				"values": field_graphs["acute_sRPE"],
				"key": "Weekly sRPE",
				"color": get_color("acute_sRPE")
			},
			{
				"values": field_graphs["chronic_sRPE"],
				"key": "Mean sRPE (past month)",
				"color": get_color("chronic_sRPE")
			}
		]
	}

	return (data, ordered_weeks)


def map_to_graph(x, y):
	values = []

	for i, j in zip(x, y):
		values.append({"x": i, "y": j})

	return values
