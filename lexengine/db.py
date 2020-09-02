from flask import current_app

from lorekeeper import LoreKeeper

from lexengine.models import Language, Word

PATH_DB = 'DATABASE'


class LexLoreKeeper(LoreKeeper):
    def __init__(self):
        super().__init__(PATH_DB)
        self.class_map = {
            "languages": Language
        }

    def get_languages(self, where:dict=None) -> list:
        """
        SELECT language.language_id, language.language_val AS name, eng_name, ancestor.language_val AS ancestor, iso_639_1, iso_639_2, iso_639_3
                FROM `language`
                LEFT JOIN (SELECT id, val FROM `language`) AS ancestor ON ancestor.language_id = language.ancestor_id
                [WHERE `where`]
        """

        query = """
            SELECT language.language_id, language.language_val AS name, eng_name, ancestor.language_val AS ancestor, iso_639_1, iso_639_2, iso_639_3
                FROM `language`
                LEFT JOIN (SELECT id, val FROM `language`) AS ancestor ON ancestor.language_id = language.ancestor_id
            """.replace("\n", " ")

        if where:
            query += " WHERE {WHERE}".format(
                WHERE=self._where(table='languages', conditions=where))

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
