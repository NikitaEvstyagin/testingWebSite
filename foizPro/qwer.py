from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from User import User

class TestLogin:
    BASE_URL = "https://conf.7ya.ru/"
    LOGIN_BUTTON_ID = "btnlgntop"
    USERNAME_FIELD_ID = "txtLogin"
    PASSWORD_FIELD_ID = "txtPassword"
    SUBMIT_BUTTON_ID = "EnterButton"
    LOGIN_FORM_CSS = ".login2020"

    def __init__(self):
        self.driver = None  # Initialize driver

    def setup_method(self):
        """Setup method to be executed before each test."""
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1387, 756)

    def teardown_method(self):
        """Teardown method to be executed after each test."""
        if self.driver:
            self.driver.quit()
            self.driver = None  # Reset driver after quitting

    def test_user(self):
        return User(username="abobavv", password="=\'6sqU-!-*\'p]Z7")

    def test_login(self):
        """Test successful user login"""
        self.setup_method()  # Call setup

        try:
            user = self.test_user()
            self.open_main_page()
            self.open_login_page()
            self.enter_credentials(user)
            self.submit_login()

            # Add verification here
            # Example:
            # WebDriverWait(self.driver, 10).until(EC.url_contains("dashboard"))
            print("Login test completed (add assertion to verify success).")

        finally:
            self.teardown_method()  # Ensure teardown is always called, even if errors occur

    def open_main_page(self):
        self.driver.get(self.BASE_URL)

    def open_login_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.LOGIN_BUTTON_ID))
        ).click()

    def enter_credentials(self, user):
        # Enter username
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.USERNAME_FIELD_ID))
        ).send_keys(user.username)

        # Click login form (if needed to activate password field)
        self.driver.find_element(By.CSS_SELECTOR, self.LOGIN_FORM_CSS).click()

        # Enter password
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.PASSWORD_FIELD_ID))
        ).send_keys(user.password)

    def submit_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.SUBMIT_BUTTON_ID))
        ).click()


# Run the test when the script is executed
if __name__ == "__main__":
    test = TestLogin()
    test.test_login()  # Execute the test