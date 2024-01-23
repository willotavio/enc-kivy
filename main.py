from kivy.app import App
from windows.encryption_window.encryption_window import EncryptionWindow


class AppMain(App):
    def build(self):
        return EncryptionWindow()


if __name__ == '__main__':
    AppMain().run()
