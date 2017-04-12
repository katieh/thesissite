from .models import get_y_value_fields
from .graph_themes import get_color, graph_date
import numpy as np
import collections
from datetime import datetime, timedelta
from colour import Color
import json
import copy


## FIX THIS!
def _get_date_range(min_date, max_date):
	SECONDS_PER_DAY = 86400
	dates = []
	i = 0

	while (min_date +  SECONDS_PER_DAY * i * 1000 <= max_date):
		dates.append(min_date + SECONDS_PER_DAY * i * 1000)
		i += 1

	return dates



def get_tag_graphs(tags, distance_ratio=None, sRPE_ratio=None):
	tag_graphs = {}
	red = Color('#f37736')
	purple = Color('#a64ca6')

	unique_tags = np.unique([x['tag'] for x in tags.values('tag')])

	# print distance_ratio
	# print sRPE_ratio
	# if distance_ratio != None and sRPE_ratio != None:
	# 	distance_ratio_dict = {x['x']:x['y'] for x in distance_ratio['values']}
	# 	sRPE_ratio_dict = {x['x']:x['y'] for x in sRPE_ratio['values']}
	# else:
	# 	distance_ratio_dict = None
	# print "DISTANCE AND SRPE"
	# print distance_ratio_dict
	# print sRPE_ratio_dict

	try:
		#weeks_dates = distance_ratio.keys()
		weeks_dates = [x['x'] for x in distance_ratio['values']]
	except:
		weeks_dates = None

	## get dates for user tags
	ut_dates = [graph_date(x['date']) for x in tags.exclude(tag__in=['performance', 'injury']).values('date')]
	try:
		ut_dates = _get_date_range(min(ut_dates), max(ut_dates))
	except:
		pass
	if weeks_dates != None:
		try:
			min_val = min(min(weeks_dates), min(ut_dates))
			max_val = max(max(weeks_dates), max(ut_dates))
			ut_dates = _get_date_range(min_val, max_val)
		except:
			pass

	## get dates for performance and injury
	pi_dates = [graph_date(x['date']) for x in tags.filter(tag__in=['performance', 'injury']).values('date')]
	try:
		pi_dates = _get_date_range(min(pi_dates), max(pi_dates))
	except:
		pass
	if weeks_dates != None:
		try:
			min_val = min(min(weeks_dates), min(pi_dates))
			max_val = max(max(weeks_dates), max(pi_dates))
			pi_dates = _get_date_range(min_val, max_val)
		except:
			pass

	## get all tag graphs
	for tag in unique_tags:

		if tag in ["performance", 'injury']:
			tag_data = {x:0 for x in pi_dates}

		else:
			tag_data = {x:0 for x in ut_dates}

		for tag_instance in tags.filter(tag=tag).order_by('date').values('date', 'value'):
			tag_data[graph_date(tag_instance['date'])] = tag_instance['value']

		sorted_tag_data = collections.OrderedDict(sorted(tag_data.items()))
		x_val = sorted_tag_data.keys()
		y_val = list(sorted_tag_data.values())

		tag_graphs[tag] = map_to_graph(x_val, y_val)


	## define unique USER tags
	user_tags = [x for x in unique_tags if x != "injury" and x != "performance"]

	## get colors
	try:
		user_colors = list(red.range_to(purple, len(user_tags)))
	except:
		user_colors = []

	# get an object with sentiments
	data = {}
	data["y_max"] = {}

	# get sentiments graph
	data['user_tags'] = []

	for tag in user_tags:
		data['user_tags'].append({
				"values": tag_graphs[tag],
				"key": str(tag),
				"color": get_color(tag) if "sentiment" in tag else user_colors[user_tags.index(tag)].hex,
				#"type": "bar",
				"type": 'line',
				"yAxis": 1,
				'area': 'true'
			})

	# # append distance and sRPE ratios for USER TAGS
	# if distance_ratio != None:

	# 	ut_distance_ratio = distance_ratio.copy()

	# 	smaller_dates = [x < y for x in ut_distance_ratio.keys() for y in ut_dates]
	# 	for smaller_date in smaller_dates:
	# 		ut_distance_ratio[smaller_date] = None

	# 	larger_dates = [x > y for x in ut_distance_ratio.keys() for y in ut_dates]
	# 	for larger_date in larger_dates:
	# 		ut_distance_ratio[larger_date] = None

	# 	data['user_tags'].append(map_to_graph(ut_distance_ratio.keys(), list(ut_distance_ratio.values())))

	# print "OVER HERE"
	# print sRPE_ratio
	# if sRPE_ratio != None:

	# 	ut_sRPE_ratio = sRPE_ratio.copy()

	# 	smaller_dates = [x < y for x in ut_sRPE_ratio.keys() for y in ut_dates]
	# 	for smaller_date in smaller_dates:
	# 		ut_sRPE_ratio[smaller_date] = None

	# 	larger_dates = [x > y for x in ut_sRPE_ratio.keys() for y in ut_dates]
	# 	for larger_date in larger_dates:
	# 		ut_sRPE_ratio[larger_date] = None

	# 	print "HERE"
	# 	print map_to_graph(ut_sRPE_ratio.keys(), list(ut_sRPE_ratio.values()))

	# 	data['user_tags'].append({
	# 			"values": map_to_graph(ut_sRPE_ratio.keys(), list(ut_sRPE_ratio.values())),
	# 			"key": str("Acute:Chronic sRPE"),
	# 			"color": get_color("Acute:Chronic sRPE"),
	# 			#"type": "bar",
	# 			"type": 'line',
	# 			"yAxis": 2,
	# 	})

	if distance_ratio:
		try:
			# add extra data point to distance if we need to
			if max(weeks_dates) < max(ut_dates):
				ut_distance_ratio = copy.deepcopy(distance_ratio)
				ut_distance_ratio['values'].append({'x': max(ut_dates), 'y':ut_distance_ratio['values'][len(ut_distance_ratio['values']) - 1]['y']})
				data['user_tags'].append(ut_distance_ratio)
			else:
				data['user_tags'].append(distance_ratio)
		except:
			pass
	if sRPE_ratio:
		try:
			# add extra data point to distance if we need to
			if max(weeks_dates) < max(ut_dates):
				ut_sRPE_ratio = copy.deepcopy(sRPE_ratio)
				ut_sRPE_ratio['values'].append({'x': max(ut_dates), 'y':ut_sRPE_ratio['values'][len(ut_sRPE_ratio['values']) - 1]['y']})
				data['user_tags'].append(ut_sRPE_ratio)
			else:
				data['user_tags'].append(sRPE_ratio)
		except:
			pass

	# get the max_y value for 'user_tags'
	try:
		data["y_max"]['user_tags'] = max([x["y"] for tag in user_tags for x in tag_graphs[tag]])
	except:
		data["y_max"]['user_tags'] = 0

	# data['user_tags'].append({
	# 	"values": zero_weeks,
	# 	"key": "",
	# 	"color": "#FFFFFF"
	# 	})

	# get user tags graph
	data['performance_injury'] = []

	# http://stackoverflow.com/questions/642763/find-intersection-of-two-lists
	for tag in set.intersection({'injury', 'performance'}, unique_tags):
		data['performance_injury'].append({
				"values": tag_graphs[tag],
				"key": str(tag),
				"color": get_color(tag),
				#"type": "bar",
				"type": 'line',
				"yAxis": 1, 
				'area': 'true'
			})

	if distance_ratio:
		# add extra data point to distance if we need to
		try:
			if max(weeks_dates) < max(pi_dates):
				pi_distance_ratio = copy.deepcopy(distance_ratio)
				pi_distance_ratio['values'].append({'x': max(pi_dates), 'y':pi_distance_ratio['values'][len(pi_distance_ratio['values']) - 1]['y']})
				data['performance_injury'].append(pi_distance_ratio)
			else:
				data['performance_injury'].append(distance_ratio)
		except:
			pass
		
	if sRPE_ratio:
		try:
			# add extra data point to distance if we need to
			if max(weeks_dates) < max(pi_dates):
				pi_sRPE_ratio = copy.deepcopy(sRPE_ratio)
				pi_sRPE_ratio['values'].append({'x': max(pi_dates), 'y':pi_sRPE_ratio['values'][len(pi_sRPE_ratio['values']) - 1]['y']})
				data['performance_injury'].append(pi_sRPE_ratio)
			else:
				data['performance_injury'].append(sRPE_ratio)
		except:
			pass

	try:
		data["y_max"]['performance_injury'] = max([x["y"] for tag in set.intersection({'injury', 'performance'}, unique_tags) for x in tag_graphs[tag]])

	except:
		data["y_max"]['performance_injury'] = 0

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

def get_week_graphs(activities, advanced=True):

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

	# get acute:chronic ratio for DISTANCE
	y_val = [float(ordered_weeks[x]["acute_distance"]) / ordered_weeks[x]["chronic_distance"] if ordered_weeks[x]["chronic_distance"] != 0 else 0 for x in ordered_weeks]
	y_val = [x if x <= 3 else 3 for x in y_val]
	field_graphs["distance_ratio"] = map_to_graph(x_val, y_val)

	# get acute:chronic ratio for sRPE
	y_val = [float(ordered_weeks[x]["acute_sRPE"]) / ordered_weeks[x]["chronic_sRPE"] if ordered_weeks[x]["chronic_sRPE"] != 0 else 0 for x in ordered_weeks]
	y_val = [x if x <= 3 else 3 for x in y_val]
	field_graphs["sRPE_ratio"] = map_to_graph(x_val, y_val)

	# get an object with all the data we want to graph
	data = {
		"distance": [
			{
				"values": field_graphs["acute_distance"],
				"key": "Weekly Mileage (Acute)",
				"color": get_color("acute_distance"),
				"type": "bar",
				"yAxis": 1
			}
		],
		"sRPE": [
			{
				"values": field_graphs["acute_sRPE"],
				"key": "Weekly sRPE (Acute)",
				"color": get_color("acute_sRPE"),
				"type": "bar",
				"yAxis": 1
			}
		]
	}

	if advanced:
		data['distance'] += [
			{
				"values": field_graphs["chronic_distance"],
				"key": "Chronic Mileage",
				"color": get_color("chronic_distance"),
				"type": "bar",
				"yAxis": 1
			},
			{
				"values": field_graphs["distance_ratio"],
				"key": "Acute:Chronic Mileage",
				"color": get_color("distance_ratio"),
				"type": "line",
				"yAxis": 2
			}
		]
		data['sRPE'] += [
			{
				"values": field_graphs["chronic_sRPE"],
				"key": "Chronic sRPE",
				"color": get_color("chronic_sRPE"),
				"type": "bar",
				"yAxis": 1
			},
			{
				"values": field_graphs["sRPE_ratio"],
				"key": "Acute:Chronic sRPE",
				"color":get_color("sRPE_ratio"),
				"type": "line",
				"yAxis": 2
			}
		]
			

	data["y_max"] = {}

	try:
		data["y_max"]["distance"] = max([x["y"] for tag in ["acute_distance", "chronic_distance"] for x in field_graphs[tag]])
		if not advanced:
			data["y_max"]["distance"] += 0.2*data["y_max"]["distance"]

	except:
		data["y_max"]["distance"] = 0

	try:
		data["y_max"]["sRPE"] = max([x["y"] for tag in ["acute_sRPE", "chronic_sRPE"] for x in field_graphs[tag]])
		if not advanced:
			data["y_max"]["sRPE"] += 0.2*data["y_max"]["sRPE"]

	except:
		data["y_max"]["sRPE"] = 0

	return (data, ordered_weeks)


def map_to_graph(x, y):
	values = []

	for i, j in zip(x, y):
		values.append({"x": i, "y": j})

	return values
