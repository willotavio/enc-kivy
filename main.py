from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from windows.encryption_window.encryption_window import EncryptionWindow
import os

from kivy.lang.builder import Builder
path = os.path.join(os.path.dirname(__file__), 'main.kv')
Builder.load_file(path)


class HomeTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(HomeTabs, self).__init__(**kwargs)
        self.ids.tab_1.add_widget(EncryptionWindow())


class AppMain(App):
    def build(self):
        self.title = "Enc ur stuff"
        return HomeTabs()


if __name__ == '__main__':
    AppMain().run()
