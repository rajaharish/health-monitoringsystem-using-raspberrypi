import MySQLdb
from time import strftime
import os
import glob
import time


data=[]


con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
cur = con.cursor ()

cur.execute('SELECT * FROM healthprojectapp_health')
data=cur.fetchall()
con.close()

for x in data:
	for y in x:
		print y
