import socket
import sys
import thread

def clientThread(conn):

    #conn.send("Connecting to the server... \n")

    data = conn.recv(1024)
    dataParseCommand = data.split('>')
    print('Received <' + dataParseCommand[0] +'> command...\n')
    if(dataParseCommand[0] == 'register'):
        print('Register procedure started...\n')
        reply = loginUser(dataParseCommand[1])
        conn.sendall(reply)

    conn.close()

def loginUser(data):
    dataParseName = data.split('|')
    username = dataParseName[0]
    dataParseAddress = dataParseName[1].split(':')
    userIpAddr = dataParseAddress[0]
    userPort = dataParseAddress[1]
    print (' -- User successfully registered --\n'
           ' -- Username: ' + username + ' --\n'
           ' -- Ip Address: ' + userIpAddr + ' --\n'
           ' -- Ip Port: ' + userPort + ' --\n')
    if not (checkExistingUserName(username)):
        addNewUser(username, userIpAddr, userPort)
    return username + ', you correctly joined our chat!\n'

def addNewUser(name, address, port):
    activeUsers[name] = [address, port]
    print ('User registered, updating dictionary...', activeUsers)

def checkExistingUserName(name):
    print ('Checking if user <' + name + '> is already registered...')
    return activeUsers.get(name) is not None and len(activeUsers.get(name)) > 0

def removeUser(name):
    print ('Removing user <' + name +'>...')
    activeUsers.pop(name)
    print ('User removed, updating dictionary...', activeUsers)


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

activeUsers = dict([('DummyUser', ['0.0.0.0', '8080'])])
print ('Init dictionary : ', activeUsers)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(100)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    print 'Waiting for users to open a connection...'
     #wait to accept a connection - blocking call
    conn, addr = s.accept()
    try:
        thread.start_new_thread(clientThread, (conn,))
        print 'Receiving registration from: ' + addr[0] + ':' + str(addr[1])
    except thread.error, msg:
        print 'Connection failed. Error Code : '  + str(msg[0]) + ' Message ' + msg[1]

s.close()
