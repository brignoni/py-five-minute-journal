import requests
from dataclasses import dataclass, field
from datetime import datetime
from pydash.objects import get


@dataclass
class Answer:
    id: int
    text: str


@dataclass
class Question:
    text: str
    answers: list[Answer] = field(default_factory=lambda: [])
    def __len__(self):
        return len(self.answers)


@dataclass
class JournalQuestions:
    day: list[str] = field(default_factory=lambda _: [])
    night: list[str] = field(default_factory=lambda _: [])


@dataclass
class JournalConfig:
    default_questions: JournalQuestions
    namespace: str
    messages: str
    quote_api: str
    quote_author: str
    quote_text: str
    title: str
    total_answers: int


@dataclass
class JournalQuote:
    author: str
    text: str


class Journal:

    _questions_day: list[Question] = []
    _questions_night: list[Question] = []

    def __init__(
        self, 
        config: JournalConfig,
    ) -> None:
        self.config = config
        self.datetime = datetime.today()

    def message(self, key: str):
        return self.config.messages.get(key)

    def add_questions(self, questions: JournalQuestions):
        for question in questions.day:
            self._questions_day.append(Question(text=question))
        for question in questions.night:
            self._questions_night.append(Question(text=question))

    def namespace(self) -> str:
        return self.config.namespace

    def id(self) -> str:
        return f'{self.config.namespace}-{self.datetime.strftime("%Y-%m-%d")}'

    def title(self) -> str:
        return self.config.title

    def year(self) -> int:
        return self.datetime.year

    def year_month_day(self) -> str:
        return self.datetime.strftime("%Y-%m-%d")

    def time(self) -> str:
        return f'---\n{self.datetime.strftime("%I:%M %p")}'

    def date(self) -> str:
        return self.datetime.strftime('%A, %b %d %Y')

    def header_title(self) -> str:
        return f'{self.title()} | {self.date()}'

    def questions_day(self):
        return self._questions_day

    def questions_night(self):
        return self._questions_night

    def answer(self, question: Question, id: str, answer: str):
        if len(answer) > 0:
            question.answers.append(Answer(id, answer))

    def total_answers(self) -> int:
        return self.config.total_answers

    def __len__(self):
        return len(self.questions_day()) + len(self.questions_night())


class JournalPlugin:

    def __init__(self, config: JournalConfig) -> None:
        self.config = config

    def quote(self) -> JournalQuote:
        response = requests.get(self.config.quote_api).json()
        return JournalQuote(
            author=get(response, self.config.quote_author),
            text=get(response, self.config.quote_text),
        )

    def questions(self) -> JournalQuestions:
        return self.config.default_questions