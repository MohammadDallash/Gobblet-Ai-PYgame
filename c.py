import socket

# Define the server address
server_ip = '192.168.40.1'
server_port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))
print(f"Connected to server at {server_ip}:{server_port}")

while True:
    # Send a message to the server
    message = input("Client: ")
    client_socket.send(message.encode())

    # Receive response from the server
    data = client_socket.recv(1024).decode()
    print(f"Server: {data}")

# Close the connection
client_socket.close()
