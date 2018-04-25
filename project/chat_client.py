
'''
This is the client script of the chat application for Networking course of Cybersecurity Master,
Pisa 2017/2018.
The following code has been entirely developed by me, it's free to use, to modify and to share,
but if you do please credit my Github page https://github.com/BRomans or the project page
https://github.com/BRomans/networking-laboratory

@Author Michele Romani

usage: python chat_client.py <your-ip-address> <udp-port> <username>

'''

import socket
import sys
import thread


'''
Switch the value of the global variable inChat that defines if the client user is chatting or not.
'''

def switchInChat():
    global inChat
    inChat = not inChat
    if inChat:
        print('Swap to chat mode, pres <enter> to continue...\n')
    else:
        print('Swap to command mode, pres <enter> to continue...\n')

'''
Return the value of the global variable inChat
'''
def getInChat():
    global inChat
    return inChat

'''
Set the address and the port of the target user for chat as global variables
'''
def setTargetAddress(address, port):
    global targetAddress
    global targetPort
    targetAddress = address
    targetPort = port

'''
Register to the chat server. This function is automatically called the first time the client is started.
It can be re called with !reconnect command.
'''
def registerToServer(command, username, userIpAddress, userPort):
    global connected
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

'''
Deprecated.
Retrieve the ip address of the specified user. This function utility has been replaced by retrieveUserInfo.
'''
def retrieveUserIp(name):
    try:
        #create an AF_INET, STREAM socket (TCP)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
        sys.exit()
    clientSocket.connect((remote_ip , port))
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

'''
Tells the server that the client user is disconnecting.
'''
def sendQuitSignal(username):
    global connected
    connected = False
    command = 'quit'
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

'''
Retrieve list of online users.
'''
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
        print ('Online Users: ' + reply)
        clientSocket.close()

    except socket.error, msg:
        #Send failed
        print 'Send failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

'''
Retrieve all the info of a specified user. These include username, ip address and udp port.
'''
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
        if reply == 'notFound':
            print ('User ' + name + ' does not exists or is offline...\n')
        else:
            print (name + ' is online...\n')
        clientSocket.close()
        return reply
    except socket.error, msg:
        #Send failed
        print 'Could not connect to user. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        return ''

'''
Print an user manual on screen.
'''
def printHelpManual():
    print ('\n--------------------------------------------------------------------\n'
           '-- Hello, here you are a quick guide for the chat application:    --\n'
           '-- !connect <username> : ask to the server the ip address of      --\n'
           '--    the specified user and then will start a chat with him      --\n'
           '-- !connect : after this command the client will ask the          --\n' 
           '--    username of the user you want to connect                    --\n'
           '-- !reconnect : manually reconnect to the chat server             --\n'
           '-- !disconnect : disconnect from server                           --\n'
           '-- !close : close current chat                                    --\n'
           '-- !users : retrieve users list                                   --\n'
           '-- !get <username> : retrieve infos about the specified user      --\n'
           '-- !chat : send a chat request to the specified user              --\n'
           '-- !quit : close the client application                           --\n'
           '---------------------------------------------------------------------\n')

'''
Starts the udp server of the client, listening for chat messages from other clients. This function is called in a
parallel thread.
'''
def startUpdServer():
    print ('\nListening for chat requests...\n')
    udp_socket.bind(('', userPort))
    commands = ['!start', '!close', '!refuse']
    while True:
        #directly accept udp requests
        try:
            data, addr = udp_socket.recvfrom(1024)
            if not getInChat():
                setTargetAddress(addr[0], addr[1])

            if(getInChat() and data != '' and data not in commands):
                print('\n' + addr[0] + ' : ' + data + '\n')
                print('--: ')

            if(data == '!start'):
                if not getInChat():
                    print ('Chat request from ' + addr[0] + '\n')
                    switchInChat()
                elif getInChat() and targetAddress and addr[0] is not targetAddress:
                    sendChatMessage('!refuse', addr[0], addr[1])
            elif(data == '!close' ):
                print('Ending chat session...\n')
                switchInChat()
            elif (data == '!refuse'):
                print('User is already in another chat, please retry later...\n')
                switchInChat()

        except socket.error:
            pass

'''
Initialize a new chat and switch the client status to inChat.
'''
def initChat(userInfo):
    global targetAddress
    global targetPort
    addressAndPort = userInfo.split('|')
    targetAddress = addressAndPort[1].rstrip()
    targetPort = int(addressAndPort[2].rstrip())
    print('Starting chat with ' + name + ' ' + targetAddress + ' ' + str(targetPort))
    sendChatMessage('!start', targetAddress, targetPort)
    switchInChat()

'''
Send a single message over udp to the specified address.
'''
def sendChatMessage(message, address, port):
    try:
        # directly send to udp server
        userMessage = message
        udp_socket.sendto(userMessage, (address, port))
    except socket.error:
        #Send failed
        print 'Error, could not deliver the message...\n'


'''
Initial setup of the client.
Username, user address and udp port are taken from command line arguments.
The host is set to default to 127.0.0.1. At this time there is not yet a dynamic
configuration of the server address.
When the client starts, it automatically connects to the server and start the
udp socket in a parallel thread.
'''
userIpdAddress = str(sys.argv[1])
userPort = int(sys.argv[2])
username = str(sys.argv[3])
inChat = False
userList = []
global targetAddress
global targetPort
global connected

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

print ('-------------------------------\n'
       + username + ', welcome to Smart Chat!\n'
       + '-------------------------------\n')
print ('\nConnecting to server...\n')
command = 'register'
registerToServer(command, username, userIpdAddress, userPort)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
thread.start_new_thread(startUpdServer, ())


'''
Endless loop that asks the user for commands to perfrom specific actions.
If the state is 'inChat' then every input of the user becomes a chat message
until the chat session is not over.
'''
while 1:
    if not getInChat():
        print ('\n\nPlease, choose a command from the list:\n'
               '-- !connect <username>\n'
               '-- !reconnect\n'
               '-- !disconnect\n'
               '-- !close\n'
               '-- !users\n'
               '-- !get <username>\n'
               '-- !help\n'
               '-- !quit\n')
    user_input = raw_input('--:')

    if getInChat():
        if(user_input == '!close'):
            switchInChat()
        sendChatMessage(user_input, targetAddress, targetPort)

    if user_input[:9] == "!connect ":
        name = user_input[9:].rstrip()
        if name == username:
            print ('You cannot chat with yourself SmartBoy ;) ...\n')
            continue
        try:
            info = retrieveUserInfo(name)
            if info and info != 'notFound' and connected:
               initChat(info)
            else:
                print('Could not start chat...\n')
        except:
            print ('Error in starting chat...\n')
    elif user_input == '!connect':
        name = raw_input('Select user to start chat: ')
        if name == username:
            print ('You cannot chat with yourself SmartBoy ;) ...\n')
            continue
        info = retrieveUserInfo(name)
        if info and info != 'notFound' and connected:
            initChat(info)
        else:
            print('Error in starting chat...\n')

    elif user_input == '!reconnect':
        sendQuitSignal(username)
        print ('Reconnecting to server...\n')
        registerToServer(command, username, userIpdAddress, userPort)

    elif user_input == '!disconnect':
        if connected:
            sendQuitSignal(username)
            print ('Client disconnected from server...\n')
        else:
            print ('Already disconnected...\n')
    elif user_input == '!users':
        if connected:
            print ('Users retrieved!\n')
            userList = retrieveUserList()
        else:
            print ('You must connect to server first...\n')
    elif user_input[:5] == "!get ":
        if connected:
            name = user_input[5:].rstrip()
            retrieveUserInfo(name)
        else:
            print ('You must connect to server first...\n')
    elif user_input == '!get':
        if connected:
            name = raw_input('Choose an username: ')
            retrieveUserInfo(name)
        else:
            print ('You must connect to server first...\n')
    elif user_input == '!help':
        printHelpManual()

    elif user_input == '!quit':
        udp_socket.close()
        sendQuitSignal(username)
        print ('Quitting client application, come back soon!\n')
        sys.exit()

    elif user_input == '':
        continue





