class Poll:
    def __init__(self, title, question, answers, visibility="только мне", results_visibility="только мне"):
        self.title = title
        self.question = question
        self.answers = answers
        self.visibility = visibility
        self.results_visibility = results_visibility