import socket
from cryptography.fernet import Fernet
from day2mfa import authenticate

def server():
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows immediate reuse of the port after the script stops
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind(('127.0.0.1', 4726))
    ss.listen(5)
    
    print("waiting for connection")

    while True:
        try:
            conn, addr = ss.accept()
            print(f"connected to {addr}") 

            try: 
                print("here")
                auth_data = conn.recv(1024).decode().split(',')
                
                if len(auth_data) < 3:
                    conn.close()
                    #this is to handle the scanning
                    continue

                user, pw, otp = auth_data[0], auth_data[1], auth_data[2]
                authetications_status, key = authenticate(user, pw, otp)
                
                if authetications_status:
                    conn.send(b"Accepted, wainting for payload")

                    payload = conn.recv(4096)

                    f = Fernet(key)
                    message = f.decrypt(payload)

                    print(f" the message is {message}")
                    with open("received_message.txt", "wb") as f_out:
                        f_out.write(message)
                    conn.close()

                else:
                    conn.send(b"bad auth sorry")
                    conn.close()

            except Exception as e:
                print(f"something went awry: {e}")
                conn.close()
        
        except KeyboardInterrupt:
            print("\nShutting down server.")
            break

    ss.close()

if __name__ == "__main__":
    server()