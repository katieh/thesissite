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
	tags = forms.CharField(required=False)
	met_expectation = forms.CharField()

# http://stackoverflow.com/questions/27651577/
class NaturalDateField(forms.DateField):
	def to_python(self, value):

		if not value:
			return None
		try:
			parsed_date = Date(value, tz=timezone.get_current_timezone())
		except:
			return None
		return parsed_date.date

class ExpectationsForm(ModelForm):

	class Meta:
		model = Activity
		fields = ['met_expectation']


class ActivityForm(ModelForm):
	start_time = NaturalDateField()
	tags = forms.CharField(required=False)

	class Meta:
		model = Activity
		fields = ['name', 'comments', 'tags', 'RPE', 'tot_dist', 'start_time', 'tot_time', 'met_expectation']

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

class TagForm(forms.Form):

	tag_name = forms.CharField()
	allow_access = forms.BooleanField(required=False)