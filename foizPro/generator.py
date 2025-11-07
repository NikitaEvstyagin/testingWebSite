import random
from faker import Faker
import xml.etree.ElementTree as ET

class PollDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_poll_data(self, count):
        """Генерация тестовых данных для опросов."""
        polls = []
        for _ in range(count):
            title = self.fake.sentence(nb_words=3) 
            question = self.fake.sentence(nb_words=5)
            answers = [self.fake.word() for _ in range(random.randint(2, 5))]
            polls.append({
                "title": title,
                "question": question,
                "answers": answers
            })
        return polls

    def save_to_xml(self, polls, filename="polls.xml"):
        """Сохранение данных в XML-файл."""
        root = ET.Element("Polls")
        for poll in polls:
            poll_element = ET.SubElement(root, "Poll")

            title_element = ET.SubElement(poll_element, "Title")
            title_element.text = poll["title"]

            question_element = ET.SubElement(poll_element, "Question")
            question_element.text = poll["question"]

            answers_element = ET.SubElement(poll_element, "Answers")
            for answer in poll["answers"]:
                answer_element = ET.SubElement(answers_element, "Answer")
                answer_element.text = answer

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Данные успешно сохранены в файл: {filename}")

def main():
    print("=== Генератор тестовых данных для опросов ===")
    try:
        count = int(input("Введите количество опросов для генерации: "))
        if count <= 0:
            print("Количество опросов должно быть больше 0.")
            return
    except ValueError:
        print("Ошибка: введите корректное число.")
        return

    generator = PollDataGenerator()
    polls = generator.generate_poll_data(count)
    generator.save_to_xml(polls)

if __name__ == "__main__":
    main()