# Modules
import threading
import ipaddress
import itertools
import hashlib
import socket
import string
import random
import math
import time
import sys
import os

# Local Modules
import Parser as argsp
import log

# Get command line arguments
args    = argsp.get_args()
argsp.check_args(args)

# Open file and readline by line
file    = open(args['f'], 'r')
lines   = [line for line in file]
payload = "\n".join(lines)
length  = sum(map(len, lines))
print("total length:",length)
file.close()

# Create socket and initialize server address
UDP_IP_ADDRESS  = args['a']
UDP_PORT_NO     = int(args['s'])
clientSock      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.bind(('',int(args['c'])))

# Processing delay
PROCESSING      = 95
# Paylod logic
INIT_PSIZE      = 1
PAYLOAD_SIZE    = INIT_PSIZE
VALID_PSIZE     = 1
PL_FACTOR       = 1
MODE            = 0
# Queue logic
QUEUE           = []
QUEUE_SIZE      = 1
VALID_QSIZE     = 1
QUEUE_MODE      = 0

# Set initial timeout
clientSock.settimeout(PROCESSING)

# Initialize transaction
latency_time = time.time()
intentMessage = "ID" + args['i']
clientSock.sendto(intentMessage.encode(), (UDP_IP_ADDRESS,UDP_PORT_NO))
transactionID, addr = clientSock.recvfrom(1024)
latency = time.time() - latency_time
print("latency:",latency)

# Log transaction to log file
transactionID = transactionID.decode()
log.add(transactionID+"|"+UDP_IP_ADDRESS)
if transactionID == "Existing alive transaction": os._exit(0)

# Set and initialize variables
seqnum, id, txn = 0, args['i'], transactionID

# start time
start_time = time.time()

# Send payload
while payload:
    queueCounter = 0
    payloadChange = 1

    # Conditional exit
    if time.time() - start_time > 130:
        print("Failed to send payload on time")
        clientSock.close()
        os._exit(0)

    # Send packets (based on queue size)
    for i in range(QUEUE_SIZE):

        # Sequence number, rransaction number, z
        sn, z, pl = f'{seqnum+i:07d}', '0', payload[PAYLOAD_SIZE*i:PAYLOAD_SIZE*(i+1)]

        # Adjust z if it is the last packet
        if not len(payload[PAYLOAD_SIZE*(i+1):]):
            z = '1'

        # Build and send payload
        build_message = "ID" + id + "SN" + sn + "TXN" + txn + "LAST" + z + pl
        clientSock.sendto(build_message.encode(), (UDP_IP_ADDRESS,UDP_PORT_NO))
        print('('+str(PAYLOAD_SIZE)+','+str(QUEUE_SIZE)+')\t' + build_message)

        # Add to queue
        QUEUE.append([build_message,z,PAYLOAD_SIZE])

        # Make sure packets get sent in order
        # time.sleep(latency)

        # Pressumed last packet
        if z == '1':
            break

    # Receive packets (based on queue size)
    for i in range(QUEUE_SIZE):
        try:
            # Try receiving the packet
            receive_time = time.time()
            ack, addr = clientSock.recvfrom(1024)
            snServer, txnServer, chksum = argsp.parse_ack(ack.decode())
            message, z, size = QUEUE.pop(0)

            # Check Acked packet
            print(snServer)

            # Get current expected message to be acked
            idMsg, snMsg, txnMsg, zMsg, plMsg = argsp.parse_packet(message)

            # Adjust to incorrect packet
            if (snMsg != snServer):
                if (argsp.compute_checksum(message) != chksum):
                    print("not the expected ACK!")
                    
                    # Received late
                    if int(snServer) < int(snMsg): continue
                    
                    # Not the expected packet > SN
                    seqnum += (int(snServer)-int(snMsg)+1)
                    payload = payload[size:]
                    queueCounter += 1

                    for i in range(int(snServer)-int(snMsg)):
                        message, z, size = QUEUE.pop(0)
                        payload = payload[size:]
                    continue

                else: seqnum += 1
            else: seqnum += 1

            # Update payload and sequence number
            payload = payload[size:]

            # Guess processing delay from packet 1 and processing time
            if int(snMsg) == 0:
                PROCESSING = time.time() - receive_time
                clientSock.settimeout(PROCESSING+latency+0.75)
                PAYLOAD_SIZE = math.ceil(length/(78/(PROCESSING-latency))) # PAYLOAD_SIZE = int(length//((85-PROCESSING)/(PROCESSING-latency)))
                print("Delay:", PROCESSING, "PAYLOAD SIZE:", PAYLOAD_SIZE)
            else:
                PROCESSING = (1-0.125)*PROCESSING + \
                            (0.125)*(time.time()-receive_time)
                if MODE == 3 and QUEUE_MODE == 1:
                    clientSock.settimeout(PROCESSING+PROCESSING*(0.125)+0.75)

            # Payload logic
            if MODE == 0 and payloadChange and seqnum-1: MODE = 3
            if MODE == 1 and payloadChange:
                if PROCESSING < 3: MODE = 2
                else: MODE = 3
            if MODE == 2 and payloadChange:
                VALID_PSIZE = PAYLOAD_SIZE
                PAYLOAD_SIZE += PL_FACTOR
                payloadChange = 0
                PL_FACTOR *= 2

            # Adjust queue size
            if QUEUE_MODE == 0 and PROCESSING < 3 and MODE == 3:
                queueCounter += 1
                QUEUE_SIZE += 1
            elif QUEUE_MODE == 0 and PROCESSING > 3:
                QUEUE_MODE = 1

            # Exit program
            if zMsg == '1':
                clientSock.close()
                os._exit(0)

        except:
            # Packet not received
            QUEUE = []

            # If no packets where returned
            if queueCounter == 0:
                # Wrong first guess
                if MODE == 0:
                    PAYLOAD_SIZE = int(PAYLOAD_SIZE*(90/100))
                    MODE = 1
                    break
                # Wrong correction
                elif MODE == 1:
                    PAYLOAD_SIZE = int(PAYLOAD_SIZE*(90/100))
                    break
                # Final correction
                elif MODE == 2:
                    PAYLOAD_SIZE -= int(PL_FACTOR/2)
                    MODE = 3
                    break

            # If some of the packets are lost
            else:
                print('packet lost!')
                QUEUE_SIZE = queueCounter
                QUEUE_MODE = 1
                break
