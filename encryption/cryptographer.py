from Cryptodome.Cipher import AES
import binascii


class Cryptographer:

    @staticmethod
    def encrypt(self, encryption_key, text_to_encrypt):
        try:
            if encryption_key and len(encryption_key) == 16 and text_to_encrypt:
                encryption_key = encryption_key.encode('utf-8')
                text_to_encrypt = text_to_encrypt.encode('utf-8')
                cipher = AES.new(encryption_key, AES.MODE_EAX)
                encrypted_text, tag = cipher.encrypt_and_digest(text_to_encrypt)

                nonce = binascii.hexlify(cipher.nonce).decode()
                encrypted_text = binascii.hexlify(encrypted_text).decode()
                tag = binascii.hexlify(tag).decode()

                encrypted_info = f"{nonce}/{encrypted_text}/{tag}"
                return True, encrypted_info
            else:
                return False, "Password must have 16 characters (*•~•)л"
        except ValueError as e:
            return False, f"Encryption failed: {str(e)}"
