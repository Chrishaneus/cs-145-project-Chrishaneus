# Modules
import ipaddress
import itertools
import hashlib
import socket
import string
import random
import time
import sys

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
file.close()

# Create socket and initialize server address
UDP_IP_ADDRESS  = args['a']
UDP_PORT_NO     = int(args['s'])
clientSock      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.bind(('',int(args['c'])))

# Initialize transaction
intentMessage = "ID" + args['i']
clientSock.sendto(intentMessage.encode(), (UDP_IP_ADDRESS,UDP_PORT_NO))
transactionID, addr = clientSock.recvfrom(1024)
transactionID = transactionID.decode()
log.add(transactionID+"|"+UDP_IP_ADDRESS)

# Processing
PROCESSING      = 20

# Paylod Logic
INIT_PSIZE      = 1
PAYLOAD_SIZE    = INIT_PSIZE
VALID_PSIZE     = 1
MODE            = 0

# Queue Logic
QUEUE           = []
QUEUE_SIZE      = 1
QUEUE_MODE      = 0
VALID_QSIZE     = 1

# PSIZE_RATIO     = 0
# QSIZE_RATIO     = 0
# RATIO           = [1,0.25,0.0625,0.0]

# Set variables
seqnum, id, txn = 0, args['i'], transactionID

# start time
start_time = time.time()

PAYLOAD = ''

# Send payload
while True:
    queueCounter = 0
    breakOuter = 0
    payloadChange = 1

    print("=="*100)

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
        QUEUE.append([build_message,z])

        if z == '1':
            break

    for i in range(QUEUE_SIZE):
        try:
            # Check acknowledgement
            ack, addr = clientSock.recvfrom(1024)
            snServer, txnServer, chksum = argsp.parse_ack(ack.decode())
            message, z = QUEUE.pop(0)

            # Get current expected message to be acked
            idMsg, snMsg, txnMsg, zMsg, plMsg = argsp.parse_packet(message)
            queueCounter += 1

            # Check Acked packet
            print(snServer)

            # Correction checks
            if (snMsg != snServer): print("sequence number:", snMsg)
            if (argsp.compute_checksum(message) != chksum): print("checksum:", chksum)

            # Update payload and sequence number
            if payloadChange: payload = payload[PAYLOAD_SIZE:]
            else: payload = payload[VALID_PSIZE:]
            seqnum += 1

            # Processing delay
            if int(snMsg) == 0:
                PROCESSING = time.time() - start_time
                clientSock.settimeout(PROCESSING+1)
                PAYLOAD_SIZE = int(length//(95/(PROCESSING-0.1)))
                payloadChange = 0
                print("Delay:", PROCESSING, PAYLOAD_SIZE)
            
            # next packet
            # if payloadChange: payload = payload[PAYLOAD_SIZE:]
            # else: payload = payload[VALID_PSIZE:]
            
            # Altered binary exponential backoff
            if MODE == 0 and payloadChange:
                VALID_PSIZE = PAYLOAD_SIZE
                PAYLOAD_SIZE += 1
                payloadChange = 0

            # Altered AIMD approach
            if QUEUE_MODE == 0 and queueCounter == QUEUE_SIZE:
                VALID_QSIZE = QUEUE_SIZE
                QUEUE_SIZE += 1

            # Check if last packet is ACKED
            if zMsg == '1':
                breakOuter = 1
                break

        except:
            QUEUE = []
            
            # Payload size error
            if queueCounter == 0:
                if MODE == 0:
                    MODE = 1
                    PAYLOAD_SIZE -= 1
                    break
                elif MODE == 1:
                    PAYLOAD_SIZE -= 1
                    break
            
            # Queue size error
            elif queueCounter != QUEUE_SIZE:
                QUEUE_SIZE = VALID_QSIZE
                print("packet loss! decreased queue size")
                if QUEUE_MODE == 0: QUEUE_MODE = 1
                break
                
    if breakOuter:
        break
