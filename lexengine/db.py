from flask import current_app
from lorekeeper import LoreKeeper, Table

from lexengine.const import *
from lexengine.models import Dialect, Language, Word

PATH_DB = 'DATABASE'


class LexLoreKeeper(LoreKeeper):
    def __init__(self):
        super().__init__(PATH_DB)
        self._table_map = {
            TABLES.DIALECT: Dialect,
            TABLES.LANGUAGE: Language
        }

    def get_languages(self, where:dict=None) -> list:
        """
        SELECT language.language_id, language.language_val, eng_name, ancestor.language_val AS ancestor, iso_639_1, iso_639_2, iso_639_3
                FROM `language`
                LEFT JOIN (SELECT id, val FROM `language`) AS ancestor ON ancestor.language_id = language.ancestor_id
                [WHERE `where`]
        """

        query = """
            SELECT language.language_id, language.language_val, eng_name, ancestor.language_val AS ancestor, iso_639_1, iso_639_2, iso_639_3
                FROM `language`
                LEFT JOIN (SELECT language_id, language_val FROM `language`) AS ancestor ON ancestor.language_id = language.ancestor_id
            """.replace("\n", " ").strip()

        if where:
            query += " WHERE {}".format(self._where(table=TABLES.LANGUAGE, conditions=where))

        results = self.db.execute(query).fetchall()
        languages = [Language.from_row(row) for row in results]

        return languages        

    def get_language(self, language:str) -> Language:
        return self.get_languages(where=language)[0]

    def get_lexicon(self, language) -> list:
        """
        SELECT * FROM words WHERE `language`
        """
        
        query = "SELECT * FROM words WHERE {WHERE}".format(
            WHERE=self._where(language)
        )

        words = [Word.from_row(word) for word in self.fetch_all(query)]

        return words
