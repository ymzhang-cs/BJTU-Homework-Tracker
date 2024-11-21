import os

from Output.abstract import OutputProcessor
from Search import Search

import bs4
import datetime

class PlainText(OutputProcessor):
    def __init__(self, search: Search) -> None:
        html = search.output()
        self.soup = bs4.BeautifulSoup(html, 'html.parser')
        self.methods = {
            'prettify': self._prettify,
            'plain_text': self._plain_text
        }

    def __str__(self) -> str:
        return self.process()

    # def update_html(self, html):
    #     self.soup = bs4.BeautifulSoup(html, 'html.parser')
    #
    # def get_html(self):
    #     return str(self.soup)

    def process(self, method='plain_text') -> str:
        return self.methods[method]()

    def _prettify(self) -> str:
        return self.soup.prettify()

    def _plain_text(self) -> str:
        return self.soup.get_text(separator='\n')

    def save(self, path: str, name: str):

        if not os.path.exists(path):
            os.mkdir(path)

        full_path = os.path.join(path, name + '.txt')
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(self.process())
        return


# if __name__ == '__main__':
#     with open('history.txt', 'r', encoding='utf-8') as f:
#         html = f.read()
#         processor = PlainText(html)
#         print(processor.process(method='plain_text'))