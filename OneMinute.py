from datetime import date
import json
import requests

QUOTE_API = 'https://zenquotes.io/api/today'

TITLE = 'ONE MINUTE JOURNAL'
FILE_PREFIX = '1MJ-'

QUESTION_GRATEFUL = 'I am grateful for...'
QUESTION_WHAT = 'What would make today great?'
QUESTION_AFFIRMATION = 'Daily Affirmation'
QUESTION_HIGHLIGHTS = 'Highlights of the Day'
QUESTION_LEARN = 'What did you learn today?'


class Printable:
    def __init__(self) -> None:
        pass

    def print(self, str, n=2):
        newlines = n * '\n'
        print(f"{newlines} {str}")


class Journal(Printable):

    def __init__(self, day_questions=[
        QUESTION_GRATEFUL,
        QUESTION_WHAT,
        QUESTION_AFFIRMATION,
    ], night_questions=[
        QUESTION_HIGHLIGHTS,
        QUESTION_LEARN,
    ]) -> None:
        self.date = date.today()
        
        self.day_questions = list(map(Question, day_questions))
        self.night_questions = list(map(Question, night_questions))

    def year(self):
        return self.date.year
    
    def today(self):
        return str(self.date)

    def open(self):

        self.print(TITLE)
        self.print('Friday, Nov 11, 2022 8:30 am', 1)

        self.quote = Quote()
        self.quote.load().display()

        for day_question in self.day_questions:
            day_question.ask()
            
        self.print('')

    def markdown(self):
        md = f'# {TITLE}\n\n\n'
        md += self.quote.markdown()
        for day_question in self.day_questions:
            md += day_question.markdown()
        return md

    def save(self):
        file = open(f'.journals/{self.year()}/{FILE_PREFIX}{self.today()}.md', 'w+')
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
        for answer in self.answers:
            md += answer.markdown()
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
        return f'<Answer id={self.id()} content="{self.content()}">'


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

    def display(self):
        if (self.quote and self.author):
            self.print(f'"{self.quote}"')
            self.print(f'~ {self.author}', 1)
