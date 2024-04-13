from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import secrets

class Cryptographer:

    @staticmethod
    def generate_salt():
        try:
            salt = bytearray(32)
            for i in range(32):
                salt[i] = secrets.randbelow(256)
            return salt
        except (AttributeError, NotImplementedError, SystemError) as e:
            return False, f"An error occurred: {e}"
    

    @staticmethod
    def derive_key_and_iv(password, salt):
        try:
            saltBytes = bytes(salt)
            iterations = 10000
            key_length = 16
            iv_length = 16
            backend = default_backend()

            pbkdf2 = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                salt=saltBytes,
                length=key_length + iv_length,
                iterations=iterations,
                backend=backend
            )

            password_bytes = password.encode("utf-8")
            key_and_iv = pbkdf2.derive(password_bytes)

            key = key_and_iv[:key_length]
            iv = key_and_iv[key_length:]

            return { "key": key, "iv": iv }
        except (ValueError, TypeError) as e:
            return False, f"An error occurred: {e}"


    @staticmethod
    def encrypt(text_to_encrypt, password):
        try:
            if len(text_to_encrypt) > 0 and len(password) >= 12:
                salt = Cryptographer.generate_salt()
                key_and_iv = Cryptographer.derive_key_and_iv(password, salt)
                key_bytes = key_and_iv["key"]
                iv_bytes = key_and_iv["iv"]

                backend = default_backend()
                cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend)

                padder = padding.PKCS7(algorithms.AES.block_size).padder()
                padded_text = padder.update(text_to_encrypt.encode("utf-8")) + padder.finalize()

                encryptor = cipher.encryptor()
                cipher_text = encryptor.update(padded_text) + encryptor.finalize()

                decoded_cipher_text = base64.b64encode(cipher_text).decode("utf-8")
                decoded_salt = base64.b64encode(salt).decode("utf-8")

                encrypted_text = f"{decoded_cipher_text} | {decoded_salt}"

                return True, encrypted_text
            else:
                message = ""
                if not text_to_encrypt:
                    message = "Provide something to be encrypted \\(-п-,\\)"
                elif not password:
                    message = "Provide a password <(•-•<)"
                elif len(password) < 12:
                    message = "Password must have at least 12 characters (*•~•)л"

                return False, message
        except (ValueError, AttributeError, TypeError) as e:
            return False, f"An error occurred: {e}"

    @staticmethod
    def decrypt(text_to_decrypt, password):
        try:
            if len(text_to_decrypt) > 0 and len(password) >= 12:
                encrypted_text = text_to_decrypt.split(" | ")[0]
                base64_salt = text_to_decrypt.split(" | ")[1]

                backend = default_backend()

                salt = base64.b64decode(base64_salt)

                key_and_iv = Cryptographer.derive_key_and_iv(password, salt);
                key_bytes = key_and_iv["key"];
                iv_bytes = key_and_iv["iv"];

                encrypted_text_bytes = base64.b64decode(encrypted_text)
                
                cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend)

                decryptor = cipher.decryptor()
                cipher_text = decryptor.update(encrypted_text_bytes) + decryptor.finalize()

                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                unpadded_text = unpadder.update(cipher_text) + unpadder.finalize()

                return True, unpadded_text.decode("utf-8")
            else:
                message = ""
                if not text_to_decrypt:
                    message = "Provide something to be decrypted \\(-п-,\\)"
                elif not password:
                    message = "Provide a password <(•-•<)"
                elif len(password) < 12:
                    message = "Password must have at least 12 characters (*•~•)л"

                return False, message
        except (ValueError, AttributeError, TypeError) as e:
            return False, f"An error occurred: {e}"
    
    @staticmethod
    def reencrypt(text_to_reencrypt, old_password, new_password):
        if len(text_to_reencrypt) > 0 and len(old_password) >= 12 and len(new_password) >= 12:
            decryption_status, decryption_result = Cryptographer.decrypt(text_to_reencrypt, old_password)
            if not decryption_status:
                return decryption_status, decryption_result
            encryption_status, encryption_result = Cryptographer.encrypt(decryption_result, new_password)
            if not encryption_status:
                return encryption_status, encryption_result
            return True, encryption_result
        else:
            message = ""
            if not text_to_reencrypt:
                message = "Provide something to be reencrypted (_/*•л•)_/"
            elif not old_password:
                message = "Provide the old password <(•-•<)"
            elif not new_password:
                message = "Provide the new password \\(~.~*\\)"
            elif len(old_password) < 12:
                message = "Old password must have at least 12 characters (/*-д-)>"
            elif len(new_password) < 12:
                message = "New password must have at least 12 characters (*-ш-)л"
            return False, message