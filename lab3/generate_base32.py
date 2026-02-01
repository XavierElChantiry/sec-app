import pyotp

base32_secret = pyotp.random_base32()

print(base32_secret)
