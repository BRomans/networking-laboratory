
import socket   # for sockets
import sys  # for exit





try:
    # specifica che vogliamo creare un socket udp
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

print 'Socket Created'

# Resolve hostname
host = '127.0.0.1'

try:
    UDP_IP = socket.gethostbyname( host )

except socket.gaierror:
    # could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()



UDP_PORT = 8888
MESSAGE = "My udp message"
try:
    # con udp non c'e' bisogno di connettersi al server, non esiste handshake

    s.sendto(MESSAGE, (UDP_IP, UDP_PORT))
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()

print 'Message send successfully'


# Now receive data
reply = s.recvfrom(4096)

print reply

s.close()
