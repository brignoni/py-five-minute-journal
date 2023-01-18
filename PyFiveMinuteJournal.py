from datetime import datetime
from providers.BaseStorageProvider import BaseStorageProvider
from providers.BaseQuoteProvider import BaseQuoteProvider


class Journal:

    def __init__(self, namespace: str, title: str, day_questions: list, night_questions: list) -> None:
        self._title = title
        self._datetime = datetime.today()
        self._namespace = namespace
        self._day_questions = list(map(Question, day_questions))
        self._night_questions = list(map(Question, night_questions))

    def namespace(self) -> str:
        return self._namespace

    def id(self) -> str:
        return f'{self.namespace()}-{self.iso_date()}'

    def title(self) -> str:
        return self._title

    def year(self) -> int:
        return self._datetime.year

    def iso_date(self) -> str:
        return self._datetime.strftime("%Y-%m-%d")

    def iso_time(self) -> str:
        return self._datetime.strftime('%I:%M %p')

    def pretty_date(self) -> str:
        return self._datetime.strftime('%A, %b %w %Y')

    def header_title(self) -> str:
        return f'{self._title} | {self.pretty_date()}'

    def day_questions(self):
        return self._day_questions

    def night_questions(self):
        return self._night_questions

    def __len__(self):
        return len(self.day_questions()) + len(self.night_questions())


class Question:

    def __init__(self, question, total_answers=3) -> None:
        self.question = question
        self.total_answers = total_answers
        self._quote = None
        self._answers = []

    def answer(self, id: str, answer: str):
        if len(answer) > 0:
            self._answers.append(Answer(id, answer))

    def content(self):
        return self.question

    def answers(self):
        return self._answers

    def __str__(self) -> str:
        answers = '\n '.join(map(str, self._answers))
        return f"<Question content='{self.question}'>\n {answers}\n</Question>"

    def __len__(self):
        return len(self._answers)


class Answer:

    def __init__(self, id, answer) -> None:
        self._id = id
        self._answer = answer

    def id(self):
        return self._id

    def content(self):
        return self._answer

    def __str__(self) -> str:
        return f'<Answer id={self.id()} content="{self.content()}"/>'


class JournalCommandLine:

    def __init__(self, journal: Journal, quote: BaseQuoteProvider, storage: BaseStorageProvider) -> None:
        self._journal = journal
        self._quote = quote
        self._storage = storage

    def ask(self, question):
        self.print(question.content())
        for idx in range(0, question.total_answers):
            id = idx + 1
            question.answer(id, input(f'\n {id}. '))

    def prompt_quote(self):
        self._quote.load()
        if (self._quote.content() and self._quote.author()):
            self.print(f'"{self._quote.content()}"')
            self.print(f'~ {self._quote.author()}', 1)

    def prompt(self):

        if self._storage.filled_once(self._journal):
            self.print(self._journal.header_title(), 1)
            for question in self._journal.night_questions():
                self.ask(question)
        elif self._storage.filled_twice(self._journal):
            self.print(
                "Today's journal is here: " +
                self._storage.file_path(self._journal)
            )
            self.print('')
        else:
            self.print(self._journal.header_title(), 1)
            self.prompt_quote()
            for question in self._journal.day_questions():
                self.ask(question)

    def save(self):
        self._storage.save(self._journal, self._quote)

    def print(self, str, n=2):
        newlines = n * '\n'
        print(f"{newlines} {str}")
