import Parser as argsp
import socket

# Get command line arguments
args    = argsp.get_args()
argsp.check_args(args) #; argsp.print_args(args)

# Open file and readline by line
file    = open(args['f'], 'r')
lines   = [line for line in file]
payload = "\n".join(lines)
file.close()
                                                    #print(payload)
                                                    #print(len(max(lines, key=len)))
                                                    #print(sum(map(len, lines)))

# Create socket and initialize server address
UDP_IP_ADDRESS  = args['a']
UDP_PORT_NO     = int(args['s'])
clientSock      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.bind(('',int(args['c'])))

# Initialize transaction
intentMessage   = "ID" + args['i']
clientSock.sendto(intentMessage.encode(), (UDP_IP_ADDRESS,UDP_PORT_NO))










# Initialize hidden parameters
# psize           = len(payload)//2
# queueLength     = 1
# processing      = 0

# Sendpayload
# while payload:
#     pass

# clientSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# clientSock.bind(('',6789))
