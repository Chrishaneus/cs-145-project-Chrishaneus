import itertools
import ipaddress
import hashlib
import socket
import string
import random
import time
import sys

import hashlib

import Parser as argsp
import log

serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSock.settimeout(50.0)
serverSock.bind(('',9000))

PAYLOAD_SIZE 	= random.randint(20,50)
QUEUE			= []
QUEUE_SIZE		= random.randint(1,10)
PROCESSING		= random.uniform(1, 2)
PAYLOAD			= ""
print(PAYLOAD_SIZE)

def debug_payload(id, sn, txn, z, pl):
		print("ID  :",id)
		print("SN  :",sn)
		print("TNX :",txn)
		print("Z   :",z)
		print("PL  :",pl)
		print("====="*10)

while True:
	data, addr = serverSock.recvfrom(1024)
	data = data.decode()
	print(data)

	# Step Two: Initiating a Transaction
	if len(data) == 10:
		print("intent message:", data)
		transactionID = ''.join(random.choice(string.digits) for _ in range(7))
		serverSock.sendto(transactionID.encode(), (addr[0], addr[1]))

	# Step Three: Sending the Payload or Data
	if len(data) > 10:
		id, sn, txn, z, pl = argsp.parse_packet(data)
		# debug_payload(id, sn, txn, z, pl)

		if len(pl) > PAYLOAD_SIZE:
			continue

		PAYLOAD += pl

		# Processing Delay
		time.sleep(PROCESSING)

		# Build Acknowledgement
		ack = "ACK" + sn + "TXN" + txn + "MD5" + argsp.compute_checksum(data)
		serverSock.sendto(ack.encode(), (addr[0], addr[1]))

		# Last Packet
		if z == '1':
			file    = open('f64516b9.txt', 'r')
			lines   = [line for line in file] #print(sum(map(len, lines)))
			payload = "\n".join(lines)
			if PAYLOAD == payload: print('CORRECT')
			break