## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file defines models for my postgres db

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta

## ------------------------------------------------------------ ##
## A model which stores data from an uploaded activity.
## ------------------------------------------------------------ ##

## user 			-- the key of the user who is allowed to access the file.
## file 			-- the name of the file
## start	 		-- the date / time of the start of the activity
## name				-- the name of the activity
## num_records 		-- the number of records in the run (length ArrayFields)
## timestamp		-- array of timestamps
## position_lat		-- array of latitude positions
## position_long	-- array of longitiude positions
## distance			-- array of total distance at each timepoint NOTE: can only store up to  ~621 miles per run
## altitude	        -- array of altitudes over the activity
## speed			-- array of speeds over the activity
## heart_rate 		-- array of heart rates over the activity
## cadence			-- array of cadences over the activity

## TODO: extract more data from the .fit files. The fitparse
## package is not very good. Might want to write your own.
## / modify it.

## TODO: put document in user folder...
## def user_directory_path(instance, filename):
## 		return 'user_{0}/{1}'.format(instance.user.id, filename)
## class MyModel(models.Model):
##    	upload = models.FileField(upload_to=user_directory_path)

class Activity(models.Model):

	## metadata on activity
	user = models.ForeignKey(User, default=None, null=True, blank=False)
	file = models.FileField(default=None)
	name = models.CharField(max_length=100, default="Run", null=True)

	## summary of activity
	start_time = models.DateTimeField(default=timezone.now)
	num_records = models.PositiveIntegerField(default=None, null=True)
	tot_dist = models.FloatField(null=True)
	avg_hr = models.PositiveIntegerField(null=True)
	avg_cadence = models.PositiveIntegerField(null=True)
	elevation_gained = models.PositiveIntegerField(null=True, default=None)
	max_speed = models.FloatField(null=True)
	max_hr = models.PositiveIntegerField(null=True)
	max_cadence = models.PositiveIntegerField(null=True)
	RPE = models.PositiveIntegerField(null=True)
	tot_time = models.PositiveIntegerField(null=True)

	## users comments
	comments = models.TextField(null=True, default=None)
	tags = models.TextField(null=True, default=None)

	## these are the data fields we keep track of for each run
	timestamp = ArrayField(models.DateTimeField(null=True), null=True, default=None) # datetime field
	position_lat = ArrayField(models.IntegerField(null=True), null=True, default=None) # integer values
	position_long = ArrayField(models.IntegerField(null=True), null=True, default=None) # integer values
	distance = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
	altitude = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
	speed = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
	heart_rate = ArrayField(models.PositiveIntegerField(null=True), null=True, default=None) # positive integer value
	cadence = ArrayField(models.PositiveIntegerField(null=True), null=True, default=None) # positive integer value


	class Meta:
		get_latest_by = 'start_time'

	@property
	def RPE_percent(self):
		return (self.RPE / 10.0) * 100

	@property
	def sRPE(self):
		try:
			return self.RPE * self.tot_time
		except:
			return None

	@property
	def avg_speed(self):
		try:
			return (self.tot_dist * 1609.34) / (self.tot_time * 60)
		except:
			return None

	def __str__(self):
		try:
			return self.user.first_name + " " + self.user.last_name + ", " + self.name
		except:
			return "---- ----, " + self.name

	## return the names of the array fields in Activity Model 
	def get_array_fields(self):
		return ["timestamp", "position_lat", "position_long", "distance", "altitude", "speed", "heart_rate", "cadence"]


	## allow us to index into this object.
	def __getitem__(self, arg):
		
		## make sure we're getting a string
		if not (type(arg) == str or type(arg) == unicode): raise ValueError("you can only index into Activity with a String!")

		## return correct field
		if arg == "user":
			return self.user
		elif arg == "file":
			return self.file
		elif arg == "name":
			return self.name
		elif arg == "start_time":
			return self.start_time
		elif arg == "tot_dist":
			return self.tot_dist
		elif arg == "avg_speed":
			return self.avg_speed
		elif arg == "max_speed":
			return self.max_speed
		elif arg == "avg_hr":
			return self.avg_hr
		elif arg == "max_hr":
			return self.max_hr
		elif arg == "avg_cadence":
			return self.avg_cadence
		elif arg == "max_cadence":
			return self.max_cadence
		elif arg == "elevation_gained":
			return self.elevation_gained
		elif arg == "timestamp":
			return self.timestamp
		elif arg == "position_lat":
			return self.position_lat
		elif arg == "position_long":
			return self.position_long
		elif arg == "distance":
			return self.distance
		elif arg == "altitude":
			return self.altitude
		elif arg == "speed":
			return self.speed
		elif arg == "heart_rate":
			return self.heart_rate
		elif arg == "cadence":
			return self.cadence
		else:
			raise ValueError("Activity does not contain field {}".format(arg))

## ------------------------------------------------------------ ##
## helper function returns the y_value_fields that we want to
## graph in the dashboard
## ------------------------------------------------------------ ##
def get_y_value_fields():

	return['count', 'total_distance', 'avg_avg_speed',
	'max_speed', 'avg_avg_hr', 'max_hr', 'avg_avg_cadence',
	'max_cadence', 'avg_elevation_gained', 'total_elevation_gained']



## ------------------------------------------------------------ ##
## A model which stores data about a user's tags
## ------------------------------------------------------------ ##
class Tag(models.Model):

	## who is the object for and on what run did they tag it?
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
	run = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)

	## information on the tag
	tag = models.CharField(max_length=100, blank=False) # what was the tag
	date = models.DateTimeField(blank=False) # date associated with tag
	value = models.FloatField(default=1) # numeric value associated with tag
	comments = models.TextField(null=True) # ONLY filled out for injury / performance tags

	def __str__(self):
		try:
			return self.user.first_name + " " + self.user.last_name + ", " + self.tag
		except:
			return "---- ----, " + self.tag

	class Meta:
		get_latest_by = 'date'


class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advanced = models.BooleanField(default=True)





















