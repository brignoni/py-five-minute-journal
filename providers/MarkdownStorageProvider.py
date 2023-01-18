import os
from pathlib import Path
from providers.BaseStorageProvider import BaseStorageProvider
from jinja2 import Environment, PackageLoader, select_autoescape


class MarkdownStorageProvider(BaseStorageProvider):

    def __init__(self, dir: str, header_template: str, question_template: str) -> None:
        self._dir = dir
        env = Environment(
            loader=PackageLoader('journal', dir),
            autoescape=select_autoescape()
        )
        self._header_template = env.get_template(header_template)
        self._question_template = env.get_template(question_template)

    def year_path(self, journal):
        return f'{self._dir}/{journal.year()}'

    def file_path(self, journal):
        return f'{self.year_path(journal)}/{journal.id()}.md'

    def exists(self, journal):
        file = Path(self.file_path(journal))
        return file.is_file()

    # def markdown_quote(self, quote):
    #     return '> ' + ('\n> '.join([
    #         quote.quote(),
    #         '',
    #         f'~ {quote.author()}'
    #     ])) + '\n\n\n'

    # def markdown_question(self, question):
    #     pass

    def transform_answer(self, a):
        return {
            'id': a.id(), 
            'content': a.content() 
        }

    def transform_question(self, q):
        return {
            'content': q.content(),
            'answers': map(self.transform_answer, q.answers()),
        }

    def questions(self):
        return []

    def day_questions(self, journal):
        return map(self.transform_question, journal.day_questions())

    def night_questions(self, journal):
        return map(self.transform_question, journal.night_questions())

    def markdown(self, journal, quote):
        output = ''
        
        if self.exists(journal):
            output += self._header_template.render(
                author=quote.author(),
                quote=quote.content(),
                title=journal.title(),
                date=journal.pretty_date()
            )
            output += '\n' + self._question_template.render(
                questions=self.day_questions(journal)
            )
        else:
            output += '\n' + self._question_template.render(
                questions=self.night_questions(journal)
            )
        
        return output

    def save(self, journal, quote):        
        if self.exists(journal):
            self.save_night(journal)
        else:
            self.save_day(journal, quote)

    def save_day(self, journal, quote):

        output = self.markdown(journal, quote)

        if not os.path.exists(self.year_path(journal)):
            os.makedirs(self.year_path(journal))

        file = open(self.file_path(journal), 'w+')
        file.write(output)
        file.close()

    def save_night(self, journal):
        pass
