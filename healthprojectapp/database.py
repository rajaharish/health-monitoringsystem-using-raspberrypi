from __future__ import unicode_literals
import MySQLdb
from time import strftime


con =MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'mypassword', db = 'health_monitor')
cur = con.cursor ()
time= strftime("%Y-%m-%d %H:%M:%S")
temp=30
pulse=170
cur.execute("INSERT INTO healthprojectapp_health VALUES(%s,%s,%s,%s,%s)",("4",time,"name",temp,pulse))
con.commit()
con.close()

print time
