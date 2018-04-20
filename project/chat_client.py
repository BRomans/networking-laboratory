#handling errors in python socket programs

import socket   #for sockets
import sys  #for exit


userIpdAddress = str(sys.argv[1])
userPort = int(sys.argv[2])
username = str(sys.argv[3])

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

def registerToServer(username, userIpAddress, userPort):
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    clientSocket.connect((remote_ip , port))
    #Send some data to remote server
    connection_message = (username + ' is connecting...\r\n\r\n')
    print ('Socket Connected to ' + host + ' on ip ' + remote_ip)
    try :
        #Set the whole string
        clientSocket.send(username + '|' + userIpAddress+':' + str(userPort))
        #s.sendall(connection_message)
        print 'Connession successful'
        #Now receive data
        reply = clientSocket.recv(4096)
        print ('Server replied: ' + reply)
        clientSocket.close()

    except socket.error, msg:
        #Send failed
        print 'Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]


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

def printHelpManual():
    print ('Hello, here you are a quick guide for the chat application:\n'
           '-- !connect <username> : ask to the server the ip address of the specified user and then will start a chat with him\n'
           '-- !connect : after this command the client will ask the username of the user you want to connect\n'
           '-- !disconnect : close the current chat\n'
           '-- !quit : close the client application\n')

print (username+',\n')
print ('\nwelcome to Smart Chat!\n')
print ('\nConnecting to server...\n')
registerToServer(username, userIpdAddress, userPort)

while 1:
    print ('Choose a command from the list:\n'
           '-- !connect <username>\n'
           '-- !disconnect\n'
           '-- !help\n'
           '-- !quit\n')
    user_input = raw_input('...waiting for a command: \n')
    if user_input[:9] == "!connect ":
        name = user_input[9:].rstrip()
        retrieveUserIp(name)

    elif user_input == '!connect':
        name = raw_input('Choose an username: ')
        retrieveUserIp(name)

    elif user_input == '!disconnect':
        print 'DISCONNECT'
    elif user_input == '!help':
        printHelpManual()
    elif user_input == '!quit':
        print ('Quitting client application, come back soon!...\n')
        sys.exit()
    else:
        print ('This command does not appear to exit, retry please!\n')




