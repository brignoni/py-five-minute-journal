from datetime import datetime
import json
import requests
from providers.BaseStorageProvider import BaseStorageProvider

QUOTE_API = 'https://zenquotes.io/api/today'


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
        return self._datetime.strftime('%A, %b %w %Y %I:%M %p')

    def header_title(self) -> str:
        return f'{self._title} | {self.pretty_date()}'

    # def open(self):

    #     self.print(self.header_title(), 1)
    #     self._quote = Quote()
    #     # self._quote.load().print()

    #     for day_question in self._day_questions:
    #         day_question.ask()

    #     self.print('')

    # def markdown(self):
    #     md = f'# {self._title}\n\n{self.pretty_date()}\n\n'
    #     md += self._quote.markdown()
    #     for day_question in self._day_questions:
    #         md += day_question.markdown()
    #     return md

    def day_questions(self):
        return self._day_questions

    def night_questions(self):
        return self._night_questions


class Question:

    def __init__(self, question, total_answers=3) -> None:
        self.question = question
        self.total_answers = total_answers
        self._quote = None
        self._answers = []

    def answer(self, id: str, answer: str):
        self._answers.append(Answer(id, answer))

    def content(self):
        return self.question

    def answers(self):
        return self._answers

    # def markdown(self) -> str:
    #     md = f'## {self.content()}\n\n'
    #     if len(self._answers) > 0:
    #         for answer in self._answers:
    #             md += answer.markdown()
    #     else:
    #         md += 'No answer.\n'
    #     return md + '\n\n'

    def __str__(self) -> str:
        answers = '\n '.join(map(str, self._answers))
        return f"<Question content='{self.question}'>\n {answers}\n</Question>"


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


class Quote:

    def __init__(self) -> None:
        pass

    def load(self):
        quote_response = requests.get(QUOTE_API)
        data = json.loads(quote_response.content)
        self._content = data[0]['q']
        self._author = data[0]['a']
        return self

    def content(self):
        return self._content

    def author(self):
        return self._author

    # def print(self):
    #     if (self.content() and self.author()):
    #         super().print(f'"{self.content()}"')
    #         super().print(f'~ {self.author()}', 1)


class JournalCommandLine:

    def __init__(self, journal: Journal, quote: Quote, storage: BaseStorageProvider) -> None:
        self._journal = journal
        self._quote = quote
        self._storage = storage

    def ask(self, question):
        self.print(question.content())
        for idx in range(0, question.total_answers):
            id = idx + 1
            question.answer(id, input(f'\n {id}. '))

    def prompt(self):
        self.print(self._journal.header_title(), 1)

        self._quote.load()

        if (self._quote.content() and self._quote.author()):
            self.print(f'"{self._quote.content()}"')
            self.print(f'~ {self._quote.author()}', 1)

        if self._storage.exists(self._journal):
            for question in self._journal.night_questions():
                self.ask(question)
        else:
            for question in self._journal.day_questions():
                self.ask(question)

    def save(self):
        self._storage.save(self._journal, self._quote)

    def print(self, str, n=2):
        newlines = n * '\n'
        print(f"{newlines} {str}")
