#!/usr/bin/env python3
import sys

def simple_hash(data: bytes) -> str:
    """DJB2-like simple hash over bytes, return 8-hex lowercase string."""
    h = 5381
    for b in data:
        # h = h * 33 + b
        h = ((h << 5) + h) + b
        h &= 0xFFFFFFFF  
    return format(h & 0xFFFFFFFF, '08x')

def sender(msg_bytes: bytes):
    digest = simple_hash(msg_bytes)
    return msg_bytes, digest

def receiver_check(msg_bytes: bytes, sent_digest: str) -> bool:
    my_digest = simple_hash(msg_bytes)
    print(f"[RECEIVER] Recomputed digest: {my_digest}")
    return my_digest == sent_digest

def main():
    try:
        message = input("Enter message to send: ")
    except EOFError:
        return

    # encode to bytes (UTF-8) like C++ unsigned char iteration
    msg_bytes = message.encode('utf-8')

    sent_msg, sent_digest = sender(msg_bytes)
    print(f"\n[SENDER] Message: {message}")
    print(f"[SENDER] Simple-hash: {sent_digest}\n")

    print("[NETWORK] Delivering message (no tampering)...")
    ok = receiver_check(sent_msg, sent_digest)
    print("Result: " + ("Hashes match : integrity OK.\n" if ok else "Hash mismatch!\n"))

    print("Demonstrating tampering (flip first byte if exists)...")
    tampered = bytearray(sent_msg)
    if len(tampered) > 0:
        tampered[0] ^= 0x01  # flip lowest bit of first byte
    # decode for printable display: use latin-1 so byte values map 1:1 to characters
    tampered_display = tampered.decode('latin-1')
    print(f"[NETWORK] Tampered message: {tampered_display}")
    ok2 = receiver_check(bytes(tampered), sent_digest)
    print("Result: " + ("Hashes match (unexpected).\n" if ok2 else "Hash mismatch : tampering detected.\n"))

if __name__ == "__main__":
    main()
