from Search import Search

from Output.abstract import OutputProcessor
from Output.plain_text import PlainText

methods = {
            'plain_text': PlainText
        }

class Output:
    def __init__(self, search: Search, method: str):
        self.search = search
        self.processor = methods[method](search)

    def __str__(self):
        return str(self.processor)

    @staticmethod
    def show_methods():
        return list(methods.keys())

    def process(self):
        return self.processor.process()

    def save(self, path: str):
        return self.processor.save(path)