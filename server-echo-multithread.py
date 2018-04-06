import thread
import socket
import SocketServer
import sys

#DA CORREGGERE

def clientthread():
    while True:
        data = conn.recv(1024)
        reply = 'OK...' + data


        if not data or data == "ciao\r\n":
            break

while 1:
    HOST = ''   # Symbolic name meaning all available interfaces
    PORT = 8888 # Arbitrary non-privileged port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
         #wait to accept a connection - blocking call
        conn, addr = s.accept()

        thread.start_new_thread(clientthread, (conn))

    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'

