#!/usr/bin/env python

import sys
# from socket import socket,AF_INET,SOCK_STREAM
from urlparse import urlparse
import socket as skt
import os
import asyncore
import threading


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
		self.nothread=0

		self.startBytes =0
		self.endBytes=0

		print "1"

	def checkport(self):
		if self.port == None:
			self.port = 80


	def connect(self):
		# print "2"
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
	

	def send_req_resume_for_thread(self,b,c):
		self.reqresume = "GET " + self.path + " HTTP/1.1\r\n" + "Host: " + self.host + "\r\nConnection: close"  "\r\nRange: bytes=" + str(b) + "-" + str(c)  + "\r\n\r\n"
		self.clientSocket.send(self.reqresume)


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
		print "Downloading Big Part"
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


	def download3(self,b,c): #huge part left
		self.clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
		self.connect()
		self.send_req_resume_for_thread(b,c)
		print "Downloading Big Part"
		with open((self.filename),'a') as d, open((self.filename+'part.txt'),'w') as f:
			try:
				while self.bytesCount<int(self.getCl()):
					data_received = self.clientSocket.recv(8192)
					d.write(data_received)
					self.bytesCount += len(data_received)
					print self.bytesCount
					# print int(self.bytesCount)
					if not data_received:
						break
			except KeyboardInterrupt,IOError:
				print "keyboard caught"
				f.write(str(self.cl2)+'  eeeeee  ') #full bytesCount
				f.write(str(self.bytesCount))
				print self.bytesCount
		self.clientSocket.close()
	# def threaddd(self):

		


	def getCl(self):
		head = self.header.split("\r\n")
		for i in head:
			if "Content-Length" in i:
				cl = i.split(":")
				self.cl2 = cl[-1]
				self.cl3 = int(self.cl2)
				return self.cl3
				# return int(self.cl2)

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
	def downloadResume(self):
		self.getHb2()
		self.checkport()
		self.connect()
		self.send_req_resume()
		self.download1()
		self.download_for_resume()

	def downloadAll(self):
		self.checkport()
		self.connect()
		self.send_req()
		self.download1()
		# self.calculate()
		self.download2()
		# self.getHb2()
	
	def downloadThread(self):
		self.checkport()
		self.connect()
		self.send_req()
		self.download1()
		self.getCl()
		self.clientSocket.close()
		self.calculate() #start
		self.calculate2() #stop
		self.calculate3()
		# self.looknong()
		# self.send_req_resume_for_thread()



		

	def calculate(self):
		# print '1111'
		lst =[]
		count = 0

		self.partion = 5
		thread = 5.0
		whole = self.cl3
		lst.append(0)

		while len(lst)<self.partion:
			# lst.append(0)
			self.inner = whole/self.partion
			count+=self.inner
			lst.append(count)
		return lst
	
	def calculate2(self):
		lst2 =[]
		whole2 = self.cl3
		for i in self.calculate():
			lst2.append(i-1)
		lst2.append(whole2-1)
		lst2.remove(-1)
		return lst2
	def calculate3(self):
		whole3 = self.cl3
		lstcal1 = self.calculate()
		lstcal2 = self.calculate2()
		lst3 =[]

		for i in range(len(lstcal2)):
		# lst3=[]
			a = lstcal1[i]
			b = lstcal2[i]
			lst3.append(a)
			lst3.append(b)
		# lst3=[]
		aa = [lst3[x:x+2] for x in xrange(0, len(lst3), 2)]
		Threadss= []
		print aa
		try:
			for a,b,c in zip(range(self.partion),self.calculate(),self.calculate2()):
				# self.clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
				tt = threading.Thread(target=self.download3(b,c))
				Threadss.append(tt)
				tt.start()
			for i in Threadss:
				i.join()
		except Exception as m:
			print m




	# 	for i in range(self.partion):
	# 		self.looknong(aa[i])
	# 		# print aa[i]


	# def looknong(self,aa):
	# 	ee = (aa[1]-aa[0])/self.partion
	# 	print ee
		







	def main(self):
		curDir = os.getcwd()
		if os.path.isfile(curDir+'/'+self.filename):
			if os.path.isfile(curDir+'/'+self.filename+'part.txt'):
				print "Your file have been downloaded before but not done yet."
				print "It will be resumed!"
				self.downloadResume()
				# self.getHb2()
				# self.checkport()
				# self.connect()
				# self.send_req_resume()
				# self.download1()
				# self.download_for_resume()
		else:
			
			self.downloadThread
			

			print "Your file never exist before, download initiated!"

			self.downloadThread()
			# self.calculate()
			# self.checkport()
			# self.connect()
			# self.send_req()
			# self.download1()
			# self.download2()
			# self.getHb2()
		

url = sys.argv[-1]
d = Downloader(url)
d.main()






