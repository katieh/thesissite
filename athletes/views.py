## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file contains methods which render views
from django.contrib.auth.models import User, Group
from friendship.models import FriendshipRequest, Friend
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import FormView
from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models.base import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.forms import formset_factory
from django.contrib import messages


import numpy as np
import datetime
from datetime import timedelta

from .tags import get_user_tags, get_sentiment_tags
from .models import Activity, Tag, Preferences
from .forms import UploadActivitiesForm, ActivityForm, InjuryForm, PerformanceForm, UploadActivityForm, TagForm
from .activity_graphs import get_field_graphs, get_field_histograms
from .dashboard_graphs import get_week_graphs, get_tag_graphs
from .fitparse import Activity as FitActivity
from activity_helper_methods import get_dict_of_fields
import json

# modified from stack overflow but I don't have internet rn 
# so can't get the link.
def _is_athlete(user):
	return user.groups.filter(name='athlete').exists()


# main view
@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def index(request):

	## ---------- GET USER PREFERENCES --------- ##
	try:
		preferences = Preferences.objects.get(user=request.user)

	except:
		preferences = Preferences()
		preferences.user = request.user
		preferences.save()

	## -------- GET WEEKS FROM ACTIVITIES! ---------- ##
	activities = Activity.objects.filter(user=request.user)
	weeks_graphs, weeks = get_week_graphs(activities, preferences.advanced)

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
	tags = Tag.objects.filter(user=request.user)
	try:
		tags_graph = get_tag_graphs(tags, distance_ratio = weeks_graphs['distance'][2], sRPE_ratio = weeks_graphs['sRPE'][2])
	except:
		tags_graph = get_tag_graphs(tags)

	return render(request, 'athletes/index.html', 
		{'nbar': 'home',
		'preferences': preferences, 
		'this_week': this_week,
		'current_week': current_week,
		'week_graphs': weeks_graphs,
		'tag_graphs': tags_graph,
		'activity': current_activity})

# main view for athletes
@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def list(request):

	# get all the activities for the user
	activities = Activity.objects.filter(user=request.user).order_by('-start_time')

	return render(request, 'athletes/list.html', {'activities': activities, 'nbar': 'activities'})


# details view for an activity
@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def details(request, pk):

	# get the matching activity IF the user has permission!
	activity = get_object_or_404(Activity, user=request.user, pk=pk)

	return render(request, 'athletes/details.html', 
		{'pk': pk,
		'activity': activity,
		'field_graphs': get_field_graphs(activity),
		'field_histograms': get_field_histograms(activity, request.user)})

# allows you to edit an activity's name and comments
@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def edit(request, pk=None):

	# get the matching activity IF the user has permission!
	if pk!=None:
		activity = get_object_or_404(Activity, user=request.user, pk=pk)

	else:
		activity = Activity()
		activity.user_id = request.user.id

	if request.method == "POST":
		form = ActivityForm(request.POST, instance=activity)
		print "this one"
		print form['tot_dist'].errors
		print "that one"
		if form.is_valid():

			activity = form.save()

			# delete any tags formerly associated with this activity
			Tag.objects.filter(run_id=activity).delete()

			# NOTE: NOT DOING THIS ANYMORE
			# ## get sentiment of comment
			# get_sentiment_tags(activity)

			## find tags in the new comment
			get_user_tags(activity)

			return redirect('athletes:details', pk=activity.pk)

	else:
		form = ActivityForm(instance=activity)

	return render(request, 'athletes/edit.html', {'form': form})

## TODO: allow athlete to remove the connection!
@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def connections(request):

	coaches = User.objects.filter(groups__name='coach')
	pending_requests = [x.to_user_id for x in FriendshipRequest.objects.filter(from_user_id=request.user.id)]
	friends = [x.to_user_id for x in Friend.objects.filter(from_user_id=request.user.id)]

	friend_data = []
	for friend in friends:

		user = User.objects.get(pk=friend)

		friend_data.append({'friend_id': user.id,
			'first_name': user.first_name,
			'last_name':user.last_name})

	return render(request, 'athletes/connections.html', 
		{'coaches': coaches, 
		'pending_requests': pending_requests,
		'friends': friends,
		'friend_data': friend_data})

# TODO: something weird is happening with my elevation gained function... not sure what but it does NOT match up with garmins
# modified from example at https://github.com/Chive/django-multiupload
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None), name='dispatch')
class UploadView(FormView):
	template_name = 'athletes/upload.html'
	form_class = UploadActivitiesForm
	success_url = '/athletes/list/' # not sure about this

	def form_valid(self, form):
		for each in form.cleaned_data['attachments']:

			## ----------------------------------------- ##
			## CREATE THE ACTIVITY IN THE DATABASE
			## ----------------------------------------- ##
			
			## create and save a new activity
			db_activity = Activity(file=each) ## get the uploaded file
			db_activity.save() ## save so that we save the file

			## open file and extract data
			activity_file = open("media/" + db_activity.file.name)
			fit_activity = FitActivity(activity_file)
			fit_activity.parse()
			activity_dict = get_dict_of_fields(fit_activity)

			# TODO: something like this would be GREAT
			## find the union of keys in dict and fields in the Activity model
			#fields = union(activity_dict.keys, db_activity.get_data_fields())
			# for field in fields:
			# 	db_activity[field] = activity_dict[field]

			## fill in the user of the uploaded activity!
			db_activity.user = self.request.user	

			## fill in data for db_activity and save again
			if 'timestamp' in activity_dict.keys():
				db_activity.timestamp = activity_dict['timestamp']

				## fill in summary stats
				db_activity.start_time = min(activity_dict['timestamp'])
				db_activity.num_records = len(activity_dict['timestamp'])
				db_activity.tot_time = int((max(activity_dict['timestamp']) - min(activity_dict['timestamp'])).total_seconds() / 60.0)

				## get iso calender
				## figure out which week the activity is in
				activity_isocalendar = db_activity.start_time.date().isocalendar()
				db_activity.week = activity_isocalendar[0] + activity_isocalendar[1] / 100.0

			if 'position_lat' in activity_dict.keys():
				db_activity.position_lat = activity_dict['position_lat']

			if 'position_long' in activity_dict.keys():
				db_activity.position_long = activity_dict['position_long']

			if 'distance' in activity_dict.keys():
				db_activity.distance = activity_dict['distance']
				db_activity.tot_dist = max(activity_dict['distance'])

			if 'altitude' in activity_dict.keys():
				db_activity.altitude = activity_dict['altitude']

				db_activity.elevation_gained = sum([abs(activity_dict['altitude'][i] - activity_dict['altitude'][i+1]) 
					for i in range(len(activity_dict['altitude']) - 1) 
					if activity_dict['altitude'][i] != None and activity_dict['altitude'][i+1] != None])

			if 'speed' in activity_dict.keys():
				db_activity.speed = activity_dict['speed']
				db_activity.max_speed = max(activity_dict['speed'])

			if 'heart_rate' in activity_dict.keys():
				db_activity.heart_rate = activity_dict['heart_rate']
				db_activity.avg_hr = int(np.nanmean([x for x in activity_dict['heart_rate'] if x != None]))
				db_activity.max_hr = max(activity_dict['heart_rate'])

			if 'cadence' in activity_dict.keys():
				db_activity.cadence = activity_dict['cadence']
				db_activity.avg_cadence = int(np.nanmean([x for x in activity_dict['cadence'] if x != None]))
				db_activity.max_cadence = max(activity_dict['cadence'])


			## save models!
			db_activity.save()

		return super(UploadView, self).form_valid(form)

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def upload_one(request):

	if request.method == 'POST':
		form = UploadActivityForm(request.POST, request.FILES)
		print form.is_valid()

		if form.is_valid():

			## create and save a new activity
			db_activity = Activity(file=request.FILES['docfile']) ## get the uploaded file
			db_activity.save() ## save so that we save the file

			## open file and extract data
			activity_file = open("media/" + db_activity.file.name)
			fit_activity = FitActivity(activity_file)
			fit_activity.parse()
			activity_dict = get_dict_of_fields(fit_activity)

			# TODO: something like this would be GREAT
			## find the union of keys in dict and fields in the Activity model
			#fields = union(activity_dict.keys, db_activity.get_data_fields())
			# for field in fields:
			# 	db_activity[field] = activity_dict[field]

			## fill in the user of the uploaded activity!
			db_activity.user = request.user	
			db_activity.RPE = request.POST['RPE']
			db_activity.name = request.POST['name']
			db_activity.comments = request.POST['comments']
			db_activity.tags = request.POST['tags']

			## save any # that were in the comments.

			# NOTE: I've STOPPED doing sentiment analysis!!!
			# ## get sentiment of comment
			# get_sentiment_tags(db_activity)

			## find tags in the new comment
			get_user_tags(db_activity)

			## fill in data for db_activity and save again
			if 'timestamp' in activity_dict.keys():
				db_activity.timestamp = activity_dict['timestamp']

				## fill in summary stats
				db_activity.start_time = min(activity_dict['timestamp'])
				db_activity.num_records = len(activity_dict['timestamp'])
				db_activity.tot_time = int((max(activity_dict['timestamp']) - min(activity_dict['timestamp'])).total_seconds() / 60.0)

				## get iso calender
				## figure out which week the activity is in
				activity_isocalendar = db_activity.start_time.date().isocalendar()
				db_activity.week = activity_isocalendar[0] + activity_isocalendar[1] / 100.0

			if 'position_lat' in activity_dict.keys():
				db_activity.position_lat = activity_dict['position_lat']

			if 'position_long' in activity_dict.keys():
				db_activity.position_long = activity_dict['position_long']

			if 'distance' in activity_dict.keys():
				db_activity.distance = activity_dict['distance']
				db_activity.tot_dist = max(activity_dict['distance'])

			if 'altitude' in activity_dict.keys():
				db_activity.altitude = activity_dict['altitude']

				db_activity.elevation_gained = sum([abs(activity_dict['altitude'][i] - activity_dict['altitude'][i+1]) 
					for i in range(len(activity_dict['altitude']) - 1) 
					if activity_dict['altitude'][i] != None and activity_dict['altitude'][i+1] != None])

			if 'speed' in activity_dict.keys():
				db_activity.speed = activity_dict['speed']
				db_activity.max_speed = max(activity_dict['speed'])

			if 'heart_rate' in activity_dict.keys():
				db_activity.heart_rate = activity_dict['heart_rate']
				db_activity.avg_hr = int(np.nanmean([x for x in activity_dict['heart_rate'] if x != None]))
				db_activity.max_hr = max(activity_dict['heart_rate'])

			if 'cadence' in activity_dict.keys():
				db_activity.cadence = activity_dict['cadence']
				db_activity.avg_cadence = int(np.nanmean([x for x in activity_dict['cadence'] if x != None]))
				db_activity.max_cadence = max(activity_dict['cadence'])

			## save models!
			db_activity.save()

			return redirect('athletes:details', pk=db_activity.pk)


	else:
		form = UploadActivityForm()

	return render(request, 'athletes/upload_one.html', {'form': form})

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def new_injury(request):

	tag = Tag()
	tag.tag = "injury"
	tag.value = 1
	tag.user_id = request.user.id

	if request.method == "POST":
		form = InjuryForm(request.POST, instance=tag)
		if form.is_valid():
			print "valid!"
			form.save()

			return redirect('athletes:injury')

		else:
			print "invalid"

	else:
		form = InjuryForm()

	return render(request, 'athletes/injury.html', {'form': form})

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def new_performance(request):

	tag = Tag()
	tag.tag = "performance"
	tag.user_id = request.user.id

	if request.method == "POST":
		form = PerformanceForm(request.POST, instance=tag)
		if form.is_valid():
			print "valid!"
			form.save()

			return redirect('athletes:performance')

		else:
			print "invalid"

	else:
		form = PerformanceForm()

	return render(request, 'athletes/performance.html', {'form': form})

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def delete_activity(request, pk):

	activity = get_object_or_404(Activity, user=request.user, pk=pk)

	# remove activity
	activity.delete()

	return redirect('athletes:index')

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def injury_list(request):

	injuries = Tag.objects.filter(user=request.user, tag="injury").order_by('-date')

	return render(request, 'athletes/injury_list.html', {'injuries': injuries, 'nbar': 'injury_list'})

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def performance_list(request):

	performances = Tag.objects.filter(user=request.user, tag="performance").order_by('-date')

	return render(request, 'athletes/performance_list.html', {'performances': performances, 'nbar': 'list'})

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def remove_tag(request, pk):

	tag = get_object_or_404(Tag, user=request.user, pk=pk)
	tag.delete()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def help(request):

	return render(request, "athletes/help.html")

@login_required
def toggle_advanced(request):

	preferences = Preferences.objects.get(user=request.user)
	preferences.advanced = not preferences.advanced
	preferences.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
@user_passes_test(_is_athlete, login_url="/coaches/", redirect_field_name=None)
def tag_access(request):

	## get unique tags
	tags = {x['tag']:x['allow_access'] for x in Tag.objects.filter(user=request.user).values('tag', 'allow_access')}
	print tags
	print len(tags)

	TagFormSet = formset_factory(TagForm, extra=len(tags))

	if request.method == 'POST':

		formset = TagFormSet(request.POST)

		if formset.is_valid():

			for form in formset:
				data = form.cleaned_data

				## get tags by tag name and user
				tags = Tag.objects.filter(user=request.user, tag=data['tag_name'])

				for tag in tags:
					tag.allow_access = data['allow_access']
					tag.save()


			messages.add_message(request, messages.INFO, 'Your preferences have been saved!')
			return redirect('athletes:tag_access')


	else:
		formset = TagFormSet()

	return render(request, 'athletes/tag_access.html', {'formset': formset, 'tags':tags})
