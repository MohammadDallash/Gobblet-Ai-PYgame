import socket
import struct
import base64

class MultiplayerHelper:
    def __init__(self):
        pass

    def get_ip_address(self, start_port = 1000, end_port=8000):
        try:
            # Create a temporary socket to get the local IP address
            ip_address = socket.gethostbyname(socket.gethostname())

            # Find an available port in the specified range
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for port in range(start_port, end_port + 1):
                try:
                    s.bind((ip_address, port))
                    s.close()
                    return ip_address, port
                except socket.error:
                    pass

            print("Error: Unable to find an available port in the specified range.")
            return None, None
        except Exception as e:
            print(f"Error: {e}")
            return None, None


    def ip_to_room_id(self, ip_address, port):
        try:
            ip_port_tuple = (ip_address, port)
            ip_integer = struct.unpack("!I", socket.inet_aton(ip_port_tuple[0]))[0] << 16
            ip_integer += ip_port_tuple[1]

            # Encode the room ID as hexadecimal string
            room_id_hex = hex(ip_integer)[2:]

            return room_id_hex
        except Exception as e:
            print(f"Error: {e}")
            return None

    def room_id_to_ip(self, room_id_hex):
        try:
            # Convert the hexadecimal string to a 64-bit integer
            room_id = int(room_id_hex, 16)

            # Extract the IP address and port from the 64-bit integer
            ip_integer = room_id >> 16
            port = room_id & 0xFFFF
            ip_address = socket.inet_ntoa(struct.pack("!I", ip_integer))
            return ip_address, port
        except Exception as e:
            print(f"Error: {e}")
            return None