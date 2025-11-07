import unittest

from readXML import read_polls_from_xml


class TestPollCreation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.polls = read_polls_from_xml("polls.xml")

    def test_create_poll(self):
        for poll in self.polls:
            with self.subTest(poll=poll):
                print(f"Testing poll: {poll['title']}")
                # Здесь можно добавить логику для создания опроса
                self.assertTrue(True)  # Пример проверки

if __name__ == "__main__":
    unittest.main()