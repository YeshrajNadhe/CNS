def xor_encrypt_decrypt(input_file, output_file, key_char):
    try:
        
        with open(input_file, 'rb') as infile:
            data = infile.read()

        key = ord(key_char)

        encrypted_data = bytes([b ^ key for b in data])

        with open(output_file, 'wb') as outfile:
            outfile.write(encrypted_data)

        print("\nProcess completed successfully!")
        print(f"Output file saved as: {output_file}")
        print("(Run again with the same key to decrypt the image.)")

    except FileNotFoundError:
        print("Error: File not found or cannot be opened.")
    except Exception as e:
        print(" An error occurred:", e)


def main():
    print("=== Image Encryption/Decryption using XOR ===")
    input_file = input("Enter image filename to encrypt/decrypt (with extension): ").strip()
    output_file = input("Enter output filename (with extension): ").strip()
    key_char = input("Enter single character key: ").strip()

    if len(key_char) != 1:
        print(" Error: Key must be a single character.")
        return

    xor_encrypt_decrypt(input_file, output_file, key_char)


if __name__ == "__main__":
    main()
