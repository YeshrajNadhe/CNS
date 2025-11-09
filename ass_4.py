def mm(a, b, m):
    r = 0
    a %= m
    while b:
        if b & 1:
            r = (r + a) % m
        a = (2 * a) % m
        b >>= 1
    return r % m

def me(b, e, m):
    r = 1
    b %= m
    while e > 0:
        if e & 1:
            r = mm(r, b, m)
        b = mm(b, b, m)
        e >>= 1
    return r

def xr(s, k):
    kb = k & 0xFF
    return ''.join(chr(ord(c) ^ kb) for c in s)

print("Diffie-Hellman with MITM Simulation\n")
p = int(input("Enter prime p: "))
g = int(input("Enter base g: "))
print(f"\nPublic: p = {p}, g = {g}\n")
a = int(input("A private a: "))
b = int(input("B private b: "))
e1 = int(input("C private toward A e1: "))
e2 = int(input("C private toward B e2: "))
print()
A = me(g, a, p)
B = me(g, b, p)
print("Public keys (honest):")
print(f"A = {A}")
print(f"B = {B}\n")
K1 = me(B, a, p)
K2 = me(A, b, p)
print("Honest shared keys:")
print(f"A key: {K1}")
print(f"B key: {K2}")
print(f"Match? {'YES' if K1 == K2 else 'NO'}\n")
plain = input("Message for honest comm: ")
ch = xr(plain, K1)
rec = xr(ch, K2)
print("\nHonest example:")
print(f"Plain: {plain}")
print("Cipher (hex):", ' '.join(f"{ord(c):02X}" for c in ch))
print(f"Decrypted by B: {rec}\n")
print("MITM Simulation")
Epub_b = me(g, e2, p)
Epub_a = me(g, e1, p)
print(f"A sends A = {A} (intercepted)")
print(f"C sends to B: {Epub_b}")
print(f"B sends B = {B} (intercepted)")
print(f"C sends to A: {Epub_a}\n")
Ka = me(Epub_a, a, p)
Kb = me(Epub_b, b, p)
Ke_a = me(A, e1, p)
Ke_b = me(B, e2, p)
print("Keys after MITM:")
print(f"A's believed key: {Ka}")
print(f"B's believed key: {Kb}")
print(f"C w/ A: {Ke_a}")
print(f"C w/ B: {Ke_b}")
print(f"A and B share? {'YES' if Ka == Kb else 'NO'}")
print("C can read/re-encrypt messages.\n")
m1 = input("Secret from A to B: ")
c1 = xr(m1, Ka)
print("A sends (hex):", ' '.join(f"{ord(c):02X}" for c in c1))
eve_plain = xr(c1, Ke_a)
print(f"C decrypts: {eve_plain}")
eve_re = xr(eve_plain, Ke_b)
print("C re-encrypts (hex):", ' '.join(f"{ord(c):02X}" for c in eve_re))
bob_get = xr(eve_re, Kb)
print(f"B decrypts: {bob_get}\n")
print("Summary:")
print("A and B believe they have a secure key, but C shares separate keys and can read/modify messages.")
print("Use authentication (signatures, TLS) in real systems to prevent MITM.")
