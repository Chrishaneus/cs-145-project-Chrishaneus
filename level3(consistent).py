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

# Initialize hidden
PROCESSING      = 20
INIT_PSIZE      = int(sum(map(len, lines))*0.1) # 0.06
PAYLOAD_SIZE    = INIT_PSIZE
VALID_PSIZE     = 1
MODE            = 0         # Ethernet’s binary exponential
QUEUE           = []
QUEUE_SIZE      = 1
QUEUE_MODE      = 0         # AIMD approach to congestion control
VALID_QSIZE     = 1

PSIZE_RATIO     = 0
QSIZE_RATIO     = 0
RATIO           = [0.25,0.1,0.05,0.0]

# Set variables
seqnum, id, txn = 0, args['i'], transactionID

# start time
start_time = time.time()

# Send payload
while True:
    queueCounter = 0
    payloadChange = 1
    PREV_PSIZE = 0
    breakOuter = 0

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

            # Correction checks
            if (snMsg != snServer): print("sequence number:", snMsg)
            if (argsp.compute_checksum(message) != chksum): print("checksum:", chksum)

            # Processing delay
            if int(snMsg) == 0:
                PROCESSING = time.time() - start_time + 0.25
                clientSock.settimeout(PROCESSING)
                print("Delay:", PROCESSING, int(snMsg))
                
            # next packet
            if payloadChange: payload = payload[PAYLOAD_SIZE:]
            else: payload = payload[VALID_PSIZE:]
            seqnum += 1

            # Altered binary exponential backoff
            if payloadChange:
                VALID_PSIZE = PAYLOAD_SIZE
                PAYLOAD_SIZE += int(PAYLOAD_SIZE*RATIO[PSIZE_RATIO])
                payloadChange = 0

            # Altered AIMD approach
            if QUEUE_MODE == 0 and queueCounter == QUEUE_SIZE:
                VALID_QSIZE = QUEUE_SIZE
                QUEUE_SIZE *= 2
            if QUEUE_MODE == 1 and queueCounter == QUEUE_SIZE:
                VALID_QSIZE = QUEUE_SIZE
                QUEUE_SIZE += 1

            # Check if last packet is ACKED
            if zMsg == '1':
                breakOuter = 1
                break

        except:
            QUEUE = []
            if queueCounter == 0:
                PAYLOAD_SIZE = VALID_PSIZE
                PSIZE_RATIO += 1
                break
                # if MODE == 0:
                #     MODE = 1; break
                # if MODE == 1:
                #     PSIZE_RATIO += 1; break
            elif queueCounter != QUEUE_SIZE:
                QUEUE_SIZE = VALID_QSIZE
                if QUEUE_MODE == 0:
                    QUEUE_MODE = 1
                    break
                if QUEUE_MODE == 1:
                    QUEUE_MODE = 2
                    break
                
    if breakOuter:
        break