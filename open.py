import OneMinute


def main():

    journal = OneMinute.Journal()

    journal.open()
    
    journal.save()


if __name__ == '__main__':
    main()
