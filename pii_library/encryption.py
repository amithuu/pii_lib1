from cryptography.fernet import Fernet  # type: ignore
import base64
import os


def encrypt_data(data, fields_to_mask):
    encrypted_values = {}
    tokens = {}
    for field in fields_to_mask:
        value = data[field]
        if field in data:
            token = Fernet.generate_key()  # Generate a separate token for each field
            cipher = Fernet(token)
            salt = os.urandom(16)
            salted_data = salt + value.encode()
            encrypted_data = cipher.encrypt(salted_data)
            encrypted_values[field] = base64.urlsafe_b64encode(salt + encrypted_data).decode()
            tokens[field] = token.decode()  # Store the token for this field
    return tokens, encrypted_values  # Return tokens and encrypted values

def decrypt_data(encrypted_data, tokens, fields_to_mask):
    decrypted_values = {}
    for field in fields_to_mask:
        if field in encrypted_data:
            encoded_data = encrypted_data[field].encode()
            token = tokens[field].encode()
            cipher = Fernet(token)
            decoded_data = base64.urlsafe_b64decode(encoded_data)
            salt = decoded_data[:16]
            encrypted_data_field = decoded_data[16:]
            decrypted_data = cipher.decrypt(encrypted_data_field)[16:].decode()
            decrypted_values[field] = decrypted_data
    return decrypted_values




""" 
Encrypts the given data using a symmetric encryption algorithm (Fernet) with a randomly generated key.
The encrypted data is then salted, base64-encoded, and returned as a string.

Parameters:
data (str): The data to be encrypted.

Returns:
str: The encrypted and base64-encoded data. 
"""

"""
Decrypts the given encrypted data using a symmetric encryption algorithm (Fernet) with a randomly generated key.
The encrypted data is first base64-decoded, then salted and decrypted using the Fernet cipher.
The decrypted data is returned as a string.

Parameters:
encrypted_data (str): The encrypted and base64-encoded data to be decrypted.

Returns:
str: The decrypted data.
"""
