## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file defines the objects that uploaded files will be assigned to

## file modified from example at:
## https://github.com/Chive/django-multiupload/blob/master/examples/simple/forms.py

from django import forms
from multiupload.fields import MultiFileField
from django.forms import ModelForm
from .models import Activity, Tag

from django.utils import timezone
from timestring import Date

class UploadActivitiesForm(forms.Form):
	attachments = MultiFileField(min_num=1, max_num=100, max_file_size=1024*1024*5)

class UploadActivityForm(forms.Form):

	docfile = forms.FileField()
	name = forms.CharField()
	comments = forms.CharField()
	RPE = forms.IntegerField()

# http://stackoverflow.com/questions/27651577/
class NaturalDateField(forms.DateField):
	def to_python(self, value):

		print "look at this"
		print value

		if not value:
			return None
		parsed_date = Date(value, tz=timezone.get_current_timezone())
		return parsed_date.date

class ActivityForm(ModelForm):
	start_time = NaturalDateField()

	class Meta:
		model = Activity
		fields = ['name', 'comments', 'RPE', 'tot_dist', 'start_time', 'tot_time']

class InjuryForm(ModelForm):
	date = NaturalDateField()

	class Meta:
		model = Tag
		fields = ['date', 'comments']

class PerformanceForm(ModelForm):
	date = NaturalDateField()

	class Meta:
		model = Tag
		fields = ['date', 'value', 'comments']