

base32secret3232 = 'JBSWY3DPEHPK3PXP'

import pyotp

totp = pyotp.TOTP('base32secret3232')
totp.now() 
print(totp.now())