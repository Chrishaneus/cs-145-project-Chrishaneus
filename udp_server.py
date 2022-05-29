import socket

serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

serverSock.bind(('',6789))

while True:
	data, addr = serverSock.recvfrom(1024)
	if len(data) > 0:
		print(data.decode())
		break
