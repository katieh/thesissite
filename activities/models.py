## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file defines models for my postgres db

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
import json

## ------------------------------------------------------------ ##
## A model which stores data from an uploaded activity.
## ------------------------------------------------------------ ##

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

	## summary fields for an activity
	file = models.FileField(default=None)
	name = models.CharField(max_length=100, default="Run", null=True)
	start_time = models.DateTimeField(default=timezone.now)
	num_records = models.PositiveIntegerField(default=None, null=True)
	tot_dist = models.FloatField(null=True)
	avg_speed = models.FloatField(null=True)
	avg_hr = models.PositiveIntegerField(null=True)
	avg_cadence = models.PositiveIntegerField(null=True)


	## these are the data fields we keep track of for each run
	timestamp = ArrayField(models.DateTimeField(null=True), null=True, default=None) # datetime field
	position_lat = ArrayField(models.IntegerField(null=True), null=True, default=None) # integer values
	position_long = ArrayField(models.IntegerField(null=True), null=True, default=None) # integer values
	distance = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
	altitude = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
	speed = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
	heart_rate = ArrayField(models.PositiveIntegerField(null=True), null=True, default=None) # positive integer value
	cadence = ArrayField(models.PositiveIntegerField(null=True), null=True, default=None) # positive integer value

	## return the names of the array fields in Activity Model 
	def get_array_fields(self):
		return ["timestamp", "position_lat", "position_long", "distance", "altitude", "speed", "heart_rate", "cadence"]

	## returns a graphable json object of the activity
	def get_graphable_json(self):

		## objects that will be graphable
		altitude = []
		speed = []
		heart_rate = []
		cadence = []

		for i in range(self.num_records):
			altitude.append({"x": self.distance[i], "y": self.altitude[i]})
			speed.append({"x": self.distance[i], "y": self.speed[i]})
			heart_rate.append({"x": self.distance[i], "y": self.heart_rate[i]})
			cadence.append({"x": self.distance[i], "y": self.cadence[i]})


		data = [
		{
		"values": altitude,
		"key": 'Altitude',
		"color": '#00aedb'
		},
		{
		"values": speed,
		"key": 'Speed',
		"color": '#00b159'
		},
		{
		"values": heart_rate,
		"key": 'Heart Rate',
		"color": '#d11141'
		},
		{
		"values": cadence,
		"key": 'Cadence',
		"color": '#f37735'
		}
		];

		return json.dumps(data)

	## TODO: something like this would be good
	# def __getitem__(self, arg):
		
	# 	## make sure we're getting a string
	# 	if not typ(arg) == str: raise ValueError("you can only index into Activity with a String!")

	# 	## return correct field
	# 	if arg == "file":
	# 		return self.file
	# 	elif arg == "timestamp":
	# 		return self.timestamp
	# 	elif arg == "position_lat":
	# 		return self.position_lat
	# 	elif arg == "position_long":
	# 		return self.position_long
	# 	elif arg == "distance":
	# 		return self.distance
	# 	elif arg == "altitude":
	# 		return self.altitude
	# 	elif arg == "speed":
	# 		return self.speed
	# 	elif arg == "heart_rate":
	# 		return self.heart_rate
	# 	elif arg == "cadence":
	# 		return self.cadence
	# 	else:
	# 		raise ValueError("Activity does not contain field {}".format(arg))


