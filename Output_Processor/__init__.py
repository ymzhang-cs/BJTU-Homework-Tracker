import bs4

class OutputProcessor:
    def __init__(self, html):
        self.soup = bs4.BeautifulSoup(html, 'html.parser')
        self.methods = {
            'prettify': self._prettify,
            'plain_text': self._plain_text
        }

    def update_html(self, html):
        self.soup = bs4.BeautifulSoup(html, 'html.parser')
    
    def get_html(self):
        return str(self.soup)

    def process(self, method='plain_text'):
        return self.methods[method]()

    def _prettify(self):
        return self.soup.prettify()
    
    def _plain_text(self):
        return self.soup.get_text(separator='\n')
    


if __name__ == '__main__':
    with open('history.txt', 'r', encoding='utf-8') as f:
        html = f.read()
        processor = OutputProcessor(html)
        print(processor.process(method='plain_text'))