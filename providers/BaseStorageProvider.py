

class BaseStorageProvider:

    def exists(self, journal):
        print('Must implement exists method')

    def save_day(self, journal, quote):
        print('Must implement save_day method')

    def save_night(self, journal):
        print('Must implement save_night method')
