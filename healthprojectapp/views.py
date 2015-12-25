from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from healthprojectapp.models import health
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from healthprojectapp.serializers import HealthSerializer
import requests
import json
import datetime
from django.contrib import messages
from time import strptime
import os
import glob
import time
import MySQLdb
import collections
import subprocess
from django.contrib import auth
from django.core.context_processors import csrf 
# Create your views here.


class HealthViewSet(viewsets.ModelViewSet):
	queryset=health.objects.all()
	serializer_class=HealthSerializer

@cache_control(no_cache=True, must_revalidate=True)
def func():
  #some code
	return
@login_required
def home(request):

	#if(request.GET.get('startmonitoring')):
		
	
	#	return render_to_response('indexhtml.html', RequestContext(request, {}))
	r=requests.get('http://127.0.0.1:8000/health/',auth=('health','health'))
	result=r.text
	output=json.loads(result)
	count=output['count']
	count=int(count)-1
	#print "c ",count
	#print "text ",result
	con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
        cur = con.cursor ()
	cur.execute("SELECT timestamp,name,temperature,pulse from healthprojectapp_health ORDER BY id DESC LIMIT 1")
	data=cur.fetchall()
	for row in data:
		timestamp=str(row[0])
		name=row[1]
		temperature=row[2]
		pulse=row[3]

	#timestamp=output['results'][count]['timestamp']
	#name=output['results'][count]['name']
	#temperature=output['results'][count]['temperature']
	#pulse=output['results'][count]['pulse']
	#DATETIME_FORMAT = '%m-%d-%Y %H:%M:%S'
	date= timestamp.partition("T")
	#return render_to_response('index.html')
	return render_to_response('testhtml.html',{'timestamp':timestamp[:10]+" "+timestamp[11:19],'name':name,'temperature':temperature,'pulse':pulse})
	#return render_to_response('index.html',{'healthdata':result})

@login_required
def archive(request):


	list=[]
	#data=[]
	#con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
	#cur = con.cursor ()

	#cur.execute('SELECT * FROM healthprojectapp_health')
	#data=cur.fetchall()
	#con.close()
	#return render_to_response('archive.html',{'data':data})


	#r=requests.get('http://127.0.0.1:8000/health/',auth=('health','health'))
        #result=r.text
        #data=json.loads(result)
	#count=data['count']
	#c=1;
	#for c in range(count):
	#	temp=str(data['results'][c]['temperature'])
	#	pulse=str(data['results'][c]['pulse'])
	#	name=str(data['results'][c]['name'])
	#	time=str(data['results'][c]['timestamp'])
		
	#	list.append(temp+pulse+name+time)
	
	#return render_to_response('archive.html',{'data':list})
	con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
        cur = con.cursor ()
        cur.execute("SELECT patientname FROM patientdetails ORDER BY patientid DESC LIMIT 1")
        data=cur.fetchall()
        for row in data:
                last_patient=row[0]

	if 'Patient_Name' in request.GET:
        	last_patient=request.GET['Patient_Name']
	
	d=collections.OrderedDict()
	r=requests.get('http://127.0.0.1:8000/health/',auth=('health','health'))
        result=r.text
        data=json.loads(result)
	count=data['count']
	c=0
	x=int(count)-1
	#print "count ",count
	#print "x ",x

	cur.execute("SELECT timestamp,name,temperature,pulse from healthprojectapp_health where name=%s ORDER BY id DESC ",last_patient)
	fulldata=cur.fetchall()
        for row in fulldata:
                timestamp=str(row[0])
                name=row[1]
                temperature=row[2]
                pulse=row[3]
		item="dict"+str(x)
		d[item]=collections.OrderedDict()
		formattedtime=timestamp[:10]+" "+timestamp[11:19]
		d[item]['time']=formattedtime
                d[item]['name']=name
                d[item]['temp']=temperature
                d[item]['pulse']=pulse
                print "data  ",d[item]
                x=x-1
	'''
	for _ in range(count):
		
		if data['results'][x]['name']==last_patient:
			item="dict"+str(x)
			d[item]=collections.OrderedDict()
			temp=data['results'][x]['temperature']
                	pulse=data['results'][x]['pulse']
                	name=data['results'][x]['name']
                	time=data['results'][x]['timestamp']
			formattedtime=time[:10]+" "+time[11:19]
			#d[item]={'temp':temp,'pulse':pulse,'name':name,'time':time}
			#d[item]={'time':time,'name':name,'temp':temp,'pulse':pulse}
			#d[item]={'pulse':pulse,'name':name,'temp':temp,'time':formattedtime}
			d[item]['time']=formattedtime
			d[item]['name']=name
			d[item]['temp']=temp
			d[item]['pulse']=pulse
			print "data  ",d[item]
			x=x-1
	'''	
	return render_to_response('archivetest.html',{'data':d})	

@login_required
def pdetails(request):
	msg=""
	return render_to_response('form.html',{'msg':msg})
@login_required
def formsubmit(request):
	if request.user.is_authenticated():
		if 'InputName' in request.GET:
			patientName=request.GET['InputName']
			Freq=request.GET['InputFreq']
			threshold=request.GET['Inputthreshold']
	
		print "patient name : ",patientName
		print "monitoring freq : ",Freq
		print "threshold : ",threshold
		con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
        	cur = con.cursor ()
		cur.execute("SELECT patientid FROM patientdetails ORDER BY patientid DESC LIMIT 1")
        	data=cur.fetchall()
        	for row in data:
                	last_id=row[0]
        	new_id=int(last_id)+1
		cur.execute("INSERT INTO patientdetails VALUES(%s,%s,%s,%s)",(new_id,patientName,Freq,threshold))
		con.commit()
        	con.close()
		messages.success(request,"Patient Created Successfully")
		#file=open("patientdetails.txt","w")
		#file.write(str(patientName)+"\n")
		#file.write(str(Freq)+"\n")
		#file.write(str(threshold)+"\n")
		#file.close()
		return render(request,'form.html',{})
	else:
		return render_to_response('login.html',{},context_instance=RequestContext(request))

def logindetails(request):
	masg=""
	return render_to_response('login.html',{'masg':masg})


def logout(request):
	auth.logout(request)
	return render_to_response('login.html',{},context_instance=RequestContext(request))
	
def login2(request):
	username=""
	if 'Username' in request.GET:
		username=request.GET['Username']
		password=request.GET['Password']
	#print "username :",username,password
	'''
	user = authenticate(username=username, password=password)
	if user:
		if user.is_active:
			login(request, user)
			return render_to_response('form.html',{})
		else:
			return HttpResponse("Account disables")
	else:
		print "invalise login"
		return HttpResponse("Invalid Login")
	'''
	con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
	cur = con.cursor ()
	cur.execute("SELECT password from users where username=%s",username)
	row=cur.fetchone()
	while row is not None:
		print row[0]
		print password
		if row[0]==password:
			print "login success"
			return render_to_response('form.html',{})
		else:
			print "login failed"
			return render_to_response('archive.html',{})
	
def login(request):
	c={}
	c.update(csrf(request))
	return render_to_response('login.html',c,context_instance=RequestContext(request))

def invalid_login(request):
	messages.error(request,"Invalid Credentials.Please try again..!!")
	return render(request,'login.html',{})
def auth_view(request):
	username=request.POST.get('Username','')
	password=request.POST.get('Password','')
	print "user ",username
	user=auth.authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		return render_to_response('form.html',{},context_instance=RequestContext(request))
	else:
		messages.error(request,"Invalid Credentials.Please try again..!!")
        	return render(request,'login.html',{})
