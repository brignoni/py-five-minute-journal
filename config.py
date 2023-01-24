import gettext
import i18n
from dotenv import load_dotenv
from os import getenv, environ

load_dotenv()

i18n.load_path.append('locales')
i18n.set('locale', getenv('LOCALE', 'en'))
i18n.set('fallback', 'en')
_ = i18n.t


def multiline(value: str):
    return list(filter(lambda s: s, value.split("\n")))


MESSAGES = {
    'complete': _("journal.complete"),
    'saved': _("journal.saved"),
}

TITLE = getenv('TITLE', _('journal.title'))

NAMESPACE = getenv('NAMESPACE', '5MJ')

DAY_QUESTIONS = multiline(getenv('DAY_QUESTIONS', "\n".join([
    _('journal.questions.i_am_grateful_for'),
    _('journal.questions.what_would_make_today_great'),
    _('journal.questions.daily_affirmations'),
])))

NIGHT_QUESTIONS = multiline(getenv('NIGHT_QUESTIONS', '\n'.join([
    _('journal.questions.highlights_of_the_day'),
    _('journal.questions.what_did_i_learn_today'),
])))

DEFAULT_TOTAL_ANSWERS = int(getenv('DEFAULT_TOTAL_ANSWERS', '3'))

HEADER_TEMPLATE = getenv('HEADER_TEMPLATE', 'header-template.md')
QUESTION_TEMPLATE = getenv('QUESTION_TEMPLATE', 'question-template.md')

OUTPUT_DIR = getenv('OUTPUT_DIR', 'journals')
