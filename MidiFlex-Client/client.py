import socket
import mido
import threading

def send_midi_message(note, velocity, server_socket):
    message = [0x90, note, velocity]  # Assuming Note On message (status byte 0x90)
    bytes_message = bytes(message)
    server_socket.send(bytes_message)

def receive_midi_messages(server_socket):
    while True:
        try:
            data = server_socket.recv(1024)
            if not data:
                break

            received_message = data.decode('utf-8')
            print(f"Received MIDI message: {received_message}")

        except ConnectionResetError:
            break

if __name__ == "__main__":
    HOST = "127.0.0.1"  # Change this to your server's IP address or "localhost" for local testing
    PORT = 5050

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        # Perform username and password input
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Send authentication details to the server
        client_socket.send(f"{username}:{password}".encode('utf-8'))

        # Wait for the server's authentication result
        authentication_result = client_socket.recv(1024).decode('utf-8')

        if authentication_result == "authenticated":
            print("Authentication successful. You can now send MIDI signals.")

            receive_thread = threading.Thread(target=receive_midi_messages, args=(client_socket,))
            receive_thread.start()

            while True:
                try:
                    user_input = input("Enter 'note [note] [0-127]' or 'slider [id] [0-127]': ")

                    if user_input.startswith('slider'):
                        slider_data = user_input.split(' ')
                        if len(slider_data) == 3:
                            slider_id = int(slider_data[1])
                            slider_value = int(slider_data[2])

                            if 0 <= slider_value <= 127:
                                # Send slider data in a custom format
                                client_socket.send(f"SLIDER:{slider_id}:{slider_value}".encode('utf-8'))
                            else:
                                print("Slider value must be in the range 0-127. Try again.")
                        else:
                            print("Invalid slider input. Format: 'slider [id] [0-127]'")

                    elif user_input.startswith('note'):
                        note_velocity = user_input.split(' ')[1:]
                        if len(note_velocity) == 2:
                            note, velocity = map(int, note_velocity)
                            if 0 <= note <= 127 and 0 <= velocity <= 127:
                                # Send MIDI message to the server
                                send_midi_message(note, velocity, client_socket)
                            else:
                                print("Note and velocity must be in the range 0-127. Try again.")
                        else:
                            print("Invalid 'note' input. Format: 'note [0-127] [0-127]'")

                    else:
                        print("Invalid input. Try again.")

                except KeyboardInterrupt:
                    # Handle Ctrl+C to gracefully exit the program
                    print("\nExiting...")
                    client_socket.close()
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}")

        else:
            print("Authentication failed. Exiting.")
            client_socket.close()

    except ConnectionResetError:
        print("Connection to the server was reset. Exiting.")
        client_socket.close()