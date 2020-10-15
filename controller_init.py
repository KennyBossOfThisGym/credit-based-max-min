#!/usr/bin/python3.5
import subprocess
from mysql_conn import db_connect
from ssh_conn import ssh_connect
from collector import collect_hostnames

def init():
	cursor,db = db_connect()
	ssh_client = ssh_connect()
	cursor.execute("DROP TABLE IF EXISTS credit_minmax")
	cursor.execute("DROP TABLE IF EXISTS minmax")
	#cursor.execute("DROP TABLE IF EXISTS fairness")

	cursor.execute("CREATE TABLE credit_minmax (ip INT UNSIGNED, hostname varchar(15),D INT(11), current_W INT(11), sum_W INT(30),credits INT(11))")
	cursor.execute("CREATE TABLE minmax (ip INT UNSIGNED, hostname varchar(15),D INT(11), current_W INT(30), sum_W INT(11))")
	#cursor.execute("CREATE TABLE fairness (quality INT(11))")

	#get active connections
	#docker inspect mouse_bridge | grep IPv4 | awk '{ print $2 }'| tr -d '"'| tr -d ','| sed 's/.\{3\}$//'
	inspect_pc = subprocess.Popen(["docker", "inspect", "mouse_bridge"], stdout=subprocess.PIPE)
	grep_pc = subprocess.Popen(["grep", "IPv4"], stdin=inspect_pc.stdout, stdout=subprocess.PIPE)
	tr1_pc = subprocess.Popen(["tr", "-d",'"'], stdin=grep_pc.stdout, stdout=subprocess.PIPE)
	tr2_pc = subprocess.Popen(["tr", "-d",","], stdin=tr1_pc.stdout, stdout=subprocess.PIPE)
	awk_pc = subprocess.Popen(["awk", '{ print $2 }'], stdin=tr2_pc.stdout, stdout=subprocess.PIPE)
	sed_pc = subprocess.Popen(["sed 's/.\{3\}$//'"], stdin=awk_pc.stdout, stdout=subprocess.PIPE,shell=True)
	inspect_pc.stdout.close()
	output=sed_pc.communicate()[0].decode('utf-8').strip()
	ip_pool=output.splitlines()

	for ip in ip_pool:
		input_devices = "INSERT INTO credit_minmax (ip) VALUES (INET_ATON('%s'))"
		cursor.execute(input_devices % ip)

	for ip in ip_pool:
		input_devices = "INSERT INTO minmax (ip) VALUES (INET_ATON('%s'))"
		cursor.execute(input_devices % ip)



	db.commit()	
	collect_hostnames()



