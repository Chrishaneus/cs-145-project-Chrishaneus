import socket

UDP_IP_ADDRESS = "54.179.155.51"
UDP_PORT_NO = 6789

Message = "areyoureadyforthis".encode()

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(Message, (UDP_IP_ADDRESS,UDP_PORT_NO))
