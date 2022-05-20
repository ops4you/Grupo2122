import pygame
import socket
import threading

localIP     = "2001:690:2280:20::10"
localPort   = 5555
bufferSize  = 65536
addresses = []

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

def appendAddress(ad,ads):
 if ((ad in ads) == False):
  ads.append(ad)
 return ads 

def sendtoClient(ads,msg):
 clock = pygame.time.Clock()
 clock.tick(15)  
 msgFromServer = msg
 bytesToSend = str.encode(msgFromServer)
 for a in ads:
  UDPServerSocket.sendto(bytesToSend, a)

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):
    bytesreceivedS = UDPServerSocket.recvfrom(bufferSize)
    message = bytesreceivedS[0].decode('utf8')
    address = bytesreceivedS[1]

    appendAddress(address,addresses)

    x = threading.Thread(target=sendtoClient(addresses,message), args=(1,))
    x.start

    clientMsg = message + ' ' + str(address)
    print(clientMsg)
    

