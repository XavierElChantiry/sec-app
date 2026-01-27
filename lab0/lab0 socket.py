
import socket # for socket 
import sys 

try: 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # AF_family refers to the addressfamily
    # IPv4. SOCK_STREAM makes the connection TCP
    print ("Socket successfully created")
except socket.error as err: 
    print ("socket creation failed with error %s" %(err))

# default port for socket 
port = 80

try: 
    host_ip = socket.gethostbyname('www.google.com') 
except socket.gaierror: 
    print ("did not resolve host")
    sys.exit() 

# connecting to the server 
s.connect((host_ip, port)) 
# connect to google
s.send(b'GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n')


print ("got data: \n\n")
# print the 200 message because this will work
print(s.recv(12))
print ("\nthe socket has successfully connected to google and sent a get request " "\ntruncated because you just care about the 200")