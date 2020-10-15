#!/usr/bin/python3.5
import paramiko
import MySQLdb
import subprocess
db = MySQLdb.connect("172.31.20.2","collector","12345","collector" )
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS hostpool")
sql = "CREATE TABLE hostpool (ip INT UNSIGNED, hostname varchar(15),W INT(11),credits INT(11),fairness double)"
cursor.execute(sql)

##get active connections
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
	input_devices = "INSERT INTO hostpool (ip) VALUES (INET_ATON('%s'))"
	#print (input_devices % ip)
	cursor.execute(input_devices % ip)
	
db.commit()	

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for ip in ip_pool:
	ssh_client.connect(hostname=ip,username='collector', key_filename='/home/collector/.ssh/id_rsa')
	stdin,stdout,stderr=ssh_client.exec_command('hostname')
       	#hostname_output = "UPDATE  hostpool SET hostname=%s WHERE ip=INET_ATON(%s)"
	stdout.channel.recv_exit_status()
	stdin_W,stdout_W,stderr_W=ssh_client.exec_command('python3 /home/collector/generate_W.py')
	stdout_W.channel.recv_exit_status()
	cursor.execute("UPDATE  hostpool SET hostname=%s, credits=100, W=%s WHERE ip=INET_ATON(%s)",(stdout.read().decode('utf-8').strip(),stdout_W.read().decode('utf-8').strip(),ip))
	db.commit()
	ssh_client.close() 

	
	
