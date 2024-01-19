import socket
import struct
import base64

def get_ip_address(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', port))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error: {e}")
        return None

def ip_to_room_id(ip_address, port):
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

def room_id_to_ip(room_id_hex):
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

# Example usage:
ip_address = get_ip_address(port=1000)
if ip_address:
    room_id_hex = ip_to_room_id(ip_address, port=1000)
    print(f"IP Address: {ip_address}")
    print(f"Room ID (Shortened): {room_id_hex}")

    original_ip_address, original_port = room_id_to_ip(room_id_hex)
    if original_ip_address is not None and original_port is not None:
        print(f"Original IP Address: {original_ip_address}")
        print(f"Original Port: {original_port}")
