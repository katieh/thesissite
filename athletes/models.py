## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file defines models for my postgres db

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils import timezone
from django.contrib.auth.models import User

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
	week = models.FloatField(default=None, null=True)
	num_records = models.PositiveIntegerField(default=None, null=True)
	tot_dist = models.FloatField(null=True)
	avg_speed = models.FloatField(null=True)
	avg_hr = models.PositiveIntegerField(null=True)
	avg_cadence = models.PositiveIntegerField(null=True)
	elevation_gained = models.PositiveIntegerField(null=True, default=None)
	max_speed = models.FloatField(null=True)
	max_hr = models.PositiveIntegerField(null=True)
	max_cadence = models.PositiveIntegerField(null=True)

	## users comments
	comments = models.TextField(null=True, default=None)

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
## A model which stores data about a user's weekly stats
## ------------------------------------------------------------ ##

class Weeks(models.Model):

	## who is the object for?
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
	weeks = JSONField(default=dict())

	def add_activity(self, activity):

		## add week(s) if we need to
		weeks_int = [int(float(x) * 100) for x in self.weeks.keys()]
		week_int = int(activity.week * 100)
		if not week_int in weeks_int:

			## check if this is the first week we're adding to weeks
			if len(weeks_int) == 0:
				i = week_int
				end = week_int + 1


			## check if we're adding a weeks earlier than we've seen
			elif min(weeks_int) > week_int:
				i = week_int
				end = min(weeks_int)

			elif max(weeks_int) < week_int:
				i = max(weeks_int) + 1
				end = week_int + 1

			print "i: {} end: {}".format(i, end)
			while (i < end):
				i_str = str(i)
				if int(i_str[len(i_str) - 2:len(i_str)]) == 53:
					print "bridging a year!: {}".format(i)
					i = (int(i_str[0:len(i_str) - 2]) + 1) * 100 + 1

				print "current loop: {}".format(i)
				self.weeks[unicode(i / 100.0)] = {}
				self.weeks[unicode(i / 100.0)]['count'] = 0
				self.weeks[unicode(i / 100.0)]['total_distance'] = 0
				self.weeks[unicode(i / 100.0)]['avg_avg_speed'] = 0
				self.weeks[unicode(i / 100.0)]['max_speed'] = 0
				self.weeks[unicode(i / 100.0)]['avg_avg_hr'] = 0
				self.weeks[unicode(i / 100.0)]['max_hr'] = 0
				self.weeks[unicode(i / 100.0)]['avg_avg_cadence'] = 0
				self.weeks[unicode(i / 100.0)]['max_cadence'] = 0
				self.weeks[unicode(i / 100.0)]['avg_elevation_gained'] = 0
				self.weeks[unicode(i / 100.0)]['total_elevation_gained'] = 0

				i += 1

		## add info to the week
		week_string = unicode(activity.week)
		print 'adding info to week: {}'.format(week_string)

		if activity.tot_dist != None:
			self.weeks[week_string]['total_distance'] += activity.tot_dist

		if activity.avg_speed != None:
			self.weeks[week_string]['avg_avg_speed'] = _update_average(self.weeks[week_string]['avg_avg_speed'],
				activity.avg_speed, self.weeks[week_string]['count'])

		if activity.max_speed != None and activity.max_speed > self.weeks[week_string]['max_speed']:
			self.weeks[week_string]['max_speed'] = activity.max_speed

		if activity.avg_hr != None:
			self.weeks[week_string]['avg_avg_hr'] = _update_average(self.weeks[week_string]['avg_avg_hr'],
				activity.avg_hr, self.weeks[week_string]['count'])

		if activity.max_hr != None and activity.max_hr > self.weeks[week_string]['max_hr']:
			self.weeks[week_string]['max_hr'] = activity.max_hr

		if activity.avg_cadence != None:
			self.weeks[week_string]['avg_avg_cadence'] = _update_average(self.weeks[week_string]['avg_avg_cadence'],
				activity.avg_cadence, self.weeks[week_string]['count'])

		if activity.max_cadence != None and activity.max_cadence > self.weeks[week_string]['max_cadence']:
			self.weeks[week_string]['max_cadence'] = activity.max_cadence

		if activity.elevation_gained != None:
			self.weeks[week_string]['avg_elevation_gained'] = _update_average(self.weeks[week_string]['avg_elevation_gained'],
				activity.elevation_gained, self.weeks[week_string]['count'])

			self.weeks[week_string]['total_elevation_gained'] += activity.elevation_gained


		self.weeks[week_string]['count'] += 1


def _update_average(old_avg, new_val, count):
	return (old_avg * count + new_val) / (count + 1)

# ## summary of activity
# 	start_time = models.DateTimeField(default=timezone.now)
# 	week = models.FloatField(default=None, null=True)
# 	num_records = models.PositiveIntegerField(default=None, null=True)
# 	tot_dist = models.FloatField(null=True)
# 	avg_speed = models.FloatField(null=True)
# 	avg_hr = models.PositiveIntegerField(null=True)
# 	avg_cadence = models.PositiveIntegerField(null=True)
# 	elevation_gained = models.PositiveIntegerField(null=True, default=None)
# 	max_speed = models.FloatField(null=True)
# 	max_hr = models.PositiveIntegerField(null=True)
# 	max_cadence = models.PositiveIntegerField(null=True)

# 	## users comments
# 	comments = models.TextField(null=True, default=None)

# 	## these are the data fields we keep track of for each run
# 	timestamp = ArrayField(models.DateTimeField(null=True), null=True, default=None) # datetime field
# 	position_lat = ArrayField(models.IntegerField(null=True), null=True, default=None) # integer values
# 	position_long = ArrayField(models.IntegerField(null=True), null=True, default=None) # integer values
# 	distance = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
# 	altitude = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
# 	speed = ArrayField(models.FloatField(null=True), null=True, default=None) # float field
# 	heart_rate = ArrayField(models.PositiveIntegerField(null=True), null=True, default=None) # positive integer value
# 	cadence = ArrayField(models.PositiveIntegerField(null=True), null=True, default=None) # positive integer value




	# ## number of runs in each week
	# count = JSONField(default=0, null=True)

	# ## distance
	# total_distance = JSONField(null=True, default=0)

	# ## speed
	# avg_avg_speed = JSONField(null=True, default=0)
	# avg_max_speed = JSONField(null=True, default=0)

	# ## hr
	# avg_avg_hr = JSONField(null=True, default=0)
	# avg_max_hr = JSONField(null=True, default=0)


	# ## cadence
	# avg_avg_cadence = JSONField(null=True, default=0)
	# avg_max_cadence = JSONField(null=True, default=0)

	# ## elevation
	# avg_elevation_gained = JSONField(null=True, default=0)
	# total_elevation_gained = JSONField(null=True, default=0)

	# ## allow us to index into object.
	# def __getitem__(self, arg):

	# 	## make sure we're getting a string
	# 	if not (type(arg) == str or type(arg) == unicode): raise ValueError("you can only index into Week with a String!")


	# 	if arg == "user":
	# 		return self.user
	# 	elif arg == "total_distance":
	# 		return self.total_distance
	# 	elif arg == "avg_avg_speed":
	# 		return self.avg_avg_speed
	# 	elif arg == "avg_max_speed":
	# 		return self.avg_max_speed
	# 	elif arg == "avg_avg_hr":
	# 		return self.avg_avg_hr
	# 	elif arg == "avg_max_hr":
	# 		return self.avg_max_hr
	# 	elif arg == "avg_avg_cadence":
	# 		return self.avg_avg_cadence
	# 	elif arg == "avg_max_cadence":
	# 		return self.avg_max_cadence
	# 	elif arg == "avg_elevation_gained":
	# 		return self.avg_elevation_gained
	# 	elif arg == "total_elevation_gained":
	# 		return self.total_elevation_gained
	# 	else:
	# 		raise ValueError("Weeks does not contain field {}.".format(arg))


	# ## allow us to set value item into object.
	# def __setitem__(self, arg, value):

	# 	## make sure we're getting a string
	# 	if not (type(arg) == str or type(arg) == unicode): raise ValueError("you can only index into Week with a String!")


	# 	if arg == "user":
	# 		self.user = value
	# 	elif arg == "total_distance":
	# 		self.total_distance = value
	# 	elif arg == "avg_avg_speed":
	# 		self.avg_avg_speed = value
	# 	elif arg == "avg_max_speed":
	# 		self.avg_max_speed = value
	# 	elif arg == "avg_avg_hr":
	# 		self.avg_avg_hr = value
	# 	elif arg == "avg_max_hr":
	# 		self.avg_max_hr = value
	# 	elif arg == "avg_avg_cadence":
	# 		self.avg_avg_cadence = value
	# 	elif arg == "avg_max_cadence":
	# 		self.avg_max_cadence = value
	# 	elif arg == "avg_elevation_gained":
	# 		self.avg_elevation_gained = value
	# 	elif arg == "total_elevation_gained":
	# 		self.total_elevation_gained = value
	# 	else:
	# 		raise ValueError("Weeks does not contain field {}.".format(arg))

# def get_avg_fields():
# 		return ["avg_avg_speed", "avg_max_speed",
# 		"avg_avg_hr", "avg_max_hr",
# 		"avg_avg_cadence", "avg_max_cadence",
# 		"avg_elevation_gained"]

def get_y_value_fields():

	return['count', 'total_distance', 'avg_avg_speed',
	'max_speed', 'avg_avg_hr', 'max_hr', 'avg_avg_cadence',
	'max_cadence', 'avg_elevation_gained', 'total_elevation_gained']



