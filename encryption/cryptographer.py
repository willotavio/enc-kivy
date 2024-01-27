from Cryptodome.Cipher import AES
import binascii


class Cryptographer:

    @staticmethod
    def encrypt(self, encryption_key, texts_to_encrypt, delimiter):
        try:
            if not delimiter:
                delimiter = "_/*;@.@;*/_"
            if encryption_key and len(encryption_key) == 16 and len(texts_to_encrypt) > 0:
                encrypted_texts = []
                encryption_key = encryption_key.encode('utf-8')
                for text_to_encrypt in texts_to_encrypt.split(delimiter):
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
                message = ""
                if not texts_to_encrypt:
                    message = "Provide something to be encrypted \\(-п-,\\)"
                elif not encryption_key:
                    message = "Provide a key <(•-•<)"
                elif len(encryption_key) != 16:
                    message = "Key must have 16 characters (*•~•)л"
                return False, message
        except ValueError as e:
            return False, f"Encryption failed: {str(e)}"

    @staticmethod
    def decrypt(self, decryption_key, texts_to_decrypt, delimiter):
        try:
            if not delimiter:
                delimiter = "_/*;@.@;*/_"
            if decryption_key and len(decryption_key) == 16 and len(texts_to_decrypt) > 0:
                decrypted_texts = []
                decryption_key = decryption_key.encode('utf-8')
                for text_to_decrypt in texts_to_decrypt.split(delimiter):
                    nonce, encrypted_text, tag = text_to_decrypt.split('/')
                    nonce = bytes.fromhex(nonce)
                    encrypted_text = bytes.fromhex(encrypted_text)
                    tag = bytes.fromhex(tag)
                    cipher = AES.new(decryption_key, AES.MODE_EAX, nonce)
                    decrypted_info = cipher.decrypt_and_verify(encrypted_text, tag)
                    decrypted_info = decrypted_info.decode('utf-8')
                    decrypted_texts.append(decrypted_info)
                return True, decrypted_texts
            else:
                message = ""
                if not texts_to_decrypt:
                    message = "Provide something to be decrypted \\(-п-,\\)"
                elif not decryption_key:
                    message = "Provide a key <(•-•<)"
                elif len(decryption_key) != 16:
                    message = "Key must have 16 characters (*•~•)л"
                return False, message
        except ValueError as e:
            return False, f"Decryption failed: {str(e)}"

    @staticmethod
    def reencrypt(self, old_encryption_key, new_encryption_key, texts_to_reencrypt, delimiter):
        if old_encryption_key and len(old_encryption_key) == 16 and new_encryption_key and len(new_encryption_key) == 16 and len(texts_to_reencrypt) > 0:
            status, result = Cryptographer.decrypt(self, old_encryption_key, texts_to_reencrypt, delimiter)
            if not status:
                return False, result
            texts_to_encrypt = ""
            for item in result:
                texts_to_encrypt += f"{item}{delimiter}"
            texts_to_encrypt = texts_to_encrypt[:-len(delimiter)]
            status, result = Cryptographer.encrypt(self, new_encryption_key, texts_to_encrypt, delimiter)
            return True, result
        else:
            message = ""
            if not texts_to_reencrypt:
                message = "Provide something to be reencrypted (_/*•л•)_/"
            elif not old_encryption_key:
                message = "Provide the old key <(•-•<)"
            elif not new_encryption_key:
                message = "Provide the new key \\(~.~*\\)"
            elif len(old_encryption_key) != 16:
                message = "Old key must have 16 characters (/*-д-)>"
            elif len(new_encryption_key) != 16:
                message = "New key must have 16 characters (*-ш-)л"
            return False, message
