#!/usr/bin/env python

'''
	given 2 arguments 
	first argument : unhex file name
	second argument : time for sending data

	example : 
		python client.py iperf-mptcp-0-0-unhex 3
'''

import socket, time, sys

TCP_IP = '10.0.3.238'
TCP_PORT = 15304
BUFFER_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))

myFile = open('UnHexFiles/' + sys.argv[1], 'r')
for line in myFile:
	s.send(line)
	data = s.recv(BUFFER_SIZE)
	print "received data:", data
	time.sleep(float(sys.argv[2]))

s.close()

