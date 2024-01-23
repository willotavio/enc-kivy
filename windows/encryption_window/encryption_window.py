from kivy.uix.boxlayout import BoxLayout
from encryption.cryptographer import Cryptographer

from kivy.lang import Builder
import os
kv_path = os.path.join(os.path.dirname(__file__), 'encryption_window.kv')
Builder.load_file(kv_path)


class EncryptionWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(EncryptionWindow, self).__init__(**kwargs)

        self.ids.encrypt_button.bind(on_press=self.encrypt)

    def encrypt(self, button_instance):
        status, result = Cryptographer.encrypt(self, self.ids.encryption_key_input.text, self.ids.text_to_encrypt_input.text)
        self.ids.encrypted_result.text = result
        if status:
            self.ids.encryption_key_input.text = ""
            self.ids.text_to_encrypt_input.text = ""
