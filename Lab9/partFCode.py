import hashlib

# the pin is 1234

target_hash = "81dc9bdb52d04dc20036dbd8313ed055"

print("Starting Brute Force Attack...")

# --- STUDENT TODO: COMPLETE THE LOGIC BELOW ---

# 1. Create a loop that goes from 0 to 9999
# 2. Use str(i).zfill(4) to ensure numbers like 7 become "0007"
# 3. Hash the string using hashlib.md5()
# 4. Compare the result to the target_hash
# 5. Print the PIN if you find a match

# YOUR CODE HERE:
for i in range(10000):
    pin = str(i).zfill(4)
    brute = hashlib.md5(pin.encode()).hexdigest()
    if brute == target_hash:
        print(i, "is the pin")
        break


# --- END TODO ---