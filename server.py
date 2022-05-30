import threading
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

def debug_payload(id, sn, txn, z, pl):
		print("ID  :",id)
		print("SN  :",sn)
		print("TNX :",txn)
		print("Z   :",z)
		print("PL  :",pl)
		print("====="*10)

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

PAYLOAD_SIZE 	= random.randint(64,80)
QUEUE			= []
QUEUE_SIZE		= random.randint(8,16)
PROCESSING		= random.uniform(1,2)
PAYLOAD			= ""
SEQNUM			= 0
print(PAYLOAD_SIZE,PROCESSING,QUEUE_SIZE)

receiverThread = receiver_thread(0, "receiver", QUEUE, QUEUE_SIZE)
receiverThread.start()

while True:
	# empty queue
	while(len(QUEUE) == 0):
		pass

	# time limit
	if time.time()-start_time > 120:
		break
	
	# get data
	queueLock.acquire()
	data, addr = QUEUE.pop(0)
	queueLock.release()

	# Step Two: Initiating a Transaction
	if len(data) == 10:
		start_time = time.time()
		print("intent message:", data)
		transactionID = ''.join(random.choice(string.digits) for _ in range(7))
		serverSock.sendto(transactionID.encode(), (addr[0], addr[1]))

	# Step Three: Sending the Payload or Data
	if len(data) > 10:
		id, sn, txn, z, pl = argsp.parse_packet(data)

		# Incorrect payload size
		if len(pl) > PAYLOAD_SIZE:
			continue
		
		# Incorrect expected sequence number
		if f'{SEQNUM:07d}' != sn:
			print(f'{SEQNUM:07d}',sn)
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

		# Last Packet
		if z == '1':
			break

file    = open('f64516b9.txt', 'r')
lines   = [line for line in file] #print(sum(map(len, lines)))
payload = "\n".join(lines)

print(time.time()-start_time)

if PAYLOAD == payload:
	print('Successfully sent data')
elif PAYLOAD in payload:
	print("sent "+str(len(PAYLOAD)*100/len(payload))+f"% of the payload")
else:
	print("Failed to send data")

receiverThread.join()