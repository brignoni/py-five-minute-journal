from config import NAME, DAY_QUESTIONS, NIGHT_QUESTIONS, PREFIX
import PyFiveMinuteJournal

def main():

    journal = PyFiveMinuteJournal.Journal(
        NAME,
        DAY_QUESTIONS,
        NIGHT_QUESTIONS,
        PREFIX
    )

    journal.open()

    journal.save()


if __name__ == '__main__':
    main()
