from fiveminutejournal.journal import Journal, JournalPlugin, JournalQuote
from fiveminutejournal.storage import JournalStorage


class JournalConsole:

    _quote: JournalQuote = None

    def __init__(self, journal: Journal, plugin: JournalPlugin, storage: JournalStorage) -> None:
        self.journal = journal
        self.plugin = plugin
        self.storage = storage
        journal.add_questions(plugin.questions())

    def ask(self, question):
        self.print(question.text)
        for idx in range(0, self.journal.total_answers()):
            id = idx + 1
            self.journal.answer(question, id, input(f'\n {id}. '))

    def quote(self):
        if self._quote is None:
            self._quote = self.plugin.quote()
        return self._quote

    def prompt_header(self):
        self.print(self.journal.header_title(), 1)
        quote = self.quote()
        if (quote.text and quote.author):
            self.print(quote.text)
            self.print(f'~ {quote.author}', 1)

    def prompt(self):
        if self.storage.filled_once(self.journal):
            self.prompt_header()
            for question in self.journal.questions_night():
                self.ask(question)
        elif self.storage.filled_twice(self.journal):
            self.print(self.journal.message('complete'))
        else:
            self.prompt_header()
            for question in self.journal.questions_day():
                self.ask(question)

    def save(self):
        self.storage.save(self.journal, self.quote())
        self.print(f'{self.journal.message("saved")}: {self.storage.file_path(self.journal)}')
        self.print('')

    def print(self, str, n=2):
        newlines = n * '\n'
        print(f"{newlines} {str}")