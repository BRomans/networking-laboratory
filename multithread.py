import thread
import socket
import sys




def clientthread():
    while True:
        data = conn.recv(1024)
        reply = 'OK...' + data


        if not data or data == "ciao\r\n":
            break



HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:

    #wait to accept a connection - blocking call
    conn, addr = s.accept()

    thread.start_new_thread(clientthread, conn)
