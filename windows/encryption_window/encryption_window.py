from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from encryption.cryptographer import Cryptographer

from kivy.lang import Builder
import os
kv_path = os.path.join(os.path.dirname(__file__), 'encryption_window.kv')
Builder.load_file(kv_path)


class EncryptionWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(EncryptionWindow, self).__init__(**kwargs)
        self.ids.encrypt_button.bind(on_press=self.encrypt)

    def on_copy_button_press(self):
        if len(self.ids.encrypted_result.text) > 0:
            Clipboard.copy(str(self.ids.encrypted_result.text))
            self.ids.copy_confirmation.text = "Copied to clipboard \\(>-<*)|"

    def encrypt(self, button_instance):
        status, result = Cryptographer.encrypt(self.ids.text_to_encrypt_input.text, self.ids.encryption_key_input.text)
        encrypted_texts = result
        if status:
            self.ids.encryption_key_input.text = ""
            self.ids.text_to_encrypt_input.text = ""
            self.ids.delimiter_input.text = ""
        else:
            encrypted_texts = result
        self.ids.encrypted_result.text = encrypted_texts
