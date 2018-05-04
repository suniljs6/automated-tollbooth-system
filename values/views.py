# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
import  datetime
# Create your views here.

@csrf_exempt
def index(request):
	return HttpResponse("Hello,World")
	
def get_user(request,name):
	result = get_object_or_404(end_user,pk=name)
	return HttpResponse(result)
 
	
@csrf_exempt
def data(request):
	values = []
	if request.method == 'POST':
		values.append(json.loads(json.dumps({"name": json.loads((request.body).decode('utf-8')).get('name'),"tname": json.loads((request.body).decode('utf-8')).get('tname'),"vehicle": json.loads((request.body).decode('utf-8')).get('vehicle')})))
		r = values[-1]
		#store_from_rpi.objects.create(name=r['name'],tname=r['tname'],vehicle=r['vehicle'])
		s = end_user.objects.filter(name=r['name']).exists()
		if(s==True):
			user = end_user.objects.all().get(name=r['name'])
			toll = tollbooth.objects.all().get(name=r['tname'])
			v = vehicle.objects.all().get(vehicle=r['vehicle'])
			fares = v.vehicle_fare_set.get(types=user.type_of_user)
			user.due+=fares.fare
			user.user_info_set.create(tid=toll)
			user.count+=1
			user.save()
			t_info = toll.tollbooth_info_set.all()
			if(t_info):
				t = toll.tollbooth_info_set.latest("id")
				if(r['vehicle']=='four_wheeler'):
					t.four_wheeler_count+=1
				elif(r['vehicle']=='bus/truck'):
					t.bus_truck_count+=1
				elif(r['vehicle']=='light-commercial'):
					t.light_commercial_vehicle_count+=1
				elif(r['vehicle']=='multi-axle'):
					t.multi_axle_vehicle_count+=1
				elif(r['vehicle']=='over_size'):
					t.over_size_vehicle_count+=1
				t.income+=fares.fare
				t.save()
			else:
				if(r['vehicle']=='four_wheeler'):
					f = toll.tollbooth_info_set.create(four_wheeler_count=1,income=fares.fare)
				elif(r['vehicle']=='bus/truck'):
					f = toll.tollbooth_info_set.create(bus_truck_count=1,income=fares.fare)
				elif(r['vehicle']=='light-commercial'):
					f = toll.tollbooth_info_set.create(light_commercial_vehicle_count=1,income=fares.fare)
				elif(r['vehicle']=='multi-axle'):
					f = toll.tollbooth_info_set.create(multi_axle_vehicle_count=1,income=fares.fare)
				elif(r['vehicle']=='over_size'):
					f = toll.tollbooth_info_set.create(over_size_vehicle_count=1,income=fares.fare)
		print r['name'],r['tname'],r['vehicle']
		return HttpResponse(values)
	else:
		return JsonResponse(values,safe=False)
@csrf_exempt		
def login(request):
	return render(request,'values/page-login.html')
@csrf_exempt
def check_login(request):
	username = request.POST.get('username')
	p = request.POST.get('password')
	s = end_user.objects.filter(name=username,password=p).exists()
	if(s==True):
		print "True"
		user = end_user.objects.all().get(name=username)
		tov = user.type_of_vehicle
		tou = user.type_of_user
		count = user.count
		check = user.user_log_set.all()
		if(check):
			q = user.user_log_set.latest('id')
			time_stamp = q.time_stamp
			amount = user.user_log_set.all().aggregate(Sum('amount_paid'))
			if amount:
				money = amount['amount_paid__sum']
			else:
				#print "fruits"
				money = None 
			print money
		else:
			#print "pedda"
			time_stamp = None
			money = 0
		return render(request,'values/index.html',{'name':username,'time':time_stamp,'tov':tov,'tou':tou,'count':count,'amount':money})
	else:
		print "False"
		return render(request,'values/page-login.html')
def logout(request):
	return redirect('values/page-login.html')
		
@csrf_exempt	
def register(request):	
	return render(request,'values/page-register.html',{})
	
def add_register(request):
	username = request.POST.get('username')
	p = request.POST.get('password')
	tou = request.POST.get('tou')
	t_o_u = types.objects.get(name=tou)
	tov = request.POST.get('tov')
	t_o_v = vehicle.objects.get(vehicle=tov)
	end_user.objects.create(name=username,password=p,type_of_user=t_o_u,type_of_vehicle=t_o_v,count=0,due=0)
	s = end_user.objects.filter(name=username).exists()
	if(s==True):
		return render(request,'values/index.html')
	else:
		return render(request,'values/page-register.html',{})

		
def tollbooth_values(request,uid):
	data_values = []
	time = []
	check = end_user.objects.filter(name=uid).exists()
	if(check):
		user = end_user.objects.all().get(name = uid)
		#print user
		tid = user.user_info_set.all()
		for i in tid:
			t = tollbooth.objects.get(name=i.tid)
			#data_values.append(json.loads(json.dumps({"name": t.name,"lon":t.lon,"lat":t.lat,'time':str(i)})))
			data_values.append(t)
			time.append(i)
		return render(request,"values/tables-basic.html",{'data':data_values,'time':time})			
#		return render(request,"values/make.html",{"data":data_values,'time':time})			

		
'''def tollbooth_payments(request,pid):
	pay_values = []
	check = end_user.objects.filter(name=pid).exists()
	if(check):
		user = end_user.objects.all().get(name = pid)
		print user
		tid = user.user_log_set.all()
		print tid
		for i in tid:
			t = user_log.objects.get(id=i.id)
			pay_values.append(json.loads(json.dumps({"name":str(t.uid),"amount_paid":t.amount_paid,"time_stamp":str(t.time_stamp)})))
		return JsonResponse(pay_values,safe=False)			
	else:
		print "fruit"
		return JsonResponse(pay_values,safe=False)
'''


def give_toll(request,uid):
	data_values = []
	check = end_user.objects.filter(name=uid).exists()
	if(check):
		user = end_user.objects.all().get(name = uid)
		#print user
		tid = user.user_info_set.all()
		for i in tid:
			t = tollbooth.objects.get(name=i.tid)
			data_values.append(json.loads(json.dumps({"name": t.name,"lon":t.lon,"lat":t.lat})))
		return JsonResponse(data_values,safe=False)

def tollbooth_payments(request,pid):
	pay_values = []
	check = end_user.objects.filter(name=pid).exists()
	if(check):
		user = end_user.objects.all().get(name = pid)
		print user
		tid = user.user_log_set.all()
		print tid
		for i in tid:
			t = user_log.objects.get(id=i.id)
			pay_values.append(t)
		return render(request,"values/tables-basic2.html",{"data":pay_values})			
		
def numofusers(request):
	return render(request,'values/numofusers.html',{})
	
def chart(request):
	return render(request,'values/charts-chartjs.html',{})		
