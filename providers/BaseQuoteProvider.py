import requests


class BaseQuoteProvider:

    api: str
    _content = ''
    _author = ''

    def request(self):
        if self.api is None:
            print('BaseQuoteProvider.api not set')
        return requests.get(self.api)

    def load(self):
        print('Must implement BaseQuoteProvider.load() method')
        return self

    def content(self):
        return self._content

    def author(self):
        return self._author
