import socket
import sys



def host_game(host='localhost',port=9999):
    while(True):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(1)

        client, addr = server.accept()

        data = client.recv(1024)
        if(data.decode('utf-8') == "end"):
            server.close()
            return

        print(f"server received : {data.decode('utf-8')}")
        print("server send : ")
        move = input()
        client.send(move.encode('utf-8'))


def connect_to_game(host='localhost',port=9999):
    while(True):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        print(f"client send:")
        move = input()
        client.send(move.encode('utf-8'))
        data = client.recv(1024)
        print(f"client recieved: {data.decode('utf-8')}")
        


# if(sys.argv[1]=='c'):
#     connect_to_game()
# elif(sys.argv[1]=='s'):
#     host_game()







