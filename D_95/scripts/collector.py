#!/usr/bin/python3.5
import subprocess
from mysql_conn import db_connect
from ssh_conn import ssh_connect

##reset function!!!!
def collect_hostnames():
	ssh_client = ssh_connect()
	cursor,db = db_connect()
	cursor.execute("SELECT  INET_NTOA(ip) FROM credit_minmax")
	ip_list = [item[0] for item in cursor.fetchall()]
	for ip in ip_list:
		ssh_client.connect(hostname=ip,username='collector', key_filename='/home/collector/.ssh/id_rsa')
		stdin,stdout,stderr=ssh_client.exec_command('hostname')
		stdout.channel.recv_exit_status()
		out=str(stdout.read().decode('utf-8').strip())
		cursor.execute("UPDATE  credit_minmax SET hostname=%s, credits=0, sum_W=0 WHERE ip=INET_ATON(%s)",(out.strip(),ip))
		cursor.execute("UPDATE  minmax SET hostname=%s,sum_W=0 WHERE ip=INET_ATON(%s)",(out.strip(),ip))
		db.commit()
		ssh_client.close() 
def collect_demands():
	ssh_client = ssh_connect()
	cursor,db = db_connect()
	cursor.execute("SELECT  INET_NTOA(ip) FROM credit_minmax")
	ip_list = [item[0] for item in cursor.fetchall()]
	for ip in ip_list:
		ssh_client.connect(hostname=ip,username='collector', key_filename='/home/collector/.ssh/id_rsa')
		stdin,stdout,stderr=ssh_client.exec_command('python3 /home/collector/generate_W.py')
		stdout.channel.recv_exit_status()
		out=str(stdout.read().decode('utf-8').strip())
		cursor.execute("UPDATE  credit_minmax SET D=%s WHERE ip=INET_ATON(%s)",(out,ip))
		cursor.execute("UPDATE  minmax SET D=%s WHERE ip=INET_ATON(%s)",(out,ip))
		db.commit()
		ssh_client.close() 