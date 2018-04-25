
'''
This is the server script of the chat application for Networking course of Cybersecurity Master,
Pisa 2017/2018.
The following code has been entirely developed by me, it's free to use, to modify and to share,
but if you do please credit my Github page https://github.com/BRomans or the project page
https://github.com/BRomans/networking-laboratory

@Author Michele Romani

usage: python chat_cserver.py

'''

import socket
import sys
import thread


'''
This function is launched in a parallel thread and manages all commands received by one or more clients.
A command is followed by '>' by convention. It is therefore possible to misslead the server if the command
sent from client does not follow this convention.
'''
def clientThread(conn):

    data = conn.recv(1024)
    dataParseCommand = data.split('>')
    command = dataParseCommand[0]
    print('Received <' + command +'> command...\n')

    if(command == 'register'):
        print('Register procedure started...\n')
        reply = loginUser(dataParseCommand[1])
        conn.sendall(reply)
    if(command == 'quit'):
        print('Quit procedure started...\n')
        reply = removeUser(dataParseCommand[1].split('|')[0])
        conn.sendall(reply)
    if(command == 'getUser'):
        reply = getExistingUser(dataParseCommand[1].split('|')[0])
        conn.sendall(reply)
    if(command == 'userList'):
        reply = userList()
        conn.sendall(reply)
    conn.close()

'''
This function try to login the user who requested into the server dictionary. If another user is already present with
the same nicnkame, it returns an error message.
'''
def loginUser(data):
    dataParseName = data.split('|')
    username = dataParseName[0]
    dataParseAddress = dataParseName[1].split(':')
    userIpAddr = dataParseAddress[0]
    userPort = dataParseAddress[1]
    if not (checkExistingUserName(username)):
        addNewUser(username, userIpAddr, userPort)
        print (' -- User successfully registered --\n'
           ' -- Username: ' + username + ' --\n'
           ' -- Ip Address: ' + userIpAddr + ' --\n'
           ' -- Ip Port: ' + userPort + ' --\n')
        return username + ', you correctly joined our chat!\n'
    else:
        return 'ERROR | User <' + username + '> already exists, please choose a different nickname'

'''
Add a new user to the dictionary
'''
def addNewUser(name, address, port):
    activeUsers[name] = [address, port]
    print ('User registered, updating dictionary...', activeUsers)

'''
Get an user from dictionary or return a notFound error if it is not present.
'''
def getExistingUser(name):
    if(checkExistingUserName(name)):
        print ('Retrieving user <' + name + '>...')
        address = activeUsers.get(name)[0]
        port = activeUsers.get(name)[1]
        return name + ' | ' + address + ' | ' + port
    else:
        return ('notFound')
'''
Checks the presence of a user in the dictionary before adding it.
'''
def checkExistingUserName(name):
    print ('Checking if user <' + name + '> is already registered...')
    return activeUsers.get(name) is not None and len(activeUsers.get(name)) > 0

'''
Return the list of all online users. Users that did not disconnet in the proper way are considered online.
'''
def userList():
    print ('Retrieving registered users...')
    userList = activeUsers.keys()
    userListFlat = ''
    for user in userList:
        userListFlat += user + ' - '
    return userListFlat

'''
After a !disconnect command from client, removes the corresponding user from dictionary, if present.
'''
def removeUser(name):
    print ('Removing user <' + name +'>...')
    if activeUsers.get(name):
        activeUsers.pop(name)
    print ('User removed, updating dictionary...', activeUsers)
    return ('See you soon, ' + name + '...')


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

#This does not have a chat client, its purpose is for testing the dictionary
activeUsers = dict([('DummyUser', ['0.0.0.0', '8080'])])
print ('Init dictionary : ', activeUsers)

#Init the server socket
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

#Infinite loop waiting for new connections from clients
while 1:
    #wait to accept a connection - blocking call
    print 'Waiting for users to open a connection...\n'
     #wait to accept a connection - blocking call
    conn, addr = s.accept()
    try:
        thread.start_new_thread(clientThread, (conn,))
        print ('Receiving registration from: ' + addr[0] + ':' + str(addr[1])+'\n')
    except thread.error, msg:
        print 'Connection failed. Error Code : '  + str(msg[0]) + ' Message ' + msg[1]

s.close()
