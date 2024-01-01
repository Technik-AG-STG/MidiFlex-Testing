import socket
import threading
import json
import mido
import os

class MidiServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sliders = {}
        self.clients = {}
        self.user_credentials = self.load_user_credentials()  # Load user credentials from "users.json"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
            print(f"Connection established with {addr}")

    def handle_client(self, client_socket):
        try:
            # Perform username and password authentication
            credentials = client_socket.recv(1024).decode('utf-8').split(":")
            username, password = credentials[0], credentials[1]

            if self.authenticate(username, password):
                self.clients[client_socket] = username
                print(f"Authentication successful for {username}")

                # Notify the client about successful authentication
                client_socket.send("authenticated".encode('utf-8'))

                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break

                    if data.startswith(b'SLIDER:'):
                        slider_data = data.split(b':')
                        slider_id = int(slider_data[1])
                        slider_value = int(slider_data[2])

                        # Process the slider value as needed
                        # For simplicity, let's just print the received values
                        if slider_id not in self.sliders:
                            self.sliders[slider_id] = slider_value
                        else:
                            self.sliders[slider_id] = max(0, min(127, slider_value))  # Ensure value is in the valid MIDI range

                        print(f"Slider values sending back: {self.sliders}")

                        # Broadcast slider data to all other clients
                        self.broadcast_slider(data, client_socket)

                    else:
                        self.broadcast(data, client_socket)

            else:
                print("Authentication failed. Closing connection.")
                # Notify the client about failed authentication
                client_socket.send("authentication_failed".encode('utf-8'))

        except ConnectionResetError:
            pass
        finally:
            # Close the client socket and remove it from the list
            client_socket.close()
            if client_socket in self.clients:
                del self.clients[client_socket]

    def broadcast_slider(self, slider_data, sender_socket):
        for client, _ in self.clients.items():
            if client != sender_socket:
                try:
                    client.send(slider_data)
                except socket.error:
                    # Handle errors during send (optional)
                    pass
    
    def authenticate(self, username, password):
        ## print(f"Received credentials: {username}, {password}")
        if username in self.user_credentials and self.user_credentials[username] == password:
            return True
        return False


    def load_user_credentials(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        users_json_path = os.path.join(script_dir, "users.json")

        try:
            with open(users_json_path, "r") as file:
                user_credentials = json.load(file)
                return user_credentials
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading user credentials: {e}")
            return {}


    def broadcast(self, message, sender_socket):
        for client, _ in self.clients.items():
            if client != sender_socket:
                try:
                    received_message = self.parse_midi_message(message)
                    client.send(received_message.encode('utf-8'))
                    print(f"Midi Signal sending back: ", received_message.encode('utf-8'))
                except socket.error:
                    # Handle errors during send (optional)
                    pass

    @staticmethod
    def parse_midi_message(message):
        # Assuming message is a MIDI message in bytes
        try:
            midi_message = mido.Message.from_bytes(message)
            formatted_message = f'note: {midi_message.note}, velocity: {midi_message.velocity}'
            return formatted_message
        except ValueError as e:
            return f"Invalid MIDI data: {e}"

if __name__ == "__main__":
    HOST = "127.0.0.1"  # Change this to your server's IP address or "localhost" for local testing
    PORT = 5050

    midi_server = MidiServer(HOST, PORT)

    try:
        midi_server.start()
    except KeyboardInterrupt:
        print("\nExiting...")