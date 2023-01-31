import os
import re
import shutil
from pathlib import Path
from providers.BaseStorageProvider import BaseStorageProvider
from jinja2 import Environment, FileSystemLoader, select_autoescape


class MarkdownStorageProvider(BaseStorageProvider):

    TIME_REGEX = r'---\n(\d{2}:\d{2})'

    def __init__(self, root_dir: str, output_dir: str, header_template: str, question_template: str) -> None:
        self._root_dir = root_dir
        self._output_dir = output_dir
        self.copy_template(header_template)
        self.copy_template(question_template)
        self._env = Environment(
            loader=FileSystemLoader(output_dir),
            autoescape=select_autoescape()
        )
        self._header_template = self._env.get_template(header_template)
        self._question_template = self._env.get_template(question_template)

    def year_path(self, journal):
        return f'{self._output_dir}/{journal.year()}'

    def file_path(self, journal):
        return f'{self.year_path(journal)}/{journal.id()}.md'

    def template_realpath(self, filename: str):
        return os.path.realpath(f'{self._output_dir}/{filename}')

    def has_template(self, filename: str):
        path = Path(self.template_realpath(filename))
        try:
            path.read_text()
            return True
        except FileNotFoundError:
            return False

    def copy_template(self, filename: str):
        if not self.has_template(filename):
            shutil.copyfile(f'{self._root_dir}/journals/{filename}', self.template_realpath(filename))

    def filled_times(self, journal, count: int):
        filepath = self.file_path(journal)
        file = Path(filepath)
        try:
            content = file.read_text()
            matches = re.findall(self.TIME_REGEX, content)
            return len(matches) == count
        except FileNotFoundError:
            return False

    def filled_once(self, journal):
        return self.filled_times(journal, 1)

    def filled_twice(self, journal):
        return self.filled_times(journal, 2)

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

    def save(self, journal, quote):
        if self.filled_once(journal) and len(journal) > 0:
            self.save_night(journal)
        elif not self.filled_twice(journal) and len(journal) > 0:
            self.save_day(journal, quote)

    def save_day(self, journal, quote):

        output = self._header_template.render(
            author=quote.author(),
            quote=quote.content(),
            title=journal.title(),
            date=journal.pretty_date()
        ) + '\n\n' + self._question_template.render(
            time=journal.iso_time(),
            questions=self.day_questions(journal)
        )

        if not os.path.exists(self.year_path(journal)):
            os.makedirs(self.year_path(journal))

        file = open(self.file_path(journal), 'w+')
        file.write(output)
        file.close()

    def save_night(self, journal):

        output = self._question_template.render(
            time=journal.iso_time(),
            questions=self.night_questions(journal)
        )

        file = open(self.file_path(journal), 'a')
        file.write(output)
        file.close()
