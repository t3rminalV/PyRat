# Remote ArmA Server Administration Tool
# Written by Adam McKissock

import os
import sys
import socket

def header():
	os.system("cls");
	print '''
	##########################################
	##					##
	##	Remote Administration Tool	##
	##	    Client Application	        ##
	##	Written by Adam McKissock	##
	##					##
	##########################################
	''';

def readServers():
	file = open("servers.txt","r");
	content = file.read().splitlines();
	return content;

def openSocket(host, data):

	global Sock;
	
	try: 
		print "\nConnecting..."

		Sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM);
		Sock.connect ((host, 1337));

	except socket.error, (value,message): 
		if Sock:
	   		Sock.close();
	   	print "Could not open socket: " + message;
	   	sys.exit(1);

	if (Sock):
		Sock.send(data);
		Sock.recv (100);
		Sock.close();



header();

servers = readServers();

temp = 1;
for server in servers:
	print str(temp) + ") " + server;
	temp = temp + 1;

temp = raw_input("\n Select a server: ");
temp2 = servers[int(temp)-1]
temp3 = temp2.split(",");

selectedserver = temp3[0];
remotehost = temp3[1];

action = raw_input("\n Enter an action: ");

send = selectedserver+","+action;

openSocket(remotehost, send);




