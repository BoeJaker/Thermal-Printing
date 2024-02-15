import socket
import argparse
parser = argparse.ArgumentParser(description="A simple command-line tool")

# Add arguments
parser.add_argument("-t", "--text", type=str, help="Specify your name")

# Parse the command-line arguments
args = parser.parse_args()

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode())

host = "192.168.3.201"
port = 9999
message = args.text

send_message(host, port, message)
