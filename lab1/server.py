
# i will be cleaning this up into functions if i need to build on this next week
import socket
# I have improted socket
s = socket.socket()
print ("Socket successfully created")

port = 12345

s.bind(('', port))
print ("socket binded to %s" %(port)) 
s.listen(5)
print ("socket is listening")

while True: 
  c, addr = s.accept()
  print ('Got connection from', addr )

  #take in username
  inital_response = c.recv(1042).decode()
  if inital_response.startswith("HELLO|"):
    username = inital_response[6:]
    c.send(("hello " + username + " we are now connected").encode())
    print("connected to " + username)
    # start taking messages from client
    while True: 
      try:
        return_string = c.recv(1042).decode()
        if return_string.startswith("MSG|"):
          # check there is content
          if return_string[4:] == "":
            c.send(("try sending some content that has content").encode())
            print("empty message sent")

          # keyboard interrupts are diabled because of blocking operation soo this is one way to close server without closing client
          # yes i am leaving this in for now
          elif return_string[4:] == "die with grace":
            c.send(("thanks "+ username + " turning off").encode())
            c.close()
            exit()  
          else:
            print(return_string)
            c.send(("thanks "+ username + " i got your message").encode()) 
        # breaks TCP connection
        elif return_string == "EXIT|":
          c.send(("goodbye " + username).encode())
          c.close()
          print(f"Disconnected from {username}. waiting for new connection")
          break
        # catch all for misfomated 
        else:
          print("\n\rsomething is wrong with the format of " + return_string)
          print("its probably a request longer than what can be processed or command was misformated")
          c.send(b'you found an edge case')
          c.close()

      except Exception as error:
        print(error)
        print( "client connection broken" )
        # restated here because exit gets caught by try catch
        if return_string[4:] == "die with grace":
          c.close()
          exit()
        c.close()
        break
      
 # if client does not say hello they get disconnected
  else:
    print("client did not say hello, and therefore was rejected")
    c.send(("ERROR|i did not get a hello how rude. good day and good bye").encode())
    c.close()


