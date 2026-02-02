import socket
import hashlib
import pyotp

s = socket.socket()
port = 12345
#this initates the connection
s.connect(('127.0.0.1', port)) 

def password_auth():
    while True:
        try:
            pw = input("password: ")
            s.send(hashlib.sha256(pw.encode()).digest())
            pw_res = s.recv(1024).decode()
            if pw_res.startswith("OTP"):
                return True
            print(pw_res)
        except:
            print("authentication failed")
            return False

def OTP_auth():
    while True:
        try:
            pw = input("OTP code: ")
            s.send(pw.encode())
            pw_res = s.recv(1024).decode()
            if pw_res.startswith("OTP code accepted"):
                print(pw_res)
                return True
            print(pw_res)
        except:
            print("authentication failed")
            return False

#this is sssssssssssssssssuper basic at the moment
x = input('Enter your name:  ')
print('type something contaning the word "exit" to break conection')
# HELLO| needed to decalre username
s.send(("HELLO|" + x).encode())
print (s.recv(1024).decode())
opt_authenticated = False
authenticated = password_auth()
if authenticated:
    opt_authenticated = OTP_auth()


while opt_authenticated:
    try: 
        #MSG| needed for messaging
        input_str = ("MSG|" + input()).encode()
        if "exit" in input_str.decode():
            # this is to exit
            s.send(b"EXIT|")
            print (s.recv(1024).decode())
            s.close()
            break
        s.send(input_str)
        #this prints the response
        print (s.recv(1024).decode())
    except:
        print("connection broken")
        s.close()
        break
