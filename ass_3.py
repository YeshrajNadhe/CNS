def encrypt(text, key):
    res = ""
    text = text[::-1]
    for ch in text:
        val = ord(ch)
        val = val ^ key
        val = (val + (key % 10)) % 256
        res += chr(val)
    return res


def decrypt(cipher, key):
    res = ""
    for ch in cipher:
        val = ord(ch)
        val = (val - (key % 10)) % 256
        val = val ^ key
        res += chr(val)
    return res[::-1]

print("Encryption & Decryption Program ")
choice = input("Enter E for Encrypt or D for Decrypt: ").upper()
key = int(input("Enter key: "))

if choice == 'E':
    msg = input("Enter message: ")
    enc = encrypt(msg, key)
    print("Encrypted:", enc)
elif choice == 'D':
    msg = input("Enter encrypted text: ")
    dec = decrypt(msg, key)
    print("Decrypted:", dec)
else:
    print("Invalid choice")
