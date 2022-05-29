import socket
import sys

# UDP
clientSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
clientSock.bind(('',6789))

#TCP
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(("10.0.2.6", 58913))

# print(sys.version)

moves = ["odd","even","exit"]

while True:
	move = input()
	if move in moves:
		clientsocket.send(move.encode())
		text, addr = clientSock.recvfrom(1024)
		
		if text.decode() == "Goodbye!":
			break
		
		score, addr = clientSock.recvfrom(1024)
		print(text.decode()); print(score.decode())
	
	
	
	
