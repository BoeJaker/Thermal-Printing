import socket
import threading

import subprocess

# Define host and port for the server
host = "0.0.0.0"
port = 9999
usb_interface="lp0"

def wrap_text(text, line_length):
    wrapped_text = ""
    current_line = ""
    words = text.split()
    for word in words:
        if len(current_line) + len(word) <= line_length:
            current_line += word + " "
        else:
            wrapped_text += current_line.strip() + "\n"
            current_line = word + " "
    if current_line:
        wrapped_text += current_line.strip()
    return wrapped_text+"\x0A"

def print_to_usb_thermal_printer(text):
    try:
        # Wrap the text to fit the line length of the thermal printer
        wrapped_text = wrap_text(text, 32)  # Adjust line length as needed
        print(wrapped_text)
        # Open a pipe to /dev/usb/lp0 and write the text
        with subprocess.Popen(['tee', '/dev/usb/'+usb_interface], stdin=subprocess.PIPE) as proc:
            proc.communicate(input=wrapped_text.encode('utf-8'))
        print("Text printed successfully to USB thermal printer.")
    except subprocess.CalledProcessError as e:
        print("Error printing to USB thermal printer:", e)

def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break

        # Decode the received data (assuming UTF-8 encoding)
        message = data.decode("utf-8")
        print("Received:", message)
        print_to_usb_thermal_printer(message)

        # Echo back the received message to the client
        # client_socket.sendall(data)

    # Close the client socket when the connection is terminated
    client_socket.close()

def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Start listening for incoming connections
    server_socket.listen(5)
    print("Server listening on {}:{}".format(host, port))

    try:
        while True:
            # Accept incoming connections
            client_socket, client_address = server_socket.accept()
            print("Accepted connection from {}:{}".format(client_address[0], client_address[1]))

            # Handle each client connection in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()

if __name__ == "__main__":
    main()
