import i18n
from dotenv import load_dotenv
from os import getenv, path
import locale
from importlib import metadata

load_dotenv()

__version__ = metadata.version("fiveminutejournal")

# getting the name of the directory
# where the this file is present.
PACKAGE_DIR = path.dirname(path.realpath(__file__))
ROOT_DIR = path.dirname(path.dirname(PACKAGE_DIR))
OUTPUT_DIR = path.realpath(f"{ROOT_DIR}/{getenv('OUTPUT_DIR', 'journals')}")

i18n.load_path.append(f'{PACKAGE_DIR}/locales')
i18n.set('locale', getenv('LOCALE', 'en'))
i18n.set('fallback', 'en')
_ = i18n.t

try:
    time_locale = f'{i18n.get("locale")}_{i18n.get("locale").upper()}'
    locale.setlocale(locale.LC_TIME, time_locale)
except Exception:
    pass


def multiline(value: str):
    return list(filter(lambda s: s, value.split('\n')))


MESSAGES = {
    'complete': _('journal.complete'),
    'saved': _('journal.saved'),
}

TITLE = getenv('TITLE', _('journal.title'))

NAMESPACE = getenv('NAMESPACE', '5MJ')

QUESTIONS_DAY = multiline(getenv('QUESTIONS_DAY', '\n'.join([
    _('journal.questions.i_am_grateful_for'),
    _('journal.questions.what_would_make_today_great'),
    _('journal.questions.daily_affirmations'),
])))

QUESTIONS_NIGHT = multiline(getenv('QUESTIONS_NIGHT', '\n'.join([
    _('journal.questions.highlights_of_the_day'),
    _('journal.questions.what_did_i_learn_today'),
])))

TOTAL_ANSWERS = int(getenv('TOTAL_ANSWERS', '3'))

HEADER_TEMPLATE = getenv('HEADER_TEMPLATE', 'header-template.md')
QUESTION_TEMPLATE = getenv('QUESTION_TEMPLATE', 'question-template.md')

QUOTE_API = getenv('QUOTE_API', 'https://zenquotes.io/api/today')
QUOTE_TEXT = getenv('QUOTE_TEXT', '[0].q')
QUOTE_AUTHOR = getenv('QUOTE_AUTHOR', '[0].a')