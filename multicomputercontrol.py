'''
Control multiple ssh clients simultaneously.
Useful Commands:	cusr - change client
					! - close connections
					all - all clients at once ***in progress

To do:	*** ON HOLD -- fix -all ***
		condense everything into Client and command functions
		eliminate globals
		enable desktop view (probably x11vnc)
		create installation, README, and help option 
		improve web browser performance 
		convert to python3
'''
import sys, os, subprocess, shlex, getpass 
from contextlib import contextmanager
from pexpect import pxssh

clientList = []
hostnameList = []
usernameList = []
passwordList = []

def main():	
	clients = raw_input("How many clients would you like to run? ")

	try:
		clients = int(clients)
	except ValueError:
		print ("Cannot have '%s' clients. Input must be a positive integer." \
			% (clients))
		sys.exit(-1)

	if clients <= 0:
		print ("Cannot have '%d' clients. Input must be a positive integer." \
			% (clients))
		sys.exit(-1)

	clientCnt = 1
	while clientCnt < (clients+1):
		print ("\nClient %d" % (clientCnt))
		addClient()
		print("***Successful Connection***")
		clientCnt += 1

	print ("\n--------------------------------------------------")
	runCommand(0, clientList[0])


class Client:

	def __init__(self):
		self.hostname = raw_input("Hostname: ")
		self.username = raw_input("Username: ")
		self.password = getpass.getpass("Password: ")
		
		graphics = raw_input("Enable graphics (y/n)? ")

		if graphics == 'y' or graphics.lower() == 'y':
			x11 = ' -X'
			self.hostname += x11

		try:
			s = pxssh.pxssh()
			s.login(self.hostname, self.username, self.password)
			self.session = s
		except Exception as e:
			print ("***Error Connecting***")
			print (e)
			
			while e:
				print ("\nCould not identify a matching client. Please try again.\n")
				self.hostname = raw_input("Hostname: ")
				self.username = raw_input("Username: ")
				self.password = getpass.getpass("Password: ")
				
				e2 = None
				try:
					s = pxssh.pxssh()
					s.login(self.hostname, self.username, self.password)
					self.session = s
				except Exception as e2:
					print ("Error Connecting")

				if e2 == None:
					break;

		

	def send_command(self, cmd):
		if cmd == '!':
			print ("Connection terminated.")
			self.session.logout()
			sys.exit(0) 
		else:
			self.session.sendline(cmd)
			self.session.prompt()
			return self.session.before 

def runCommand(clientNum, clientRunning):
	x = clientList[clientNum]
	y = usernameList[clientNum]
	usr = clientNum
	usrNum = usr + 1

	print ("Connected to remote host %s(%d)" % (y, usrNum))
	print ("(To end connection: <!>)\n")	

	while True:

		cmd_line = raw_input("%s(%d)-> " % (y, usrNum))
		
		if cmd_line == 'cusr':
			tmp = int(raw_input("Enter user number: "))
			tmp -= 1

			if tmp in range(0, len(clientList)):
				usr = tmp
				x = clientList[usr]
				y = usernameList[usr]
				print ("\n--------------------------------------------------")
				print ("Connected to remote host %s(%d)" % (y, usrNum))
				print ("(To end connection: !)\n")	
			else:
				print ("Invalid user.")
		#elif cmd_line == 'all':
			#new_terminal = 'gnome-terminal & -e '.format(' '.join(sys.argv))
			#p = subprocess.Popen(new_terminal, shell=True, \
			#	stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#os.system("nohup gnome-terminal &")

			#***os.system("gnome-terminal -e 'bash -c \"exec python botnetV1.py\"'")
			
			#subprocess.Popen(shlex.split\
			#	('gnome-terminal -x bash -c "python botnetV1.py; exec bash"'))

		else:
			result = x.send_command(cmd_line)
			result_list = result.split("\n")
			cnt = 0

			while cnt < len(result_list):
				if cnt != 0:
					print (result_list[cnt])
				cnt += 1

def addClient():
	client = Client()
	clientList.append(client)
	hostnameList.append(client.hostname)
	usernameList.append(client.username)
	passwordList.append(client.password)


if __name__ == "__main__":
	main()
