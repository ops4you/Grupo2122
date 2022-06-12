from multiprocessing import connection
from multiprocessing.sharedctypes import Value
import time
import pygame
import socket
import threading

from yaml import add_representer

localIP     = "::1"
localPort   = 5555
bufferSize  = 65536
addresses = []
connection_counters = {}

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

def appendAddress(ad,ads):
 if ((ad in ads) == False):
  ads.append(ad)
 return ads 

def sendtoClient(ads,msg):
 msgFromServer = msg
 bytesToSend = str.encode(msgFromServer)
 for a in ads:
    UDPServerSocket.sendto(bytesToSend, a)

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):
    clock = pygame.time.Clock()
    clock.tick(15)
    bytesreceivedS = UDPServerSocket.recvfrom(bufferSize)
    message = bytesreceivedS[0].decode('utf8')
    address = bytesreceivedS[1]
    
    if address not in addresses:
      print("Player with IP " + str(address[0]) + " and port " + str(address[1]) + " connected!")

    appendAddress(address,addresses)

    if address not in connection_counters:
       connection_counters.update({address: 0})

    for key in connection_counters:

      if key == address:
       connection_counters.update({key: 0})
      elif key != address:
       connection_counters[key] = connection_counters[key] + 1

      if connection_counters[key]>30 and key in addresses:
        #del connection_counters(key)
        addresses.remove(key)

    print(connection_counters)
    print(addresses)

    x = threading.Thread(target=sendtoClient(addresses,message), args=(1,))
    x.start

    clientMsg = message + ' ' + str(address)
   
    

