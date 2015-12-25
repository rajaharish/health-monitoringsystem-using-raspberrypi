from __future__ import unicode_literals
import MySQLdb
from time import strftime
from datetime import datetime
import os
import glob
import time
import smtplib

while True:
	os.system('sudo modprobe w1-gpio')
	os.system('sudo modprobe w1-therm')

	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'

	def read_temp_raw():
    		f = open(device_file, 'r')
    		lines = f.readlines()
    		f.close()
    		return lines

	def read_temp():
    		lines = read_temp_raw()
    		while lines[0].strip()[-3:] != 'YES':
        		time.sleep(0.2)
        		lines = read_temp_raw()
    		equals_pos = lines[1].find('t=')
    		if equals_pos != -1:
        		temp_string = lines[1][equals_pos+2:]
        		temp_c = float(temp_string) / 1000.0
        		temp_f = temp_c * 9.0 / 5.0 + 32.0
        		return temp_c, temp_f

	
	temp_cel,temp_far=read_temp()	
	print temp_cel
	time.sleep(1)
	temp_cel,temp_far=read_temp()
	print temp_cel
	#with open('../patientdetails.txt','r') as factive:
	#	readdata=factive.read().splitlines(False)
	#details=[]
	#for txt in readdata:
	#	details.append(txt)
	currenttime=strftime("%Y-%m-%d %H:%M:%S")
	con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
	cur = con.cursor ()
	#temp=30
	cur.execute("SELECT patientname,frequency,temp_threshold FROM patientdetails ORDER BY patientid DESC LIMIT 1")
	pdata=cur.fetchall()
	for row in pdata:
		pname=row[0]
		pfreq=row[1]
		ptemp_thres=row[2]

	print "patient name  from db ",pname
	print "patient freq from file ",pfreq
	print "patient threshold from file ",ptemp_thres
	#patientname=details[0]
	#freq=details[1]
	#threshold=details[2]
	threshold=ptemp_thres
	freq=pfreq
	patientname=pname
	pulse=170
	cur.execute("SELECT id FROM healthprojectapp_health ORDER BY id DESC LIMIT 1")
	data=cur.fetchall()
	for row in data:
		last_id=row[0]
	new_id=int(last_id)+1
	cur.execute("INSERT INTO healthprojectapp_health VALUES(%s,%s,%s,%s,%s)",(new_id,currenttime,pname,temp_cel,pulse))
	con.commit()
	con.close()

	print "time & temp ",currenttime,temp_cel



	def emailnotification(currenttime,temp_cel):

		server=smtplib.SMTP('smtp.gmail.com',587)

		gmail_user="harish753@gmail.com"
		gmail_pwd="Hari$1945"
		FROM="harish753@gmail.com"
		TO="rvempati@villanova.edu"
		SUBJECT="Health Monitoring Update"
		TEXT="\n Patient "+patientname+" Body Temperature is   "+str(temp_cel)+" C" "  on   " +str(currenttime)


		server.ehlo()
		server.starttls()

		server.login(gmail_user,gmail_pwd)

		msg="""\From : %s\nTo : %s\nSubject : %s\n\n%s"""%(FROM,TO,SUBJECT,TEXT)
		server.sendmail("harish753@gmail.com","rvempati@villanova.edu",msg)

		server.close()
		print "Email Notification Send Successfully"
	
	if (temp_cel>int(threshold)):
		print "Body Temeprature is not normal,will notify by email "
		emailnotification(currenttime,temp_cel)

	else:
		print "Body Temperature is normal,so no email notification has been sent"
	time.sleep(float(freq))
