#!/usr/bin/env python
from urlparse import urlparse
import socket as skt
import os
import sys
import asyncore


filename = sys.argv[-2]
f = open(filename , 'wb')

servName = sys.argv[-1]
# port = 8080
parsed_url = urlparse(servName)
s = parsed_url.hostname
n = parsed_url.path
pp = parsed_url.port
port = pp

if pp==None:
	pp = 80

s = urlparse(servName).hostname
print s
n = urlparse(servName).path
# print 'hostname',s
# print 'path', n

def sendHeader(server, path):
	return ("GET {n} HTTP/1.1\r\n"+ "Host: {s}\r\n\r\n").format(s=server, n=path)



clientSocket = skt.socket(skt.AF_INET,skt.SOCK_STREAM)
clientSocket.connect((s, port))

request1 = sendHeader(s,n)

clientSocket.send(request1)



data = ""
header_buffer = ''
while True:

	data_received = clientSocket.recv(1024)
	header_buffer += data_received
	if '\r\n\r\n' in header_buffer:
		header, remain = header_buffer.split('\r\n\r\n')
		f.write(remain)
		break

left_huge=''
while True:
	data_received = clientSocket.recv(1024)
	left_huge+= data_received
	if len(data_received)==0:
		f.write(left_huge)
		break
 
f.close()


content1 = header.split('Content-Length: ')
# print content1
ww = content1[1]
www = ww.split('Connection: ')
Cl = www[0] #Content length
print Cl

# qq = first_received.split('\r\n\r\n')
# All_data = qq[1]
# print All_data #all the remaining data

