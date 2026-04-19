import socket
from cryptography.fernet import Fernet
import hashlib

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

def cleint(user, pw):
    if not port_scan('127.0.0.1', 4726):
        print("port not open")
        return
    

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 4726))

    # i would lke to move this to after the authenticate but i will follow what is written 
    user_db = load_user_db()
    key = user_db[user_input]["fernet_key"]
    fernet = Fernet(key)
    hidden_text = extract_hidden("evidence.png")
    encrypted_bytes = fernet.encrypt(hidden_text.encode('utf-8'))

    #this is here because port scan takes time so TOTP might expire
    # otp = input("Enter your one time passcode [blank will not work if 'or' commented]: ") or authenticator_code(user_input)
    otp = input("Enter OTP")
    hash_pw = hashlib.sha256(pw.encode()).hexdigest()
    auth_string = f"{user},{hash_pw},{otp}"
    print("attempting to connect now")
    client_socket.send(auth_string.encode())

    response = client_socket.recv(1024).decode()
    if response == "Accepted, wainting for payload":
        client_socket.send(encrypted_bytes) 
        print(f"Sending payload now. Received: `{response}`")
    else:
        print(f"Authentication Failed. Received: `{response}`")

    client_socket.close()
    

if __name__ == "__main__":
    # user_input = input("Enter your name [Default: guest]: ") or "guest"
    # pw_input = input("Enter your password [Default: guest]: ") or "guest"
    user_input = input("enter Username")
    pw_input = input("Enter your password")



    cleint(user_input, pw_input)

