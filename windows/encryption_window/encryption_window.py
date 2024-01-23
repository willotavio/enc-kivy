from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import os

kv_path = os.path.join(os.path.dirname(__file__), 'encryption_window.kv')
Builder.load_file(kv_path)


class EncryptionWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(EncryptionWindow, self).__init__(**kwargs)
