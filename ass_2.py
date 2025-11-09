import time
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
# Function to find gcd
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(e, phi):
    for d in range(1, phi):
        if (d * e) % phi == 1:
            return d
    return None

# Function for modular exponentiation
def modexp(base, exp, mod):
    return pow(base, exp, mod)

print("RSA Key Generation, Encryption & Decryption \n")

start_time = time.time()

while True:
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))
    if is_prime(p) and is_prime(q):
        break
    else:
        print("Both p and q must be PRIME numbers! Try again.\n")
n = p * q
phi = (p - 1) * (q - 1)

# Input e and check gcd(e, phi) = 1
e = int(input("Enter e (coprime with phi): "))
while gcd(e, phi) != 1:
    e = int(input("Invalid e! Enter another value: "))

# Compute private key d
d = modinv(e, phi)
key_gen_time = time.time() - start_time

print(f"\nPublic key: (e={e}, n={n})")
print(f"Private key: (d={d}, n={n})")
print(f"Key Generation Time: {key_gen_time:.6f} seconds")

# Encryption
m = int(input("\nEnter number to encrypt: "))
start_enc = time.time()
c = modexp(m, e, n)
enc_time = time.time() - start_enc
print(f"Ciphertext: {c}")
print(f"Encryption Time: {enc_time:.6f} seconds")

# Decryption
start_dec = time.time()
m_dec = modexp(c, d, n)
dec_time = time.time() - start_dec
print(f"Decrypted Message: {m_dec}")
print(f"Decryption Time: {dec_time:.6f} seconds")

