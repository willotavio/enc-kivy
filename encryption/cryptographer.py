from Cryptodome.Cipher import AES
import binascii


class Cryptographer:

    @staticmethod
    def encrypt(self, encryption_key, texts_to_encrypt):
        try:
            if encryption_key and len(encryption_key) == 16 and texts_to_encrypt:
                encrypted_texts = []
                encryption_key = encryption_key.encode('utf-8')
                for text_to_encrypt in texts_to_encrypt.split(' | '):
                    text_to_encrypt = text_to_encrypt.encode('utf-8')
                    cipher = AES.new(encryption_key, AES.MODE_EAX)
                    encrypted_text, tag = cipher.encrypt_and_digest(text_to_encrypt)

                    nonce = binascii.hexlify(cipher.nonce).decode()
                    encrypted_text = binascii.hexlify(encrypted_text).decode()
                    tag = binascii.hexlify(tag).decode()

                    encrypted_info = f"{nonce}/{encrypted_text}/{tag}"
                    encrypted_texts.append(encrypted_info)

                return True, encrypted_texts

            else:
                return False, "Password must have 16 characters (*•~•)л"
        except ValueError as e:
            return False, f"Encryption failed: {str(e)}"
