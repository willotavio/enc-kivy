from kivy.uix.boxlayout import BoxLayout

import os
from kivy.lang.builder import Builder

path = os.path.join(os.path.dirname(__file__), 'reencryption_window.kv')
Builder.load_file(path)

class ReencryptionWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(ReencryptionWindow, self).__init__(**kwargs)

