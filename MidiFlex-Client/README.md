# MidiFlex PC Client

This Python script acts as the MidiFlex Client, enabling users to transmit MIDI signals to a server. It establishes a socket connection to the server and authenticates users through a username and password. After successful authentication, users gain the ability to send MIDI notes and slider data, with the server relaying this information to other connected clients.

## Requirements

Before running the script, make sure you have the following:

- Python installed (version 3.8.10)
- mido library installed (pip install mido==1.3.0)

## Usage

1. Clone the repository:

```bash
git clone https://github.com/Technik-AG-STG/MidiFlex-Client.git
cd MidiFlex-Client
```

2. Run the script:

```bash
python client.py
```

3. Enter your username and password as prompted:

4. Upon successful authentication, you can send MIDI signals by entering commands in the format:
- note [note] [velocity] to send a MIDI note
- slider [id] [0-127] to send slider data

Example:

```plaintext
Enter 'note 60 100' or 'slider 1 64':
```

5. To gracefully exit the program, press Ctrl+C.

## Configuration

Modify the HOST and PORT variables in the script to match your server's IP address and port:
```bash
HOST = "127.0.0.1"  # Change this to your server's IP address or "localhost" for local testing
PORT = 5050
```

## Notes

The code leverages the mido library for crafting and dispatching MIDI messages. Ensure that your server is operational and set up with user credentials in the "users.json" file to accept MIDI signals from this client. Feel free to modify and expand the functionality according to your unique requirements. Should you encounter any challenges or have recommendations, kindly raise them by opening an issue on this repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.