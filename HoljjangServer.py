import socket
import random

# UDP
serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('',58913))
serversocket.listen(5)

# NOTE: address format -> ('10.0.2.7', 53064)

connection,address = serversocket.accept()
moves 	= ["odd", "even", "exit"]
UDP_IP 	= address[0]
cscore 	= 0
sscore 	= 0
score	= ""
win  	= ""

while True:
	move = connection.recv(64).decode()	# move
	rndn = random.randint(1,10)			# random number

	# odd case
	if move == moves[0]:
		if rndn % 2 == 1:
			cscore += 1; win = "CLIENT"
		else:
			sscore += 1; win = "SERVER"
	# even case
	if move == moves[1]:
		if rndn % 2 == 0:
			cscore += 1; win = "CLIENT"
		else:
			sscore += 1; win = "SERVER"
	# exit case
	if move == moves[2]:
		serverSock.sendto("Goodbye!".encode(),(UDP_IP,6789))
		break

	# print and send
	if move in moves:
		win += " WINS!"
		score = "Client:\t"+str(cscore)+", Server:\t"+str(sscore)

		print(move)
		print(win)
		print(score)

		serverSock.sendto(win.encode(),(UDP_IP,6789))
		serverSock.sendto(score.encode(),(UDP_IP,6789))
