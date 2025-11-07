from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import time
from User import User
from Poll import Poll


class ApplicationManager:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.set_window_size(1387, 755)
        self.base_url = "https://conf.7ya.ru/"

        self.navigation = NavigationHelper(self)
        self.login = LoginHelper(self)
        self.poll = PollHelper(self)

    def open_home_page(self):
        self.driver.get(self.base_url)

    def stop(self):
        self.driver.quit()


class HelperBase:
    def __init__(self, manager):
        self.manager = manager
        self.driver = manager.driver


class NavigationHelper(HelperBase):
    def open_home_page(self):
        self.driver.get(self.manager.base_url)
        self.driver.find_element(By.CSS_SELECTOR, ".initial").click()

    def go_to_my_page(self):
        self.driver.find_element(By.LINK_TEXT, "Моя страница").click()
        self.driver.find_element(By.CSS_SELECTOR, ".mypage_dopmenu > a:nth-child(2) > img").click()


class LoginHelper(HelperBase):
    LOGIN_BUTTON_ID = "btnlgntop"
    USERNAME_FIELD_ID = "txtLogin"
    PASSWORD_FIELD_ID = "txtPassword"
    SUBMIT_BUTTON_ID = "EnterButton"
    LOGIN_FORM_CSS = ".login2020"

    def login(self, user):
        self.open_login_page()
        self.enter_credentials(user)
        self.submit_login()

    def open_login_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.LOGIN_BUTTON_ID))
        ).click()

    def enter_credentials(self, user):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.USERNAME_FIELD_ID))
        ).send_keys(user.username)

        self.driver.find_element(By.CSS_SELECTOR, self.LOGIN_FORM_CSS).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.PASSWORD_FIELD_ID))
        ).send_keys(user.password)

    def submit_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, self.SUBMIT_BUTTON_ID))
        ).click()


class PollHelper(HelperBase):
    def create_poll(self, poll):
        self.fill_poll_details(poll)
        self.set_poll_visibility(poll)
        self.publish_poll()

    def fill_poll_details(self, poll):
        self.driver.find_element(By.ID, "ctl00_main_NameVoting").send_keys(poll.title)
        self.driver.find_element(By.ID, "ctl00_main_txtQuestion0").send_keys(poll.question)
        self.driver.find_element(By.ID, "ctl00_main_txtAnswer0").send_keys(poll.answers)
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()

    def set_poll_visibility(self, poll):
        visibility_dropdown = Select(self.driver.find_element(By.ID, "ctl00_main_ddlVisVoting"))
        visibility_dropdown.select_by_visible_text(poll.visibility)

        results_dropdown = Select(self.driver.find_element(By.ID, "ctl00_main_dllVisResult"))
        results_dropdown.select_by_visible_text(poll.results_visibility)

    def publish_poll(self):
        self.driver.find_element(By.ID, "ctl00_main_btnPublish").click()
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()


class TestBase:
    def setup_method(self):
        self.app = ApplicationManager()

    def teardown_method(self):
        self.app.stop()


class TestLogin(TestBase):
    def test_login(self):
        user = User(username="abobavv", password="=\'6sqU-!-*\'p]Z7")
        self.app.navigation.open_home_page()
        self.app.login.login(user)
        def is_logged_in(self):
            return "Выход" in self.driver.page_source

        def is_logged_in_as(self, username):
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, ".topline2020 span.username")
                return username in element.text
            except:
                return False

        def logout(self):
            try:
                self.driver.find_element(By.LINK_TEXT, "Выход").click()
            except:
                pass  # если не залогинен, ничего не делаем

        def login(self, user):
            if self.is_logged_in():
                if self.is_logged_in_as(user.username):
                    return
                else:
                    self.logout()

            self.open_login_page()
            self.enter_credentials(user)
            self.submit_login()


class TestCreatePoll(TestBase):
    def test_create_poll(self):
        test_poll = Poll(
            title="new",
            question="Как дела?",
            answers="Отлично\nХорошо\nПлохо",
            visibility="Для всех",
            results_visibility="Для всех"
        )

        user = User(username="abobavv", password="=\'6sqU-!-*\'p]Z7")

        self.app.navigation.open_home_page()
        self.app.login.login(user)
        self.app.navigation.go_to_my_page()
        self.app.poll.create_poll(test_poll)

        print("Тест успешно выполнен! Опрос создан.")
        time.sleep(5)  # Пауза для визуальной проверки


if __name__ == "__main__":
    test = TestCreatePoll()
    test.setup_method()
    try:
        test.test_create_poll()
    finally:
        test.teardown_method()