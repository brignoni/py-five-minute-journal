

class BaseStorageProvider:

    def transform_answer(self, a):
        return a

    def transform_question(self, q):
        return q

    def day_questions(self, journal):
        return list(map(self.transform_question, filter(len, journal.day_questions())))

    def night_questions(self, journal):
        return list(map(self.transform_question, filter(len, journal.night_questions())))

    def save(self, journal, quote):
        print('Must implement save method')
