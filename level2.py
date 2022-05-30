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
intentMessage   = "ID" + args['i']
clientSock.sendto(intentMessage.encode(), (UDP_IP_ADDRESS,UDP_PORT_NO))
transactionID, addr = clientSock.recvfrom(1024)
transactionID = transactionID.decode()
log.add(transactionID+"|"+UDP_IP_ADDRESS)

# Initialize hidden
PAYLOAD_SIZE 	= 1
QUEUE_SIZE		= 1
PROCESSING		= 20
MODE            = 0
QUEUE           = {}

# Set timeout
clientSock.settimeout(PROCESSING)

# Set variables
seqnum, id, txn = 0, args['i'], transactionID

# start time
start_time = time.time()

# Send payload
while True:
    
    for i in range(QUEUE_SIZE):
        # Sequence Number, Transaction Number, Z
        sn, z, pl = f'{seqnum:07d}', '0', payload[0:PAYLOAD_SIZE]

        # Adjust Z if it is the last packet
        if not payload[PAYLOAD_SIZE:]:
            z = '1'

        # Build and send payload
        build_message = "ID" + id + "SN" + sn + "TXN" + txn + "LAST" + z + pl
        clientSock.sendto(build_message.encode(), (UDP_IP_ADDRESS,UDP_PORT_NO))
        QUEUE[sn] = build_message

    # Check Acknowledgement
    try:  
        ack, addr = clientSock.recvfrom(1024)
        print(build_message+'\t('+str(PAYLOAD_SIZE)+')')
    except:
        if MODE == 0:
            PAYLOAD_SIZE = PAYLOAD_SIZE//2
            MODE = 1
            continue
        if MODE == 1:
            PAYLOAD_SIZE = PAYLOAD_SIZE-1
            MODE = 2
            continue
    
    snServer, txnServer, chksum = argsp.parse_ack(ack.decode())

    # Checksum
    if (argsp.compute_checksum(build_message) == chksum): pass
    QUEUE.pop(sn)

    # Processing delay
    if PAYLOAD_SIZE == 1:
        PROCESSING = time.time() - start_time + 1
        clientSock.settimeout(PROCESSING)
        print("Delay:", PROCESSING)
        
    # next packet
    payload = payload[PAYLOAD_SIZE:]
    seqnum = seqnum + 1

    # Altered binary exponential backoff
    if MODE == 0: PAYLOAD_SIZE *= 2
    if MODE == 1: PAYLOAD_SIZE += 1

    if z == '1':
        break