import socket,threading
import sys

# handle messages from server
def handle_server_message(connSocket):
    while True:
        try:
            message = connSocket.recv(1024)
            if not message:
                print("close connection to server")
                break
            print(message.decode())
        except:
            print(connSocket, "error received from server")
            break
    connSocket.close()
        
    
# connect to server
#s = socket.socket()
HOST = socket.gethostbyname('localhost')
PORT = 6789
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))

# start a new thread to receive message
threading.Thread(target = handle_server_message, args = (clientSocket,)).start()

while True:
    # input something and send it to server
    try:
        inputMessage = input()
        clientSocket.send(inputMessage.encode())
        print("You: "+inputMessage)
        # handle exit
        if inputMessage=='exit':
            print('Exiting')
            break
    except:
        print("error from client")
        break


