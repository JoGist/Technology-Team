
import socket



msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("192.168.1.119", 20001)

bufferSize          = 1024



# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


while(True):
    # Send to server using created UDP socket

    UDPClientSocket.sendto(bytesToSend, serverAddressPort)



    msgFromServer = UDPClientSocket.recvfrom(bufferSize)



    msg = "Message from Server {}".format(msgFromServer[0])

    print(msg)
