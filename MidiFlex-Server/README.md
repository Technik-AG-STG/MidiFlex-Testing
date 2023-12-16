# MidiFlex Server

This Python script acts as the MidiFlex Server, allowing multiple clients to connect and exchange MIDI signals. Clients can authenticate using a username and password, after which they can send MIDI notes, slider data, and receive broadcasted MIDI signals from other connected clients.

## Requirements

Before running the server script, ensure you have the following:

- Python installed (version 3.8.10)
- mido library installed (pip install mido==1.3.0)

## Configuration

1. Modify the HOST and PORT variables in the script to set the server's IP address and port:

```bash
HOST = "127.0.0.1"  # Change this to your server's IP address or "localhost" for local testing
PORT = 5050
```

2. User Authentication

User credentials are loaded from a file named "users.json." Ensure the file is present and correctly formatted with username-password pairs:

```json
{
  "user1": "password1",
  "user2": "password2",
  "user3": "password3"
}
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/Technik-AG-STG/MidiFlex-Server.git
cd MidiFlex-Server
```

2. Run the server script:

```bash
python server.py
```

Clients can connect to the server using the client scripts on the other Github Repositories.

## Server Features

- Authentication: Clients must provide a valid username and password to connect to the server.
- MIDI Message Broadcasting: Clients can send MIDI messages, and the server broadcasts these messages to other connected clients.

## Note

The server uses the mido library to parse and format MIDI messages.
If you encounter any issues or have suggestions, please open an issue on this repository.
Feel free to customize and extend the server's functionality based on your specific use case.

## License

This project is licensed under the MIT License - see the LICENSE file for details.