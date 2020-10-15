#!/usr/bin/python3.5
import MySQLdb
def db_connect():
	db = MySQLdb.connect("172.31.20.2","collector","12345","collector" )
	cursor = db.cursor()
	return(cursor,db)