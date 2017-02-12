## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file contains methods which render views

from django.views.generic.edit import FormView
from django.shortcuts import render, reverse, redirect, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
import numpy as np

from .models import Activity
from .forms import UploadActivitiesForm
from fitparse import Activity as FitActivity
from activity_helper_methods import get_dict_of_fields


# main view
def index(request):

	return render(request, 'activities/index.html', {'nbar': 'home'})

# main view for activities
def list(request):

	# get all the activities
	activities = Activity.objects.all()

	return render(request, 'activities/list.html', {'activities': activities, 'nbar': 'activities'})


# details view for an activity
def details(request, pk):

	# get the matching activity
    activity = get_object_or_404(Activity, pk=pk)

    return render(request, 'activities/details.html', 
    	{'pk': pk,
    	'activity': activity,
    	'speed': activity.get_variable_json("speed"), 
    	'heartrate': activity.get_variable_json("heart_rate"),
    	'altitude': activity.get_variable_json("altitude"),
    	'cadence': activity.get_variable_json("cadence")})

def edit(request, pk):

	return render(request, 'activities/edit.html')


# modified from example at https://github.com/Chive/django-multiupload
class UploadView(FormView):
    template_name = 'activities/upload.html'
    form_class = UploadActivitiesForm
    success_url = '/activities/list/' # not sure about this

    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            
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

			## fill in data for db_activity and save again
			db_activity.timestamp = activity_dict['timestamp']
			db_activity.position_lat = activity_dict['position_lat']
			db_activity.position_long = activity_dict['position_long']
			db_activity.distance = activity_dict['distance']
			db_activity.altitude = activity_dict['altitude']
			db_activity.speed = activity_dict['speed']
			db_activity.heart_rate = activity_dict['heart_rate']
			db_activity.cadence = activity_dict['cadence']

			## fill in summary stats
			db_activity.start_time = min(activity_dict['timestamp'])
			db_activity.num_records = len(activity_dict['timestamp'])
			db_activity.tot_dist = max(activity_dict['distance'])
			db_activity.avg_speed = np.nanmean([x for x in activity_dict['speed'] if x != None])
			db_activity.avg_hr = int(np.nanmean([x for x in activity_dict['heart_rate'] if x != None]))
			db_activity.avg_cadence = int(np.nanmean([x for x in activity_dict['cadence'] if x != None]))

			## save model
			db_activity.save()

        return super(UploadView, self).form_valid(form)




