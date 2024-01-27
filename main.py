from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from windows.encryption_window.encryption_window import EncryptionWindow
from windows.decryption_window.decryption_window import DecryptionWindow
from windows.reencryption_window.reencryption_window import ReencryptionWindow
import os

from kivy.config import Config
from kivy.lang.builder import Builder

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

path = os.path.join(os.path.dirname(__file__), 'main.kv')
Builder.load_file(path)

class HomeTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(HomeTabs, self).__init__(**kwargs)
        self.ids.tab_1.add_widget(EncryptionWindow())
        self.ids.tab_2.add_widget(DecryptionWindow())
        self.ids.tab_3.add_widget(ReencryptionWindow())


class AppMain(App):
    def build(self):
        self.title = "Enc ur stuff"
        return HomeTabs()


if __name__ == '__main__':
    AppMain().run()
