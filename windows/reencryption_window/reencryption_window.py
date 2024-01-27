from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from encryption.cryptographer import Cryptographer

import os
from kivy.lang.builder import Builder

path = os.path.join(os.path.dirname(__file__), 'reencryption_window.kv')
Builder.load_file(path)


class ReencryptionWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(ReencryptionWindow, self).__init__(**kwargs)
        self.ids.reencrypt_button.bind(on_press=self.reencrypt)

    def on_copy_button_press(self):
        if len(self.ids.reencrypted_result.text) > 0:
            Clipboard.copy(str(self.ids.reencrypted_result.text))
            self.ids.copy_confirmation.text = "Copied to clipboard \\(>-<*)|"

    def reencrypt(self, instance):
        status, result = Cryptographer.reencrypt(
            self,
            self.ids.old_reencryption_key_input.text,
            self.ids.new_reencryption_key_input.text,
            self.ids.text_to_reencrypt_input.text,
            self.ids.delimiter_input.text
        )
        reencrypted_result = ""
        if status:
            for item in result:
                reencrypted_result += f"{item}\n\n"
            reencrypted_result = reencrypted_result[:-2]
            self.ids.reencrypted_result.text = reencrypted_result
            self.ids.text_to_reencrypt_input.text = ""
            self.ids.old_reencryption_key_input.text = ""
            self.ids.new_reencryption_key_input.text = ""
            self.ids.delimiter_input.text = ""
        else:
            self.ids.reencrypted_result.text = result

