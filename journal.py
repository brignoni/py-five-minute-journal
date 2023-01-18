import config 
# import NAMESPACE, TITLE, DAY_QUESTIONS, NIGHT_QUESTIONS, OUTPUT_DIR
from providers.MarkdownStorageProvider import MarkdownStorageProvider
from PyFiveMinuteJournal import Quote, Journal, JournalCommandLine

def main():
    
    journal = Journal(
        config.NAMESPACE,
        config.TITLE,
        config.DAY_QUESTIONS,
        config.NIGHT_QUESTIONS
    )

    storage = MarkdownStorageProvider(
        config.OUTPUT_DIR, 
        config.HEADER_TEMPLATE,
        config.QUESTION_TEMPLATE
    )

    quote = Quote()

    quote_cli = JournalCommandLine(
        journal,
        quote,
        storage
    )

    quote_cli.prompt()

    quote_cli.save()


if __name__ == '__main__':
    main()
