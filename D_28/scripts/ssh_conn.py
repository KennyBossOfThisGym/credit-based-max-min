#!/usr/bin/python3.5
import paramiko
def ssh_connect():
	ssh_client=paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	return(ssh_client)
