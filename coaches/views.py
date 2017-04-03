from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from friendship.models import FriendshipRequest, Friend
from django.contrib.auth.models import User
from athletes.models import Activity, Tag, Preferences
from athletes.dashboard_graphs import get_week_graphs, get_tag_graphs
from collections import Counter
from .coaches_dashboard import get_athletes_graph
from colour import Color
from athletes.graph_themes import get_colors

import datetime
from datetime import timedelta

# modified from stack overflow but I don't have internet rn 
# so can't get the link.
def _is_coach(user):
	return not user.groups.filter(name='athlete').exists()

# function copied from 
# http://stackoverflow.com/questions/480214/
def _remove_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def _pending_requests(user):
	return FriendshipRequest.objects.filter(to_user_id=user.id).count()

# coaches home view
@login_required
@user_passes_test(_is_coach, login_url="/athletes/", redirect_field_name=None)
def index(request):

	## ---------- GET USER PREFERENCES --------- ##
	try:
		preferences = Preferences.objects.get(user=request.user)

	except:
		preferences = Preferences()
		preferences.user = request.user
		preferences.save()

	# get athelete graphs
	athlete_ids = [x['to_user_id'] for x in Friend.objects.filter(from_user_id=request.user.id).values('to_user_id')]
	activities = dict()
	tags = {'recent': [], 'new': []}

	## ---------- COLORS FOR GRAPH! ------------ ##
	user_colors = get_colors(len(athlete_ids))

	## ------- construct objects to pass in -------- ##

	for athlete_id in athlete_ids:
		user = User.objects.get(pk=athlete_id)
		user_name = user.first_name + " " + user.last_name

		# add to activity
		activities[user_name] = {}
		activities[user_name]["data"] = Activity.objects.filter(user_id=athlete_id)
		activities[user_name]["color"] = user_colors[athlete_ids.index(athlete_id)].hex

		# get all tags
		tags_qs = Tag.objects.filter(user_id=athlete_id, allow_access=True).order_by('-date').exclude(tag__in=["sentiment_neg", "sentiment_pos", "performance", "injury"])
		all_tags = _remove_duplicates([x.tag for x in tags_qs])

		# look at recent tags
		recent_tags = all_tags[0:min(len(all_tags), 4)]

		if len(recent_tags) > 0:
			tags['recent'].append({'color': user_colors[athlete_ids.index(athlete_id)], 'id': athlete_id, 'name':user_name,
		'tags': recent_tags})

		# see if there are any NEW tags this week
		last_week = datetime.datetime.now().date() - timedelta(days=datetime.datetime.now().weekday()) - timedelta(days=7)
		new_tags_qs = tags_qs.filter(date__gte=last_week)
		old_tags = [x.tag for x in tags_qs.filter(date__lt=last_week)]
		new_tags = [x for x in all_tags if x not in old_tags]

		if len(new_tags) > 0:
			tags['new'].append({'color': user_colors[athlete_ids.index(athlete_id)], 'id': athlete_id, 'name':user_name,
					'tags': new_tags})

	# get graph
	athletes_graph = get_athletes_graph(activities, preferences.advanced)

	return render(request, 'coaches/index.html', 
		{'nbar': 'home',
		'athletes_graph': athletes_graph,
		'tags': tags,
		'pending': _pending_requests(request.user),
		'preferences':preferences})

# coaches list view of athletes
@login_required
@user_passes_test(_is_coach, login_url="/athletes/", redirect_field_name=None)
def list(request):

	friend_ids = [x['to_user_id'] for x in Friend.objects.filter(from_user_id=request.user.id).values('to_user_id')]
	friends = User.objects.filter(pk__in=friend_ids)

	athlete_data = []

	for friend in friends:

		data = dict()
		data['id'] = friend.id

		try:
			tags = [x["tag"] for x in Tag.objects.filter(user=friend.id, allow_access=True).values("tag").order_by('-date') if (x["tag"] not in ["sentiment_neg", "sentiment_pos", "performance", "injury"])]
			unique_tags = _remove_duplicates(tags)
			tag_counts = Counter(tags)


			data['name'] = friend.first_name + " " + friend.last_name
			data['recent_tags'] = unique_tags[0:min(len(unique_tags), 4)]
			data['frequent_tags'] =  tag_counts.most_common(min(len(unique_tags), 4))
		except:
			pass

		try:
			data['injury'] = Tag.objects.filter(user=friend.id, tag="injury", allow_access=True).latest()
		except:
			pass

		try:
			data['performance'] = Tag.objects.filter(user=friend.id, tag="performance", allow_access=True).latest()
		except:
			pass

		athlete_data.append(data)

		# except:
		# 	athlete_data = None

		print athlete_data
		print data

	return render(request, 'coaches/list.html', {'athletes': athlete_data, 'nbar':'athletes',
		'pending': _pending_requests(request.user)})

@login_required
@user_passes_test(_is_coach, login_url="/athletes/", redirect_field_name=None)
def connections(request):

	friendship_requests = FriendshipRequest.objects.filter(to_user_id=request.user.id)

	request_data = []

	# get information about who made the request!
	for friendship_request in friendship_requests:

		user = User.objects.get(pk=friendship_request.from_user_id)

		request_data.append({'request_id': friendship_request.id,
			'first_name': user.first_name,
			'last_name': user.last_name})

	# get information on the current friendships
	friends = Friend.objects.filter(from_user_id=request.user.id)

	friend_data = []

	for friend in friends:

		user = User.objects.get(pk=friend.to_user_id)

		friend_data.append({'friend_id': user.id,
			'first_name': user.first_name,
			'last_name':user.last_name})


	return render(request, 'coaches/connections.html', 
		{'request_data': request_data,
		'friend_data': friend_data,
		'pending': _pending_requests(request.user)})

@login_required
@user_passes_test(_is_coach, login_url="/athletes/", redirect_field_name=None)
def details(request, pk):

	## -------- GET WEEKS FROM ACTIVITIES! ---------- ##
	athlete = User.objects.get(pk=pk)
	activities = Activity.objects.filter(user=pk)
	weeks_graphs, weeks = get_week_graphs(activities)

	try:
		current_activity = activities.latest()

	except:
		current_activity = None
	

	# -------- GET THE CURRENT WEEK! ---------- ##
	this_week = datetime.datetime.now().date() - timedelta(days=datetime.datetime.now().weekday())
	try:
		current_week = weeks[this_week]

	except KeyError:
		current_week = None

	## -------- GET USER TAGS ---------- ##
	tags = Tag.objects.filter(user=pk, allow_access=True)

	return render(request, 'coaches/details.html', 
		{'this_week': this_week,
		'current_week': current_week,
		'week_graphs': weeks_graphs,
		'tag_graphs': get_tag_graphs(tags, weeks_graphs['distance'][2], weeks_graphs['sRPE'][2]),
		'activity': current_activity,
		'athlete': athlete,
		'pending': _pending_requests(request.user)})




