from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import Poll
from User import User
from qwer import TestLogin




class CreatePostTest:
    BASE_URL = "https://conf.7ya.ru/"
    TEST_USER = User(username="abobavv", password="=\'6sqU-!-*\'p]Z7")

    def __init__(self):
        # Настройка Chrome драйвера
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.set_window_size(1387, 755)
        self.login_manager = self.TestLogin(self.driver)

    def run_test(self):
        """Основной метод для запуска теста"""
        try:
            # Создаем тестовый опрос
            test_poll = Poll.Poll(
                title="new",
                question="Как дела?",
                answers="Отлично\nХорошо\nПлохо"
            )

            # Выполняем шаги теста
            self.open_home_page()
            self.login_manager.test_login()
            self.go_to_my_page()
            self.fill_poll_details(test_poll)
            self.set_poll_visibility(test_poll)
            self.publish_poll()

            print("Тест успешно выполнен! Опрос создан.")
            time.sleep(5)  # Пауза для визуальной проверки

        except Exception as e:
            print(f"Ошибка во время выполнения теста: {str(e)}")
        finally:
            self.driver.quit()

    def open_home_page(self):
        self.driver.get(self.BASE_URL)
        self.driver.find_element(By.CSS_SELECTOR, ".initial").click()

    def go_to_my_page(self):
        self.driver.find_element(By.LINK_TEXT, "Моя страница").click()
        self.driver.find_element(By.CSS_SELECTOR, ".mypage_dopmenu > a:nth-child(2) > img").click()

    def fill_poll_details(self, poll):
        self.driver.find_element(By.ID, "ctl00_main_NameVoting").send_keys(poll.title)
        self.driver.find_element(By.ID, "ctl00_main_txtQuestion0").send_keys(poll.question)
        self.driver.find_element(By.ID, "ctl00_main_txtAnswer0").send_keys(poll.answers)
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()

    def set_poll_visibility(self, poll):
        # Установка видимости голосования
        visibility_dropdown = Select(self.driver.find_element(By.ID, "ctl00_main_ddlVisVoting"))
        visibility_dropdown.select_by_visible_text(poll.visibility)

        # Установка видимости результатов
        results_dropdown = Select(self.driver.find_element(By.ID, "ctl00_main_dllVisResult"))
        results_dropdown.select_by_visible_text(poll.results_visibility)

    def publish_poll(self):
        self.driver.find_element(By.ID, "ctl00_main_btnPublish").click()
        self.driver.find_element(By.ID, "ctl00_main_sendform1").click()


# Запуск теста при выполнении скрипта
if __name__ == "__main__":
    test = CreatePostTest()
    test.run_test()