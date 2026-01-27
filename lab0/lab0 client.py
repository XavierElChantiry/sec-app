
import socket
s = socket.socket()
port = 12345
#this initates the connection
s.connect(('127.0.0.1', port)) 
# this sends hats are cool as a bytestring
s.send(b"hats are cool")
#this prints the response
print (s.recv(1024).decode())
# close the connection 
s.close()

("hello").encode()