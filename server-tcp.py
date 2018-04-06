import SocketServer
import socket
import threading
import time



class EchoRequestHandler(SocketServer.BaseRequestHandler):

    def handler(self):

        # retrieve received data
        data = self.request.recv(1024)

        # send back to client
        server.request.send("OK..." + data)
        return


address = ('', 8888)
server = SocketServer.TCPServer(address, EchoRequestHandler)
ip, port = server.server_address

# start thread with tcp server
t = threading.Thread(target = server.serve_forever)
t.setDaemon(True)
t.start()
print "Server started..."

# sleep 300 seconds then shutdown
time.sleep(300)

print "Shutting down server..."

server.shutdown()
