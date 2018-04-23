

import socket   #for sockets
import sys  #for exit
import thread


userIpdAddress = str(sys.argv[1])
userPort = int(sys.argv[2])
username = str(sys.argv[3])
connected = False
userList = []

# Resolve hostname
host = '127.0.0.1'

try:
    remote_ip = socket.gethostbyname( host )

except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip

#Connect to remote server
port = 8888

def registerToServer(command, username, userIpAddress, userPort):
    connected = True
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print ('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()
    clientSocket.connect((remote_ip , port))
    #Send some data to remote server
    connection_message = (username + ' is connecting...\r\n\r\n')
    print ('Socket Connected to ' + host + ' on ip ' + remote_ip)
    try :
        #Set the whole string
        clientSocket.send(command + '>' + username + '|' + userIpAddress+':' + str(userPort))
        #s.sendall(connection_message)
        print 'Connession successful'
        #Now receive data
        reply = clientSocket.recv(4096)
        print ('Server replied: ' + reply)
        clientSocket.close()
        if(reply.split('|')[0] == 'ERROR '):
            sys.exit(1)

    except socket.error, msg:
        #Send failed
        print ('Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])


def retrieveUserIp(name):
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    clientSocket.connect((remote_ip , port))
    #Send some data to remote server
    connection_message = ('User ' + name + ' is connecting...\r\n\r\n')
    print ('Socket Connected to ' + host + ' on ip ' + remote_ip)
    try :
        #Set the whole string
        clientSocket.send(name)
        #s.sendall(connection_message)
        print 'Connession successful'
        #Now receive data
        reply = clientSocket.recv(4096)
        print ('Server replied: ' + reply)
        clientSocket.close()

    except socket.error, msg:
        #Send failed
        print 'Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

def sendQuitSignal(username):
    command = 'quit'
    connected = False
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    clientSocket.connect((remote_ip , port))
    try :
        #Set the whole string
        clientSocket.send(command + '>' + username + '|')
        #Now receive data
        reply = clientSocket.recv(4096)
        print ('Server replied: ' + reply)
        clientSocket.close()

    except socket.error, msg:
        #Send failed
        print 'Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

def retrieveUserList():
    command = 'userList'
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    clientSocket.connect((remote_ip , port))
    try :
        #Set the whole string
        clientSocket.send(command + '>')
        #Now receive data
        reply = clientSocket.recv(4096)
        print ('Server replied: ' + reply)
        clientSocket.close()

    except socket.error, msg:
        #Send failed
        print 'Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

def retrieveUserInfo(name):
    command = 'getUser'
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    clientSocket.connect((remote_ip , port))
    try :
        #Set the whole string
        clientSocket.send(command + '>' + name + '|')
        #Now receive data
        reply = clientSocket.recv(4096)
        print ('Server replied: ' + reply)
        clientSocket.close()

    except socket.error, msg:
        #Send failed
        print 'Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

def printHelpManual():
    print ('Hello, here you are a quick guide for the chat application:\n'
           '-- !connect <username> : ask to the server the ip address of the specified user and then will start a chat with him\n'
           '-- !connect : after this command the client will ask the username of the user you want to connect\n'
           '-- !reconnect : this command manually reconnect to the chat server\n'
           '-- !disconnect : disconnect from server\n'
           '-- !close : close current chat\n'
           '-- !users : retrieve users list\n'
           '-- !get <username> : retrieve infos about the specified user\n'
           '-- !quit : close the client application\n')

def startUpdServer():
    print ('Listening for users to connect...')
    udp_socket.bind((userIpdAddress, userPort))
    inchat = False
    while True:
        #directly accept udp requests
        data, addr = udp_socket.recvfrom(1024)
        print('Request : ' + data)
        if(data == '!start' and inchat == False):
            reply = 'ok'
            inchat = True
            udp_socket.sendto(reply, (addr[0], addr[1]))
        elif(data == 'ok'):
            print('Chat request accepted...\n')

        elif(data == '!close'):
            inchat = False

        reply = raw_input('--: ')
        udp_socket.sendto(reply, (addr[0], addr[1]))





def chatWithUser(user, userAddress, userPort):

    try:
        # directly send to udp server
        userMessage = '!start'
        while(userMessage != '!close'):
            userMessage = raw_input('--: ')
            udp_socket.sendto(userMessage, (userAddress, userPort))


    except socket.error:
        #Send failed
        print 'Chat error... reloading application'



print (username+', welcome to Smart Chat!\n')
print ('\nConnecting to server...\n')
command = 'register'
registerToServer(command, username, userIpdAddress, userPort)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
thread.start_new_thread(startUpdServer, ())

while 1:
    print ('Please, choose a command from the list:\n'
           '-- !connect <username>\n'
           '-- !reconnect\n'
           '-- !disconnect\n'
           '-- !users\n'
           '-- !get <username>\n'
           '-- !chat\n'
           '-- !help\n'
           '-- !quit\n')
    user_input = raw_input('...waiting for a command: \n')
    if user_input[:9] == "!connect ":
        name = user_input[9:].rstrip()
        retrieveUserIp(name)

    elif user_input == '!connect':
        name = raw_input('Choose an username: ')
        retrieveUserIp(name)

    elif user_input == '!reconnect':
        registerToServer(command, username, userIpdAddress, userPort)

    elif user_input == '!disconnect':
        sendQuitSignal(username)
        print ('Client disconnected from server...\n')
    elif user_input == '!disconnect':
        print ('Closing current chat...\n')
    elif user_input == '!users':
        print ('Users retrieved!\n')
        userList = retrieveUserList()

    elif user_input[:5] == "!get ":
        name = user_input[5:].rstrip()
        retrieveUserInfo(name)
    elif user_input == '!get':
        name = raw_input('Choose an username: ')
        retrieveUserInfo(name)

    elif user_input == '!chat':
        try:
            name = raw_input('Choose an username to start a new chat: ')
            address = raw_input('Ip Address: ')
            port = int(raw_input('Port: '))
            chatWithUser(name, address, port)
        except:
            print ('Error in starting chat...\n')

    elif user_input == '!help':
        printHelpManual()
    elif user_input == '!quit':
        sendQuitSignal(username)
        print ('Quitting client application, come back soon!\n')
        sys.exit()
    else:
        print ('This command does not appear to exit, retry please!\n')




