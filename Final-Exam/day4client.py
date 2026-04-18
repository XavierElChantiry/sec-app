import socket
from cryptography.fernet import Fernet

from day1portscan import port_scan
from day3steg import extract_hidden
from Authenticator import authenticator_code
import json

def load_user_db(filepath="users.json"):

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{filepath} not found.")
        return {}

def cleint(user, pw, key):
    if not port_scan('127.0.0.1', 4726):
        print("port not open")
        return
    
    hidden_text = extract_hidden("evidence.png")

    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(hidden_text.encode('utf-8'))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 4726))
    #this is here because port scan takes time so TOTP might expire
    otp = input("Enter your one time passcode [blank will not work if 'or' commented]: ") or authenticator_code(user_input)
    auth_string = f"{user},{pw},{otp}"
    print("attempting to connect now")
    client_socket.send(auth_string.encode())

    response = client_socket.recv(1024).decode()
    if response == "Accepted, wainting for payload":
        print(f"Sending payload now. Received: `{response}`")
        client_socket.send(encrypted_bytes) 
    else:
        print(f"Authentication Failed. Received: `{response}`")

    client_socket.close()
    

if __name__ == "__main__":
    user_input = input("Enter your name [Default: guest]: ") or "guest"
    pw_input = input("Enter your password [Default: guest]: ") or "guest"
    user_db = load_user_db()
    key = user_db[user_input]["fernet_key"]
    print(user_input, pw_input, key)


    cleint(user_input, pw_input, key)

