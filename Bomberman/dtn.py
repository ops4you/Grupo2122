import argument_parsers
import socket
import struct
import sys

serverAddress = "::1"
serverPort = 5555

class WirelessNode():
    def __init__(self,ip,port,gw):
        self.ip = ip
        self.port = port
        self.gw = gw
        self.neighbours = {}

    def multicast_communication(self):

        #Receive Information

        # Initialise socket for IPv6 datagrams
        socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Allows address to be reused
        socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Binds to all interfaces on the given port
        socket.bind(('', 8080))

        # Allow messages from this socket to loop back for development
        socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)

        # Construct message for joining multicast group
        join_data = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
        socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, join_data)

        # Received message and join to nighbours group
        data, addr = socket.recvfrom(1024)
        message = data.decode('utf8')
        print(message)
        self.message_parsing(message)

        #Send Information

        #message to send via multicast and multicast group information
        message = 'hello packet from ' + str(self.ip) + ',' + str(self.port) + ' ' + str(self.gw)
        multicast_group = ("ff02::abcd:1", 8080)

        # Send multicast message
        socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        socket.sendto(message.encode('utf-8'), multicast_group)


    def message_parsing(self,message):
        
        #split message information
        message = message.split(" ")

        if (str(self.ip) + ',' + str(self.port)) != message[1]:
         if message[2] == '1':
            self.neighbours.update({message[1]: 0})
         elif message[1] not in self.neighbours:
            self.neighbours.update({message[1]: 1})
         elif message[1] in self.neighbours:
            self.neighbours[message[1]] = self.neighbours[message[1]] + 1

    def gateway_communication(self):
        serverAddressPort = (serverAddress, serverPort)
        UDPGatewaySocket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_DGRAM)
        UDPGatewaySocket.bind((self.ip, self.port))
        data, addr = UDPGatewaySocket.recvfrom(1024)
        message = data.decode('utf8')
        message_splitted = message.split(" ")

        if(message_splitted[0]=='S'):
         for x in self.neighbours:
           socket.sendto(message.encode('utf-8'), x) 

        if(message_splitted[0]=='C'):
         socket.sendto(message.encode('utf-8'), serverAddressPort) 

class NodeForwarding():
    
    player_ip,serverAddress,serverPort,clientport = argument_parsers.clientParse()
