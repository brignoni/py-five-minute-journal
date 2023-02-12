from fiveminutejournal import (
    NAMESPACE,
    MESSAGES,
    HEADER_TEMPLATE,
    OUTPUT_DIR,
    ROOT_DIR,
    QUESTION_TEMPLATE,
    QUOTE_API,
    QUOTE_AUTHOR,
    QUOTE_TEXT,
    QUESTIONS_DAY,
    QUESTIONS_NIGHT,
    TITLE,
    TOTAL_ANSWERS,
)
from fiveminutejournal.utils import get_plugin
from fiveminutejournal.console import JournalConsole
from fiveminutejournal.storage import MarkdownJournalStorage
from fiveminutejournal.journal import (
    Journal,
    JournalConfig,
    JournalQuestions,
)

def main():

    default_questions = JournalQuestions(
        day=QUESTIONS_DAY,
        night=QUESTIONS_NIGHT,
    )

    config = JournalConfig(
        default_questions=default_questions,
        namespace=NAMESPACE,
        messages=MESSAGES,
        quote_api=QUOTE_API,
        quote_author=QUOTE_AUTHOR,
        quote_text=QUOTE_TEXT,
        title=TITLE,
        total_answers=TOTAL_ANSWERS,
    )

    plugin = get_plugin(config=config, name='default')

    journal = Journal(config)

    storage = MarkdownJournalStorage(
        root_dir=ROOT_DIR,
        output_dir=OUTPUT_DIR,
        header_template=HEADER_TEMPLATE,
        question_template=QUESTION_TEMPLATE,
    )

    console = JournalConsole(
        journal=journal,
        plugin=plugin,
        storage=storage,
    )

    console.prompt()

    console.save()


if __name__ == '__main__':
    main()
