import socket
# I have improted socket
s = socket.socket()
print ("Socket successfully created")

port = 12345

s.bind(('', port))
print ("socket binded to %s" %(port)) 

s.listen(5)
print ("socket is listening")

# loop until  interrupted
while True: 

  c, addr = s.accept()
  print ('Got connection from', addr )
  # this prints the contents of the message, or atleast the first 400 bytes
  print(c.recv(400))

  c.send('got the message this is your response'.encode()) 

