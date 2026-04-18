import hashlib
import pyotp
import json
import os


def load_user_db(filepath="users.json"):

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{filepath} not found.")
        return {}


def authenticate(username, input_password, input_token):
    users = load_user_db()
    # i just realized things like rate limiting are optional sooooo i am going to go with they have one chance and thats it
    
    if username not in users:
        print(f"User '{username}' does not exist.")
        return False

    user_data = users[username]

    salt = bytes.fromhex(user_data['salt'])
    expected_hash = user_data['hash']
    
    input_hash = hashlib.sha256(salt + input_password.encode()).hexdigest()
    pw_success = (input_hash == expected_hash)
    # print(pw_success)

    totp = pyotp.TOTP(user_data['totp_secret'])
    totp.now() 
    # print(totp.now())
    # print(input_token)
    otp_success = totp.verify(input_token)

    # Final Policy Check
    if pw_success and otp_success:
        print(f"{username} Access Granted.")
        return True, user_data["fernet_key"]
    else:
        print("Incorrect Password or TOTP token")
        return False, "null"



if __name__ == "__main__":
    # c = authenticate("agent", "agent", 558627)
    # c = authenticate("mike", "mike", 556581)
    c, f = authenticate("admin", "password1", 732403)
    print(c, f)