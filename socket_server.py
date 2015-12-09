#! /usr/bin/env python
# coding:utf-8
#file=socket_server

import socket
import time
import threading
import Queue
import fcntl
import struct


def get_ip_address(ifname):
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])


class SocketServer:
	recv_data = ""
	__send_data =None
	__flag_succed = False
	__mysocket = None
	__client = 	None


	def __init__(self):
		self.__send_data=Queue.Queue(200)
		self.__mysocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		ip=get_ip_address('wlp6s0')
		print("ip:%s\n"%ip)
		self.__mysocket.bind((ip,1333))
		self.__mysocket.listen(10)
		print("waitting connect\n")
		try:
			self.__client,addr=self.__mysocket.accept()
			self.__flag_succed=True
			print("connect succed \n")
		except:
			print("connect fail\n")
			self.__flag_succed=False
		if self.__flag_succed==True:
			threading.Thread(target=self.__recv).start()
			threading.Thread(target=self.__send).start()
		pass

	def __recv(self):
		while self.__flag_succed:
			try:
				recv_data=self.__client.recv(1024) 
				print(recv_data)
			except:
				print("fail to receive\n")
				break
		pass

	def __send(self):
		while self.__flag_succed:
			time.sleep(0.02)
			if not self.__send_data.empty():
				data=self.__send_data.get_nowait()
				if data:
					self.__client.send(data)
		pass

	def send(self,data):
		if self.__flag_succed:
			if not self.__send_data.full():
				self.__send_data.put(data)
				self.__send_data.put('\n')
		else:
			print("erro:socket not connected\n")

if __name__ == "__main__":

	MyServer=SocketServer()
	while True:
		data=raw_input()
		MyServer.send(data)








