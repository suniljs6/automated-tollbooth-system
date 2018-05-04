# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class vehicle_fare(models.Model):
	vehicle = models.ForeignKey('vehicle',on_delete=models.CASCADE)
	types = models.ForeignKey('types',on_delete=models.CASCADE)
	fare = models.BigIntegerField(default=0)
	def __str__(self):
		return str(self.vehicle)

class types(models.Model):
	name = models.CharField(max_length=200,db_index=True,primary_key=True)
	def __str__(self):
		return self.name
	
class vehicle(models.Model):
	vehicle = models.CharField(max_length=200,db_index=True,primary_key=True)
	def __str__(self):
		return self.vehicle
	
class admin_user(models.Model):
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.name
	
class authority_user(models.Model):
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.name
	
class end_user(models.Model):
	name = models.CharField(max_length=200,primary_key=True)
	password = models.CharField(max_length=200)
	type_of_user = models.ForeignKey('types',on_delete=models.CASCADE)
	type_of_vehicle = models.ForeignKey('vehicle',on_delete=models.CASCADE)
	count = models.BigIntegerField(default=0)
	due = models.BigIntegerField(default=0)
	def __str__(self):
		return self.name

class tollbooth(models.Model):
	name = models.CharField(max_length=200,primary_key=True)
	lat = models.CharField(max_length=200)
	lon = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class user_info(models.Model):
	uid = models.ForeignKey('end_user',on_delete=models.CASCADE)
	tid = models.ForeignKey('tollbooth',on_delete=models.CASCADE)
	time_stamp = models.DateTimeField(auto_now=True,auto_now_add=False)
	def __str__(self):
		return str(self.time_stamp)
	
class user_log(models.Model):
	uid =  models.ForeignKey('end_user',on_delete=models.CASCADE)
	amount_paid = models.BigIntegerField(default=0)
	time_stamp = models.DateTimeField(auto_now=True,auto_now_add=False)
	def __str__(self):
		return str(self.id)
	
class tollbooth_info(models.Model):
	tid = models.ForeignKey('tollbooth',on_delete=models.CASCADE)
	bus_truck_count = models.BigIntegerField(default=0)
	four_wheeler_count = models.BigIntegerField(default=0)
	light_commercial_vehicle_count = models.BigIntegerField(default=0)
	multi_axle_vehicle_count = models.BigIntegerField(default=0)
	over_size_vehicle_count = models.BigIntegerField(default=0)
	dateof = models.DateField(auto_now=True,auto_now_add=False)
	income = models.BigIntegerField(default=0)
	def __str__(self):
		return str(self.id)
