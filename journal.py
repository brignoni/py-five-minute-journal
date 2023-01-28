import config
from providers.MarkdownStorageProvider import MarkdownStorageProvider
from providers.ZenQuoteProvider import ZenQuoteProvider
from PyFiveMinuteJournal import Journal, JournalCommandLine

def main():

    journal = Journal(
        config.NAMESPACE,
        config.TITLE,
        config.DAY_QUESTIONS,
        config.NIGHT_QUESTIONS,
        config.DEFAULT_TOTAL_ANSWERS
    )

    storage = MarkdownStorageProvider(
        config.OUTPUT_DIR,
        config.TEMPLATE_DIR,
        config.HEADER_TEMPLATE,
        config.QUESTION_TEMPLATE
    )

    quote = ZenQuoteProvider()

    quote_cli = JournalCommandLine(
        journal,
        quote,
        storage,
        config.MESSAGES
    )

    quote_cli.prompt()

    quote_cli.save()


if __name__ == '__main__':
    main()
