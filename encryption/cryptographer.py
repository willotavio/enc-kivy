from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import secrets

class Cryptographer:

    @staticmethod
    def generateSalt():
        salt = bytearray(32)
        for i in range(32):
            salt[i] = secrets.randbelow(256)
        return salt
    

    @staticmethod
    def deriveKeyAndIv(password, salt):
        saltBytes = bytes(salt)
        iterations = 10000
        keyLength = 16
        ivLength = 16
        backend = default_backend()

        pbkdf2 = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=saltBytes,
            length=keyLength + ivLength,
            iterations=iterations,
            backend=backend
        )

        passwordBytes = password.encode("utf-8")
        keyAndIv = pbkdf2.derive(passwordBytes)

        key = keyAndIv[:keyLength]
        iv = keyAndIv[keyLength:]

        return { "key": key, "iv": iv }


    @staticmethod
    def encrypt(textToEncrypt, password):
        salt = Cryptographer.generateSalt()
        keyAndIv = Cryptographer.deriveKeyAndIv(password, salt)
        keyBytes = keyAndIv["key"]
        ivBytes = keyAndIv["iv"]

        backend = default_backend()
        cipher = Cipher(algorithms.AES(keyBytes), modes.CBC(ivBytes), backend)

        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_text = padder.update(textToEncrypt.encode("utf-8")) + padder.finalize()

        encryptor = cipher.encryptor()
        cipher_text = encryptor.update(padded_text) + encryptor.finalize()

        decoded_cipher_text = base64.b64encode(cipher_text).decode("utf-8")
        decoded_salt = base64.b64encode(salt).decode("utf-8")

        encrypted_text = f"{decoded_cipher_text} | {decoded_salt}"

        return True, encrypted_text


    @staticmethod
    def decrypt(encrypted_info, password):
        encrypted_text = encrypted_info.split(" | ")[0]
        base64_salt = encrypted_info.split(" | ")[1]

        backend = default_backend()

        salt = base64.b64decode(base64_salt)

        key_and_iv = Cryptographer.deriveKeyAndIv(password, salt);
        key_bytes = key_and_iv["key"];
        iv_bytes = key_and_iv["iv"];

        encrypted_text_bytes = base64.b64decode(encrypted_text)
        
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend)

        decryptor = cipher.decryptor()
        cipher_text = decryptor.update(encrypted_text_bytes) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_text = unpadder.update(cipher_text) + unpadder.finalize()

        return True, unpadded_text.decode("utf-8")
    
    @staticmethod
    def reencrypt(text_to_reencrypt, old_password, new_password):
        decrypt_status, decrypted_text = Cryptographer.decrypt(text_to_reencrypt, old_password)
        encrypt_status, reencrypted_text = Cryptographer.encrypt(decrypted_text, new_password)
        return True, reencrypted_text