#!/usr/bin/env python3

def rotate_left(n, b):
    """Rotate left 32-bit integer n by b bits."""
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1_equivalent(msg: str) -> str:
    """Simplified SHA-1 equivalent implementation."""
    # Step 1: Convert to bytes and pad
    data = bytearray(msg.encode('utf-8'))
    orig_len_bits = (8 * len(data)) & 0xFFFFFFFFFFFFFFFF
    data.append(0x80)
    while (len(data) % 64) != 56:
        data.append(0)
    data += orig_len_bits.to_bytes(8, 'big')

    # Step 2: Initialize variables (same constants as SHA-1)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Step 3: Process in 512-bit chunks
    for i in range(0, len(data), 64):
        w = [0]*80
        chunk = data[i:i+64]
        for j in range(16):
            w[j] = int.from_bytes(chunk[j*4:(j*4)+4], 'big')
        for j in range(16, 80):
            w[j] = rotate_left(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        # Step 4: Main loop
        for j in range(80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = (rotate_left(a, 5) + f + e + k + w[j]) & 0xFFFFFFFF
            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Step 5: Produce final hex digest
    return ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4])

def main():
    message = input("Enter message to send: ")

    # Sender side
    sender_hash = sha1_equivalent(message)
    print(f"\n[SENDER] Message: {message}")
    print(f"[SENDER] SHA-1 Equivalent Hash: {sender_hash}")

    # Receiver side
    print("\n[NETWORK] Delivering message (no tampering)...")
    receiver_hash = sha1_equivalent(message)
    print(f"[RECEIVER] Recomputed Hash: {receiver_hash}")
    if receiver_hash == sender_hash:
        print("Result: Hashes match — integrity OK.\n")
    else:
        print("Result: Hash mismatch!\n")

    # Tampering demonstration
    tampered = list(message)
    if tampered:
        tampered[0] = chr(ord(tampered[0]) ^ 0x01)
    tampered = ''.join(tampered)
    print("[ATTACKER] Tampered message:", tampered)
    tampered_hash = sha1_equivalent(tampered)
    print("[RECEIVER] Hash of tampered message:", tampered_hash)
    if tampered_hash != sender_hash:
        print("Result: Hash mismatch — tampering detected!")
    else:
        print("Result: Hashes match (unexpected!)")

if __name__ == "__main__":
    main()
