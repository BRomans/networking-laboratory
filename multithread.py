import thread
import socket
import sys



HOST = '127.0.0.1'   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    #dice al s.o. di aprire la connessione
    s.bind(HOST, PORT)
except socket.error, msg:
    print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()



def clientthread(conn):

    conn.send("Welcome to the server \n")

    while True:
        data = conn.recv(1024)
        reply = 'OK...' + data
        print data
        if not data or data == "ciao\r\n":
            break

        conn.sendall(reply)
    #came out of loop
    conn.close()


while 1:

    #wait to accept a connection - blocking call
    conn, addr = s.accept()

    thread.start_new_thread(clientthread, conn)

s.close()
