import xml.etree.ElementTree as ET
import os

class Settings:
    file = "Settings.xml"
    tree = None

    @staticmethod
    def load_settings():
        if not os.path.exists(Settings.file):
            raise Exception("Settings file not found: " + Settings.file)
        Settings.tree = ET.parse(Settings.file)

    @staticmethod
    def _get_value(tag):
        if Settings.tree is None:
            Settings.load_settings()
        root = Settings.tree.getroot()
        element = root.find(tag)
        return element.text if element is not None else None

    @property
    def BaseUrl(self):
        return Settings._get_value("BaseUrl")

    @property
    def Login(self):
        return Settings._get_value("Login")

    @property
    def Password(self):
        return Settings._get_value("Password")
