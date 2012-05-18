# Remote ArmA Server Administration Tool
# Written by Adam McKissock

import os, sys, socket, wmi, urllib, time, zipfile, fileinput
from subprocess import Popen

server = "";
action = "";
pid = "";
codever = "";
actionfile = "";

def header():
	os.system("cls");
	print '''
	##########################################
	##					##
	##	Remote Administration Tool	##
	##	    Server Application	        ##
	##	Written by Adam McKissock	##
	##					##
	##########################################
	''';

def openSocket():

	try: 
		print "\nWaiting For Connection..."

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		sock.bind (("", 1337));
		sock.listen(1);
	
	except socket.error, (value,message): 
		if sock:
	   		sock.close();
	   	print "Could not open socket: " + message;

	while True:
		channel, details = sock.accept();
		print "We have opened a connection with", details;
		temp = channel.recv(100);
		channel.close();
		print "Connection with", details, "closed.";
		return temp;
		break;

def getPid(name):
	filename = "pid/" + name + ".txt";	
	file = open(filename,"r");
	content = file.read();
	return content;

def isRunning():
	global pid;	

	pid = getPid(server);

	c = wmi.WMI();
	count = 0
	for process in c.Win32_Process (ProcessId=pid):		
 		print process.ProcessId, process.Name;
 		count = count + 1;

 	if count > 0:
 		return 1;
 	else:
 		return 0;	

def stopServer():	
	global pid;	

	pid = getPid(server);

	isrunning = isRunning();

	if isrunnning == 1:
		c = wmi.WMI()
		for process in c.Win32_Process (ProcessId=pid):
			process.Terminate ();
			print "Stopped!";

def startServer():	
	
	args = "start ..\\arma2oaserver.exe -port=2302 -mod=@dayz;@CBA;@JayArma2Lib -name=cfgdayz"+server+" -config=cfgdayz"+server+"\\server.cfg -cfg=cfgdayz"+server+"\\arma2.cfg -profiles=cfgdayz"+server+" -cpuCount=2 -world=Chernarus -noFilePatching -pid=dayzrat\\pid\\"+server+".txt";
	#args = "start calc.exe"
	p = Popen(args, bufsize=0, executable=None,stdin=None, stdout=None, stderr=None,preexec_fn=None, close_fds=False, shell=True);
	time.sleep(5);

class MyThread ( threading.Thread ):
	
	def run ( self ):
		os.system("..\\dayz" + server + ".bat");
		sys.exit();

def updateServer():

	stopServer();
	time.sleep(2);

	if actionfile == "core":
		urllib.urlretrieve("http://www.armafiles.info/" + "dayz/dayz_v" + codever + ".rar", "..\\@dayz\\Addons\\" + actionfile + ".zip");
	else:
		urllib.urlretrieve("http://www.armafiles.info/" + "dayz/dayz_"+ actionfile + "_v" + codever + ".rar", "..\\@dayz\\Addons\\" + actionfile + ".zip");
	
	time.sleep(1);

	os.rename("..\\@dayz\\Addons\\" + actionfile + ".rar","..\\@dayz\\Addons\\" + actionfile + ".zip");

	zip = zipfile.ZipFile("..\\@dayz\\Addons\\" + actionfile + ".zip");
	zip.extractall(path="..\\@dayz\\Addons\\");	

	print "Unziped!";

	if actionfile == "code":
		filename = "..\\" + "cfgdayz" + server + "\\server.cfg";
		writestring = 'hostname = "DayZ Zombie RPG - NZ (v' + codever + ') www.dayzmod.com";\n';

		f = open(filename,'r');
		lines = f.readlines();
		f.close();

		f = open(filename,'w');
		f.write(writestring);
		f.write(''.join(lines[1:]));
		f.close();

	    
	startServer();


def mainLoop():

	global server;
	global action;
	global actionfile;	
	global codever;	

	data = "";

	data = openSocket();
	data = data.split(",");

	print "TIST";
	print data;

	if "anim" in data[1] or "code" in data[1] or "equip" in data[1] or "sfx" in data[1]or "core" in data[1] or "vehicles" in data[1] or "weapons" in data[1]:
		print "1";
		server = data[0];
		action = data[1];
		temp = action.split();
		action = temp[0];
		actionfile = temp[1];
		codever = temp[2];
	else:
		print "2";
		server = data[0];
		action = data[1];	

	print "server: " + server;
	print "action: " + action;
	print "codever: " + codever;

	if action == "stop":
		stopServer();
		mainLoop();
		
	elif action == "start":
		startServer();
		mainLoop();

	elif action == "update":
		updateServer();
		mainLoop();
	else:
		print "Wrong command."
		mainLoop();


#Main code shizzle.
header();

mainLoop();

