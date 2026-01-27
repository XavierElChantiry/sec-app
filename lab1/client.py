import socket

s = socket.socket()

port = 12345
#this initates the connection
s.connect(('127.0.0.1', port)) 

#this is sssssssssssssssssuper basic at the moment
x = input('Enter your name:  ')
print('type something contaning the word "exit" to break conection')
# HELLO| needed to decalre username
s.send(("HELLO|" + x).encode())
print (s.recv(1024).decode())
while True:
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
