from providers.BaseQuoteProvider import BaseQuoteProvider

class ZenQuoteProvider(BaseQuoteProvider):

    api = 'https://zenquotes.io/api/today'

    def load(self):
        data = self.request().json()
        self._content = data[0]['q']
        self._author = data[0]['a']
        return self