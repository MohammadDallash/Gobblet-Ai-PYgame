import socket

# Define the server address
server_ip = '192.168.40.1'
server_port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server listening on {server_ip}:{server_port}")

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

while True:
    # Receive data from the client
    data = client_socket.recv(1024).decode()
    if not data:
        break  # Break the loop if no data received (client disconnected)
    
    print(f"Client: {data}")

    # Send a response to the client
    message = input("Server: ")
    client_socket.send(message.encode())

# Close the connection
client_socket.close()
server_socket.close()
