

base32secret3232 = '7VW5NA46WWYKTWV2GQSH6NZJIZYHYS3T'

import pyotp
import time

totp = pyotp.TOTP('base32secret3232')
totp.now() 
print(totp.now())