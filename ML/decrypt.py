from cryptography.fernet import Fernet



key = "0oeWfuGITiu4D7Yv1nXk-ISwSb1glKK3q2pu-1di11o="


def encrypt_text(text):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(text.encode())
    return encrypted_text


def decrypt_text(encrypted_text):
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text
# print(f"Generated Key: {key}")

# text_to_encrypt = "Hello, World!"

# encrypted_text = encrypt_text(key, text_to_encrypt)
# print(f"Encrypted Text: {encrypted_text}")

# decrypted_text = decrypt_text(key, encrypted_text)
# print(f"Decrypted Text: {decrypted_text}")
