from datetime import datetime
import json
import requests

QUOTE_API = 'https://zenquotes.io/api/today'

TITLE = 'FIVE MINUTE JOURNAL'

class Printable:
    def __init__(self) -> None:
        pass

    def print(self, str, n=2):
        newlines = n * '\n'
        print(f"{newlines} {str}")


class Journal(Printable):

    def __init__(self, name: str, day_questions: list, night_questions: list, prefix: str) -> None:
        self.name = name
        self.datetime = datetime.today()
        self.prefix = prefix
        self.day_questions = list(map(Question, day_questions))
        self.night_questions = list(map(Question, night_questions))

    def year(self):
        return self.datetime.year
    
    def iso_date(self):
        return  self.datetime.strftime("%Y-%m-%d")

    def pretty_date(self):
        return self.datetime.strftime('%A, %b %w %Y %I:%M %p')

    def open(self):

        self.print(f'{self.name} | {self.pretty_date()}', 1)

        self.quote = Quote()
        self.quote.load().print()

        for day_question in self.day_questions:
            day_question.ask()
            
        self.print('')

    def markdown(self):
        md = f'# {self.name}\n\n{self.pretty_date()}\n\n'
        md += self.quote.markdown()
        for day_question in self.day_questions:
            md += day_question.markdown()
        return md

    def save(self):
        file = open(f'journals/{self.year()}/{self.prefix}{self.iso_date()}.md', 'w+')
        file.write(self.markdown())
        file.close()


class Question(Printable):

    def __init__(self, question, total_answers=3) -> None:
        self.question = question
        self.total_answers = total_answers
        self.quote = None
        self.answers = []

    def ask(self):
        self.print(self.content())
        for idx in range(0, self.total_answers):
            self.answers.append(Answer(idx))

    def content(self):
        return self.question

    def markdown(self) -> str:
        md = f'## {self.content()}\n\n'
        if len(self.answers) > 0:
            for answer in self.answers:
                md += answer.markdown()
        else:
            md += 'No answer.\n'
        return md + '\n\n'

    def __str__(self) -> str:
        answers = '\n '.join(map(str, self.answers))
        return f"<Question content='{self.question}'>\n {answers}\n</Question>"


class Answer:

    def __init__(self, idx) -> None:
        self.idx = idx
        self.answer = input(f'\n {idx + 1}. ')

    def id(self):
        return f'{self.idx + 1}'

    def content(self):
        return self.answer

    def markdown(self):
        return f'{self.id()}. {self.content()}\n'

    def __str__(self) -> str:
        return f'<Answer id={self.id()} content="{self.content()}"/>'


class Quote(Printable):

    def __init__(self) -> None:
        pass

    def load(self):
        quote_response = requests.get(QUOTE_API)
        data = json.loads(quote_response.content)
        self.quote = data[0]['q']
        self.author = data[0]['a']
        return self

    def markdown(self):
        return '> ' + ('\n> '.join([
            self.quote,
            '',
            f'~ {self.author}'
        ])) + '\n\n\n'

    def print(self):
        if (self.quote and self.author):
            super().print(f'"{self.quote}"')
            super().print(f'~ {self.author}', 1)
