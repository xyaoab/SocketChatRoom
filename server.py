import socket,threading
import time


#conn is client itself
def broadcast(msg, conn):
	#broadcast the message to other clients except the client who sent it
	# exclude it self 
    for socket in listofclients:
        if socket != conn:
            try:
                socket.send(msg)
            except:
                #broken socket ended by ctrl+c
                print('[Error]Broken socket ', socket, ' closing connection!')
                socket.close()
                remove(socket)

def remove(conn):
	#remove connection if the user wants to exit or the connection is interrupted
    if conn in listofclients:
        listofclients.remove(conn)

# handle new clients
def handle_client(connSocket, addr):
    # handle messages from clients
    # you need to add more details to make it support broadcast message to all clients
    name = connSocket.recv(1024)
    name = name.decode()
    #send welcome message
    welcome = 'Welcome %s! If you ever want to quit, type "exit" to exit.' % name
    msg = "%s has joined the chat!" % name
    try:
        connSocket.send(welcome.encode())
        broadcast(msg.encode(),connSocket)
    except:
        print("no response, closing connection from ", connSocket)
        connSocket.close()
        remove(connSocket)
        return

    while True:
        # receive message and print it
        try:
            message = connSocket.recv(1024)
            #accidentally lose connection -ctrl-c
            if not message:
                print("No message from ",name)
                print("%s will be removed from the chatroom" %name)
                break
            # handle exit
            if message.decode()=='exit':
                #connSocket.send(message)
                msg = name + ' has left the chat.'  
                print(msg)
                connSocket.close()
                remove(connSocket)
                broadcast(msg.encode(),connSocket)
                break
            # to broadcast msg to other clients that
            msg = name +': '+ message.decode()
            print(msg)
            broadcast(msg.encode(),connSocket)
        except:
            print("no response, closing connection from ", connSocket)
            break
    connSocket.close()
    remove(connSocket)


# setup server
PORT = 6789
HOST = socket.gethostbyname('localhost')
listofclients=[]
serverAddr = (HOST, PORT)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(serverAddr)

# start listen
serverSocket.listen()
print('Server is listening at ',HOST,PORT)
        
while True:
    try:
        # when there is a new connection, pass it to a new thread to handle, then continue to listen
        connSocket,addr = serverSocket.accept()
        print('Served connnected by ',addr)
        #invite the user to type in their name(optional)
        try:
            connSocket.sendall("Welcome to this chatroom! Now type your name and press enter!".encode())
        except:
            print('[Error] sending msg from server to client ', addr)
            break
        
        #append new connection client
        listofclients.append(connSocket)
        #start a thread to handle client request  
        threading.Thread(target = handle_client, args = (connSocket, addr,)).start()
    except:
        print('[Error]accidentally exit from ', addr)
        break
remove(connSocket)
connSocket.close()
        

    

    
