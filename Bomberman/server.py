import socket

localIP     = "::1"
localPort   = 20001
bufferSize  = 1024

msgFromServer       = "Position Received!"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('utf8')
    address = bytesAddressPair[1]
    clientMsg = message + ' ' + str(address)
    print(clientMsg)
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)