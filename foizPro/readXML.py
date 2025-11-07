import xml.etree.ElementTree as ET

def read_polls_from_xml(filename):
    """Чтение данных из XML-файла."""
    polls = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for poll_element in root.findall("Poll"):
        title = poll_element.find("Title").text
        question = poll_element.find("Question").text
        answers = [answer.text for answer in poll_element.find("Answers")]
        polls.append({
            "title": title,
            "question": question,
            "answers": answers
        })
    return polls

# Пример использования
if __name__ == "__main__":
    polls = read_polls_from_xml("polls.xml")
    for poll in polls:
        print(poll)