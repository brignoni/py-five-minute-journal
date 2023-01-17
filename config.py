from os import getenv
from dotenv import load_dotenv

load_dotenv()

def multiline(value: str):
    return  list(filter(lambda s: s, value.split("\n")))

NAME = getenv('NAME', 'Five Minute Journal')

PREFIX = getenv('PREFIX', '5MJ-')

DAY_QUESTIONS = multiline(getenv('DAY_QUESTIONS', '\n'.join([
    'I am grateful for...',
    'What would make today great?'
    'Daily affirmations'
])))

NIGHT_QUESTIONS = multiline(getenv('NIGHT_QUESTIONS', '\n'.join([
    'Highlights of the day'
    'What did I learn today?'
])))

DEFAULT_ANSWER_COUNT = int(getenv('DEFAULT_ANSWER_COUNT', '3'))

OUTPUT_DIR = getenv('OUTPUT_DIR', 'journals')

# TIMEZONE