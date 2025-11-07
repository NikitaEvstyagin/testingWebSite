from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import Poll
from User import User
from qwer import TestLogin
import unittest


class BrowserManager:
    _instance = None
    _lock = threading.Lock()
    _driver = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(BrowserManager, cls).__new__(cls)
                cls._instance._init_driver()
                
        return cls._instance

    def _init_driver(self):
        if self._driver is None:
            self._driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self._driver.set_window_size(1387, 755)

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls()._init_driver()
        return cls._driver

    @classmethod
    def quit_driver(cls):
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = BrowserManager.get_driver()
        cls.base_url = "https://conf.7ya.ru/"
        cls.test_user = User(username="abobavv", password="=\'6sqU-!-*\'p]Z7")

    @classmethod
    def tearDownClass(cls):
        # Не закрываем браузер здесь, чтобы он оставался открытым для следующих тестов
        pass


class CreatePostTest(TestBase):
    def test_create_and_edit_post(self):
        """Основной метод для запуска теста"""
        try:
            # Создаем тестовый опрос
            test_poll = Poll.Poll(
                title="new",
                question="Как дела?",
                answers="Отлично\nХорошо\nПлохо"
            )

            # Выполняем шаги теста
            test_login = TestLogin()
            test_login.driver = self.driver
            test_login.open_main_page()
            test_login.open_login_page()
            test_login.enter_credentials(self.test_user)
            test_login.submit_login()
            time.sleep(2)

            self.open_home_page()
            self.go_to_my_page()
            self.fill_poll_details(test_poll)
            self.publish_poll()

            # Теперь редактируем созданный опрос
            self.edit_post()

            # Проверяем результаты
            self.verify_poll_created(test_poll)
            self.verify_poll_edited()

            print("Тест успешно выполнен! Опрос создан и отредактирован.")

        except Exception as e:
            self.fail(f"Ошибка во время выполнения теста: {str(e)}")

    def open_home_page(self):
        self.driver.get(self.base_url)
        self.driver.find_element(By.CSS_SELECTOR, ".initial").click()

    def go_to_my_page(self):
        self.driver.find_element(By.LINK_TEXT, "Моя страница").click()
        self.driver.find_element(By.CSS_SELECTOR, ".mypage_dopmenu > a:nth-child(2) > img").click()

    def fill_poll_details(self, poll):
        self.driver.find_element(By.ID, "ctl00_main_NameVoting").send_keys(poll.title)
        self.driver.find_element(By.ID, "ctl00_main_txtQuestion0").send_keys(poll.question)
        self.driver.find_element(By.ID, "ctl00_main_txtAnswer0").send_keys(poll.answers)
        time.sleep(1)
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()
        self.driver.find_element(By.ID, "ctl00_main_btnPublish").click()

    def publish_poll(self):
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()

    def edit_post(self):
        """Метод для редактирования созданного опроса"""
        self.driver.find_element(By.LINK_TEXT, "Мои опросы").click()
        self.driver.find_element(By.CSS_SELECTOR, "td > a:nth-child(1) > img").click()

        # Изменяем видимость опроса
        dropdown = self.driver.find_element(By.ID, "ctl00_main_ddlVisVoting")
        Select(dropdown).select_by_index(2)

        # Изменяем видимость результатов
        results_dropdown = self.driver.find_element(By.ID, "ctl00_main_dllVisResult")
        Select(results_dropdown).select_by_index(1)

        # Сохраняем изменения
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()

        # Возвращаемся на главную страницу
        self.driver.find_element(By.CSS_SELECTOR, ".initial").click()

    def verify_poll_created(self, poll):
        """Проверяем, что опрос создан с правильными данными"""
        self.driver.find_element(By.LINK_TEXT, "Мои опросы").click()
        self.driver.find_element(By.CSS_SELECTOR, "td > a:nth-child(1) > img").click()

        created_title = self.driver.find_element(By.ID, "ctl00_main_NameVoting").get_attribute("value")
        created_question = self.driver.find_element(By.ID, "ctl00_main_txtQuestion0").get_attribute("value")

        self.assertEqual(poll.title, created_title, f"Ожидался заголовок '{poll.title}', получено '{created_title}'")
        self.assertEqual(poll.question, created_question,
                         f"Ожидался вопрос '{poll.question}', получено '{created_question}'")

    def verify_poll_edited(self):
        """Проверяем, что изменения видимости применились"""
        visibility = Select(self.driver.find_element(By.ID, "ctl00_main_ddlVisVoting")).first_selected_option.text
        results_visibility = Select(
            self.driver.find_element(By.ID, "ctl00_main_dllVisResult")).first_selected_option.text

        self.assertEqual(visibility, "Все пользователи", "Видимость опроса не изменилась")
        self.assertEqual(results_visibility, "Только после голосования", "Видимость результатов не изменилась")


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(CreatePostTest('test_create_and_edit_post'))
    # Здесь можно добавить другие тесты
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    test_suite = suite()
    try:
        runner.run(test_suite)
    finally:
        BrowserManager.quit_driver()