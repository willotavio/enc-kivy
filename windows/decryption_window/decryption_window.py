from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from encryption.cryptographer import Cryptographer

import os

from kivy.lang.builder import Builder
path = os.path.join(os.path.dirname(__file__), 'decryption_window.kv')
Builder.load_file(path)


class DecryptionWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(DecryptionWindow, self).__init__(**kwargs)
        self.ids.decrypt_button.bind(on_press=self.decrypt)

    def on_copy_button_press(self):
        if len(self.ids.decrypted_result.text) > 0:
            Clipboard.copy(str(self.ids.decrypted_result.text))
            self.ids.copy_confirmation.text = "Copied to clipboard \\(>-<*)|"

    def decrypt(self, button_instance):
        status, result = Cryptographer.decrypt(self, self.ids.decryption_key_input.text, self.ids.text_to_decrypt_input.text)
        decrypted_result = ""
        if status:
            for item in result:
                decrypted_result += f"{item}\n\n"

            decrypted_result = decrypted_result[:-2]
            self.ids.decrypted_result.text = decrypted_result
            self.ids.decryption_key_input.text = ""
            self.ids.text_to_decrypt_input.text = ""
        else:
            self.ids.decrypted_result.text = result

