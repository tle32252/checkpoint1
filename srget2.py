#!/usr/bin/env python
import socket as skt
import os
import sys
from urlparse import urlparse
import cStringIO
import asyncore
import os.path

class Downloader(object):
    def __init__(self, serv_name,url):
        self.host, self.path, self.port = self.parse_url(url)
        self.filename = sys.argv[-2]
        self.url = url
        self.f = open(self.filename , 'wb')
        
        # self.port = port
        self.clientSocket = skt.socket(skt.AF_INET,skt.SOCK_STREAM)
        self.request1 = self.makeReq("GET", self.path, {"HOST": self.host, "Connection": "close"})

        self.etagStat = False
        self.bytesCount = 0
        # self.headB = self.getHB()
        self.tailB = 0
        self.header_buffer = ""
        self.collectHeader = ""
        self.infoName = "info.txt"
        self.makeHeader()
        self.keeper= ''
        
        
        


        # self.main()
    def makeReq(self,req_type, what, details, ver="1.1"):
        NL = "\r\n"
        req_line = "{verb} {w} HTTP/{v}".format(verb=req_type, w=what, v=ver)
        details = ["{name}: {v}".format(name=n,v=v) for (n,v) in details.iteritems()]
        detail_lines = NL.join(details)
        full_request = "".join([req_line, NL, detail_lines, NL, NL])
        return full_request

    def parse_url(self,url, DEFAULT_PORT=80):
        parsed_url = urlparse(url)
        host, path, port = (parsed_url.hostname,parsed_url.path,parsed_url.port)
        if not port:
            port = DEFAULT_PORT
        return (host, path, port)

    # def connect(self):
    #     self.clientSocket.connect((self.host, self.port))



    def makeReqResu(self):
        self.headB = self.getHB()
        return ("GET {n} HTTP/1.1\r\n"+ "Host: {s}\r\n"+"Connection: close\r\n"+"Range: bytes={b}-\r\n\r\n").format(n=self.path,s=self.url,b=self.headB)
        

    def openCon(self):
        self.clientSocket.connect((self.host, self.port))
        self.clientSocket.send(self.request1)

    def openConResu(self):
        self.clientSocket.send(self.makeReqResu())

    def finish(self):
        self.clientSocket.close()

    def makeHeader(self):
        self.openCon()
        # while True:

        data = self.clientSocket.recv(1024)

        while data:
            self.collectHeader += data
            # print self.collectHeader
            if "\r\n\r\n" in self.collectHeader:
                self.head , self.remain = self.collectHeader.split("\r\n\r\n")
                self.f.write(self.remain)
                break
            

        
        self.realCl = self.getCl(self.head)
        self.realEtag = self.getEtag(self.head)
        self.realLmf = self.getLmndf(self.head)
        self.keeper = self.realCl+'\r\n'+self.realEtag+'\r\n'+self.realLmf+'\r\n'
        # print type(self.keeper)
        self.writeinfo()

    def makeHeaderResume(self): #need to stick with the same no of cl
        # self.headB = self.getHB()
        self.openConResu()
        data = self.clientSocket.recv(1024)
        while data:
            self.collectHeader += data
            # print self.collectHeader
            if "\r\n\r\n" in self.collectHeader:
                self.head , self.remain = self.collectHeader.split("\r\n\r\n")
                self.f.write(self.remain)
                break
        self.realEtag = self.getEtag(self.head)
        self.realLmf = self.getLmndf(self.head)
        self.keeper = self.realCl+'\r\n'+self.realEtag+'\r\n'+self.realLmf+'\r\n'
        self.writeinfo()

    
    def getHeader(self):
        while True:
            self.data = self.clientSocket.recv(8192)
            self.header_buffer += self.data
            if '\r\n\r\n' in self.header_buffer:
                self.header, self.remain = self.header_buffer.split('\r\n\r\n')
                self.bytesCount += len(self.remain)
                self.f.write(self.remain) #this will write the remaining part
                break

    def dlWithCL(self):

        self.cwd = os.path.abspath('.') + '/'
        counter = 0
        try:

            while self.bytesCount< int(self.Cl) and counter<5:
                self.data_received = self.clientSocket.recv(8192)
                self.f.write(self.data_received)
                # print int(self.bytesCount), int(self.Cl) - self.bytesCount
                self.bytesCount += len(self.data_received)
                counter += 1
                # print self.bytesCount

                # try:
                    # pass:
                    # print "tt"
                    # os.remove(self.cwd+self.infoNamye)
                # except OSError:
                    # pass
        except KeyboardInterrupt:
            self.f.write(str(self.bytesCount))

        finally: 
            self.finish()

    def getHB(self):
        curDir = os.getcwd()
        with open(curDir+'/'+self.filename+'part.txt', "r") as rh:
            read = rh.read()
            a,b = read.split('GMT')
            return b

    # def checking(self):



    def getCl(self,data):
        self.content1= data.split('Content-Length: ')
        self.ww = self.content1[1]
        self.www = self.ww.split('Connection: ')
        self.ContentLLL = self.www[0]
        self.Cl = self.ContentLLL.split("\r\n")[0]

        return self.Cl

    def getEtag(self,data):
        self.etag = data.split('ETag: ')
        self.etag2 = self.etag[1]
        self.etag3 = self.etag2.split('Accpet-Ranges: ')
        self.etag4 = self.etag3[0]
        self.etag5 = self.etag4.split("\r\n")[0]
        return self.etag5

    def getLmndf(self,data):
        self.lmf = data.split('Last-Modified: ')
        self.lmf2 = self.lmf[1]
        self.lmf3 = self.lmf2.split('Connection: ')
        self.lmf4 = self.lmf3[0] 
        self.lmf5 = self.lmf4.split("\r\n")[0]
        return self.lmf5

    # def chk(self):
    def writeinfo(self):
        with open(self.filename+'part.txt','wb') as q:
            q.write(str(self.keeper))
            q.write(str(self.bytesCount))






    def main(self):
        curDir = os.getcwd()
        print 'ss'

        if os.path.isfile(curDir+'/'+self.filename):
            # print 'yes'
            # sys.exit(1)
            print "hey im here"
            if os.path.isfile(curDir+'/'+self.filename+'part.txt'):
                # print 'yesysss'
                self.getHB()
                self.makeHeaderResume()
                # self.openConResu()
                self.writeinfo()
                self.dlWithCL() #resume part
                self.finish()

        
        # # self.makeHeader()
        # else:
        #     self.dlWithCL()
        #     print "this is count",self.bytesCount

        else:
            self.makeHeader()
            # self.openCon()
            self.writeinfo()
            self.dlWithCL() #download all
            os.remove(curDir+'/'+self.filename+'part.txt')
            self.finish()
            
                # print 'qq'
          

if __name__ == '__main__':
    serv_name = sys.argv[-1]
    url = sys.argv[-1]
    clients = [Downloader(serv_name,url)]
    asyncore.loop()




