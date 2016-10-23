import sys
# from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse
import socket as skt
import os
import asyncore


class Downloader:
	def __init__(self,url):
		self.clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
		self.host = urlparse(url).hostname
		self.path = urlparse(url).path
		self.port = urlparse(url).port
		self.headBytes = 0
		self.filename = sys.argv[-2]
		self.bytesCount = 0
		self.bytesCount2 = 0
		self.realCl = 0
		self.lefted = ""

	def checkport(self):
		if self.port == None:
			self.port = 80


	def connect(self):
		self.clientSocket.connect((self.host, self.port))
		print "Connected."

	def send_req(self):
		self.req = "GET " + self.path + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\n\r\n"
		self.clientSocket.send(self.req)
		print "Request header sent."

	def send_req_resume(self):
		self.reqresume = "GET " + self.path + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\nRange: bytes=" + str(self.getHb()) + "-"  + "\r\n\r\n"
		self.clientSocket.send(self.reqresume)
		print self.reqresume
		print "Request header (resume) sent."

	def download1(self):
		header_buffer =""
		data =""
		while True:
			data_received = self.clientSocket.recv(8192)
			header_buffer += data_received
			# print header_buffer, type(header_buffer)
			# with open((self.filename),'wb') as f:
			if '\r\n\r\n' in header_buffer:
				self.header, remain = header_buffer.split('\r\n\r\n')

				self.bytesCount += len(remain)
				self.lefted += remain
				with open((self.filename),'a') as d:
					d.write(self.lefted)

					# print "Remain written."

				break

	def download2(self): #huge part left
		print "sss"
		with open((self.filename),'a') as d, open((self.filename+'part.txt'),'w') as f:
			try:
				while self.bytesCount<int(self.getCl()):
					data_received = self.clientSocket.recv(8192)
					d.write(data_received)
					self.bytesCount += len(data_received)
					# print int(self.bytesCount)
			except KeyboardInterrupt,IOError:

				f.write(str(self.cl2)+'  eeeeee  ') #full bytesCount
				f.write(str(self.bytesCount))
				print self.bytesCount

	def download_for_resume(self): #huge part left
		self.bytesCount2 = self.getHb()
		print "wwwwww"
		
		with open((self.filename),'a') as d, open((self.filename+'part.txt'),'w') as f:
			try:
				while self.bytesCount2<int(self.realCl):
					data_received = self.clientSocket.recv(8192)
					d.write(data_received)
					self.bytesCount2 += len(data_received)
					#print int(self.bytesCount2)
			except KeyboardInterrupt,IOError:

				f.write(str(self.realCl)+'  eeeeee  ') #full bytesCount
				f.write(str(self.bytesCount2))

		


	def getCl(self):
		head = self.header.split("\r\n")
		for i in head:
			if "Content-Length" in i:
				cl = i.split(":")
				self.cl2 = cl[-1]
				return int(self.cl2)

	def getHb(self):
		with open((self.filename+'part.txt'),'r') as rd:
			read = rd.read()
			read2 = read.split('eeeeee')
			read3 = int(read2[1])
			return read3
			# print read3

	def getHb2(self):
		with open((self.filename+'part.txt'),'r') as rd:
			read = rd.read()
			read2 = read.split('eeeeee')
			read3 = int(read2[0])
			self.realCl = read3
			# print self.realCl
			# return read3 #full

	def main(self):
		curDir = os.getcwd()
		if os.path.isfile(curDir+'/'+self.filename):
			if os.path.isfile(curDir+'/'+self.filename+'part.txt'):
				print "Your file have been downloaded before but not done yet."
				print "It will be resumed!"
				self.getHb2()
				self.checkport()
				self.connect()
				self.send_req_resume()
				self.download1()
				self.download_for_resume()
		else:
			print "Your file never exist before, download initiated!"
			self.checkport()
			self.connect()
			self.send_req()
			self.download1()
			self.download2()
			self.getHb2()
		

url = sys.argv[-1]
d = Downloader(url)
d.main()






