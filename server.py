import threading
import itertools
import ipaddress
import hashlib
import socket
import string
import random
import math
import time
import sys

import hashlib

import Parser as argsp
import log

serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSock.bind(('',9000))

start_time = 10 * time.time()
queueLock = threading.Lock()

class receiver_thread(threading.Thread):
	def __init__(self, threadID, name, q, s):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.queue = q
		self.size = s
	def run(self):
		while True:
			try:
				# get data
				data, addr = serverSock.recvfrom(1024)
				data = data.decode()
				queueLock.acquire()
				if len(self.queue) < self.size:
					self.queue.append([data,addr])
				queueLock.release()
			except:
				break

file    = open('payload/test.txt', 'r')
lines   = [line for line in file] #print(sum(map(len, lines)))
payload = "\n".join(lines)
length 	= sum(map(len, lines))


QUEUE			= []
QUEUE_SIZE		= random.randint(1,8)
PROCESSING		= random.uniform(1,10)
PAYLOAD_SIZE 	= math.ceil(length/(75/PROCESSING))
PAYLOAD			= ""
SEQNUM			= 0
UNIQUE_ID		= ""

serverSock.settimeout(30)
print(PAYLOAD_SIZE,PROCESSING,QUEUE_SIZE)

receiverThread = receiver_thread(0, "receiver", QUEUE, QUEUE_SIZE)
receiverThread.start()

while True:
	# empty queue
	while(len(QUEUE) == 0):
		if time.time()-start_time > 120: break

	# time limit
	if time.time()-start_time > 120:
		break

	# get data
	queueLock.acquire()
	data, addr = QUEUE[0]
	queueLock.release()

	# Step Two: Initiating a Transaction
	if len(data) == 10:
		start_time = time.time()
		print("intent message:", data)
		transactionID = ''.join(random.choice(string.digits) for _ in range(7))
		serverSock.sendto(transactionID.encode(), (addr[0], addr[1]))
		UNIQUE_ID = data
		QUEUE.pop(0)

	# Step Three: Sending the Payload or Data
	if len(data) > 10:
		id, sn, txn, z, pl = argsp.parse_packet(data)

		# Incorrect payload size
		if len(pl) > PAYLOAD_SIZE:
			QUEUE.pop(0)
			print('wrong payload size!', PAYLOAD_SIZE, len(pl))
			continue
		
		# Incorrect expected sequence number
		if f'{SEQNUM:07d}' != sn:
			QUEUE.pop(0)
			print('not the expected sequence number!',f'{SEQNUM:07d}',sn)
			continue

		# Incorrect ID
		if UNIQUE_ID[2:] != id:
			QUEUE.pop(0)
			print('Wrong ID!',UNIQUE_ID,id)
			continue

		# Processing Delay
		time.sleep(PROCESSING)
		PAYLOAD += pl

		# Build Acknowledgement
		ack = "ACK" + sn + "TXN" + txn + "MD5" + argsp.compute_checksum(data)
		print(ack)
		serverSock.sendto(ack.encode(), (addr[0], addr[1]))

		# Update expected sequence number
		SEQNUM += 1

		QUEUE.pop(0)

		# Last Packet
		if z == '1':
			break

print(time.time()-start_time)

if PAYLOAD == payload:
	print('Successfully sent data')
elif PAYLOAD in payload:
	print("sent "+str(len(PAYLOAD)*100/len(payload))+f"% of the payload")
else:
	print("Failed to send data")
	print(PAYLOAD)

receiverThread.join()