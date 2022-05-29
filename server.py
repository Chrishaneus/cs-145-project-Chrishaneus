import socket
import string    
import random

serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSock.bind(('',9000))

while True:
	data, addr = serverSock.recvfrom(1024)
	if len(data) > 0:
		print("intent message:", data.decode())
		random_number = ''.join(random.choice(string.digits) for _ in range(7))
		serverSock.sendto(random_number.encode(), ("10.0.2.12", 6691))
		break