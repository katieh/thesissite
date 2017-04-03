from athletes.dashboard_graphs import get_week_graphs
from athletes.graph_themes import get_colors
from colour import Color
import json

def get_athletes_graph(activities, ratio):

	## ----------- GRAPH OBJECT ----------- ##
	data = dict()
	data["distance"] = []
	data["sRPE"] = []

	for athlete in activities:

		if len(activities[athlete]["data"]) > 0:
			week_graph, weeks = get_week_graphs(activities[athlete]["data"])

			if (ratio):
				distance_ratio = week_graph["distance"][2]
				sRPE_ratio = week_graph["sRPE"][2]
			else:
				distance_ratio = week_graph["distance"][1]
				sRPE_ratio = week_graph["sRPE"][1]


			# fix distance ratio graph
			distance_ratio["key"] = athlete
			distance_ratio["color"] = activities[athlete]["color"]

			# fix sRPE ratio graph
			sRPE_ratio["key"] = athlete
			sRPE_ratio["color"] = activities[athlete]["color"]

			data["distance"].append(distance_ratio)
			data["sRPE"].append(sRPE_ratio)


	return json.dumps(data)