import socket
import sys

UDP_IP = '127.0.0.1'   # Symbolic name meaning all available interfaces
UDP_PORT = 8888 # Arbitrary non-privileged port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print 'Socket created'

try:
    #dice al s.o. di aprire la connessione
    sock.bind((UDP_IP, UDP_PORT))
except socket.error, msg:
    print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'


print 'Socket now listening'

while True:
    #con udp non serve accettare richieste di connessione, si ricevono direttamente i dati
    data, addr = sock.recvfrom(1024)

    print "received message:", data
    reply = 'OK...' + data
    if not data or data.rstrip() == "ciao":
        break
    sock.sendto(data, (addr[0], addr[1]))

sock.close()
