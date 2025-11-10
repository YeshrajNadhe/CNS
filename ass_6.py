def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    for i in range(1, phi):
        if (e * i) % phi == 1:
            return i
    return None

def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

def simple_hash(msg):
    return sum(ord(c) for c in msg) % 100

def main():
    print("=== Simple RSA Digital Signature Demo (educational) ===\n")
    while True:
        try:
            p = int(input("Enter prime number p (>5): ").strip())
            q = int(input("Enter prime number q (>5): ").strip())
            if p <= 5 or q <= 5:
                print("Please enter primes > 5.")
                continue
            break
        except ValueError:
            print("Enter valid integers.")
    n = p * q
    phi = (p - 1) * (q - 1)
    print(f"\nComputed: n = {n}, phi = {phi}")
    while True:
        try:
            e = int(input("Enter public exponent e (1 < e < phi, gcd(e,phi)=1): ").strip())
            if e <= 1 or e >= phi:
                print("e must satisfy 1 < e < phi.")
                continue
            if gcd(e, phi) != 1:
                print("gcd(e, phi) != 1. Choose different e.")
                continue
            break
        except ValueError:
            print("Enter a valid integer for e.")
    d = mod_inverse(e, phi)
    if d is None:
        print("Could not compute modular inverse d with this phi/e (unexpected). Exiting.")
        return
    print(f"Computed private exponent d = {d}")
    message = input("\nEnter message (plain text): ")
    hash_value = simple_hash(message)
    print(f"\nMessage Hash Value (simpleHash): {hash_value}")
    signature = mod_exp(hash_value, d, n)
    print(f"Digital Signature (using sender's private key d): {signature}")
    cipher = []
    print("\nEncrypting message (character-wise) using public key (e,n):")
    for ch in message:
        c = mod_exp(ord(ch), e, n)
        cipher.append(c)
    print("Ciphertext (numbers):")
    print(' '.join(str(x) for x in cipher))
    decrypted_chars = []
    for c in cipher:
        m = mod_exp(c, d, n)
        decrypted_chars.append(chr(m))
    decrypted = ''.join(decrypted_chars)
    print("\nDecrypted message (receiver reconstructs):")
    print(decrypted)
    print("\nVerifying digital signature:")
    verify_hash = mod_exp(signature, e, n)
    receiver_hash = simple_hash(decrypted)
    print(f"Decrypted Signature -> recovered hash: {verify_hash}")
    print(f"Receiver computed hash (from decrypted message): {receiver_hash}")
    if verify_hash == receiver_hash:
        print("\nSignature Verified! Message is authentic and intact.")
    else:
        print("\nVerification Failed! Message altered or signature invalid.")

if __name__ == "__main__":
    main()

