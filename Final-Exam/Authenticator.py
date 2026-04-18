
import pyotp
import json
def load_user_db(filepath="users.json"):

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{filepath} not found.")
        return {}

def authenticator_code(username):
    users = load_user_db()

    user_data = users[username]

    totp = pyotp.TOTP(user_data['totp_secret'])
    # print(user_data['totp_secret'])
    print(totp.now())
    return totp.now() 

if __name__ == "__main__":
    authenticator_code("admin")