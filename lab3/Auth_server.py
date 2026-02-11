
# i will be cleaning this up into functions if i need to build on this next week
import socket
import pyotp
# import crypt
# I have improted socket

#this will be moved to a external file if we have to touch this section again
# i know its not secure at all

auth_dict = {
  "mike": b'\x1a\xa4\xf3\xd6\xea[L\x93\x05\xa7\xef\xe7\xd0k1\xe9v1w\x11\x9a\xfb\x06\x04\xa27\xdd\x7f\xa3n}\x82', # Ford
  "mini": b'\xca\x97\x81\x12\xca\x1b\xbd\xca\xfa\xc21\xb3\x9a#\xdcM\xa7\x86\xef\xf8\x14|Nr\xb9\x80w\x85\xaf\xeeH\xbb', # a
  "xav": b'y\x02i\x9b\xe4,\x8a\x8eF\xfb\xbbE\x01re\x17\xe8k"\xc5j\x18\x9fv%\xa6\xdaI\x08\x1b$Q' # 7
}
base32secret3232 = '7VW5NA46WWYKTWV2GQSH6NZJIZYHYS3T'



port = 12345
s = socket.socket()
print ("Socket successfully created")

def chat_function():
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

def pw_authentication(counter):
    try:
        while counter > 0 :
            pw = c.recv(1042)
            if pw == auth_dict[username]:
                c.send(("OTP code please " + username).encode())
                print("user authenticated")
                return True
            else:
                print("user not authenticated")
                c.send(("Username or password is incorrect. try again").encode())
                counter -= 1
        return False
    except Exception as error:
        print(error)
        print("username does not exist")
        return False


def OTP_auth():
    opt_counter = 4
    try:
        while opt_counter > 0:
            totp = pyotp.TOTP('base32secret3232')
            totp.now()
            OTP = c.recv(1042).decode()
            if totp.verify(OTP):
                c.send(("OTP code accepted " + username).encode())
                print("user authenticated")
                return True
            else:
                print("user not authenticated")
                c.send(("OTP incorrect").encode())
                opt_counter -= 1
    except Exception as error:
        print(error)
        print("something odd has occured")
        return False


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
        c.send(("hello " + username + " password please").encode())
        print("connected to " + username)

        counter = 7


        # start taking messages from client
        if pw_authentication(counter) and OTP_auth():
            chat_function()
        else:
            c.send("ERROR|something broke".encode())
        c.close()

 # if client does not say hello they get disconnected
    else:
        print("client did not say hello, and therefore was rejected")
        c.send(("ERROR|i did not get a hello how rude. good day and good bye").encode())
        c.close()