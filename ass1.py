import random

def caesar_cipher(text, key, mode):
    res = ""
    if mode == 'd':
        key = -key
    for ch in text:
        if ch.isalpha():
            base = 'A' if ch.isupper() else 'a'
            res += chr((ord(ch) - ord(base) + key) % 26 + ord(base))
        else:
            res += ch
    return res

def vigenere_cipher(text, key, mode):
    res = ""
    key = key.upper()
    j = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[j % len(key)]) - ord('A')
            if mode == 'd':
                shift = -shift
            base = 'A' if ch.isupper() else 'a'
            res += chr((ord(ch) - ord(base) + shift) % 26 + ord(base))
            j += 1
        else:
            res += ch
    return res

def vernam_cipher(text, key):
    res = ""
    for i in range(len(text)):
        res += chr(((ord(text[i].upper()) - 65) ^ (ord(key[i].upper()) - 65)) + 65)
    return res

def one_time_pad_encrypt(text):
    key = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(len(text)))
    cipher = vernam_cipher(text, key)
    return cipher, key

def rail_fence_encrypt(text, key):
    fence = ['' for _ in range(key)]
    row, dir = 0, 1
    for ch in text:
        fence[row] += ch
        if row == 0: dir = 1
        elif row == key - 1: dir = -1
        row += dir
    return ''.join(fence)


def rail_fence_decrypt(cipher, key):
    rail = [['' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0
    for _ in cipher:
        if row == 0: dir_down = True
        if row == key - 1: dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
    res, row, col = '', 0, 0
    for _ in cipher:
        if row == 0: dir_down = True
        if row == key - 1: dir_down = False
        if rail[row][col] != '':
            res += rail[row][col]
            col += 1
        row += 1 if dir_down else -1
    return res


while True:
    print("\nClassical Cipher Techniques:")
    print("1. Caesar Cipher")
    print("2. Polyalphabetic (Vigenère) Cipher")
    print("3. Vernam Cipher")
    print("4. One-Time Pad")
    print("5. Rail Fence Cipher")
    print("6. Exit")

    ch = input("Enter your choice: ")

    if ch == '1':
        text = input("Enter text: ")
        key = int(input("Enter key (number): "))
        mode = input("Encrypt or Decrypt (e/d): ").lower()
        print("Result:", caesar_cipher(text, key, mode))

    elif ch == '2':
        text = input("Enter text: ")
        key = input("Enter key (word): ")
        mode = input("Encrypt or Decrypt (e/d): ").lower()
        print("Result:", vigenere_cipher(text, key, mode))

    elif ch == '3':
        text = input("Enter text (A-Z): ").upper()
        key = input("Enter key (same length): ").upper()
        print("Result:", vernam_cipher(text, key))

    elif ch == '4':
        text = input("Enter text (A-Z): ").upper()
        cipher, key = one_time_pad_encrypt(text)
        print("Generated Key:", key)
        print("Encrypted Text:", cipher)
        print("Decrypted Text:", vernam_cipher(cipher, key))

    elif ch == '5':
        text = input("Enter text: ")
        key = int(input("Enter number of rails: "))
        mode = input("Encrypt or Decrypt (e/d): ").lower()
        print("Result:", rail_fence_encrypt(text, key) if mode == 'e' else rail_fence_decrypt(text, key))

    elif ch == '6':
        print("Exiting...")
        break

    else:
        print("Invalid choice!")
