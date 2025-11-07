from refactor import TestBase
from Settings import Settings
from User import User

class AuthBase(TestBase):
    def setup_method(self):
        super().setup_method()
        user = User(username=Settings.Login, password=Settings.Password)
        self.app.login.login(user)
