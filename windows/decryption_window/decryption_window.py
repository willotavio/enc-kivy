from kivy.uix.boxlayout import BoxLayout

import os

from kivy.lang.builder import Builder
path = os.path.join(os.path.dirname(__file__), 'decryption_window.kv')
Builder.load_file(path)


class DecryptionWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(DecryptionWindow, self).__init__(**kwargs)
