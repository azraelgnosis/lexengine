from abc import ABC
import sqlite3

from lorekeeper import Model, Row


class Word(Model):
    __slots__ = ["word_id", "word", "IPA", "is_lemma", "lemma_id", "inflection", "ancestor", "language"]


class Lexeme:
    __slots__ = ["lemma", "language"]

class Language(Model):
    __slots__ = ["language_id", "language_val", "eng_name", "ancestor_id", "ancestor", "iso_639_1", "iso_639_2", "iso_639_3", "dialects"]
    columns = ['language_val', 'eng_name', 'ancestor_id', 'iso_639_1', 'iso_639_2', 'iso_639_3']
    # rename = {"language_val": "name"}


class Pronunciation:
    __slots__ = ["pronunciation_id", "IPA", "language", "dialect"]

    def __init__(self, pronunciation_id, IPA, language, dialect):
        self.pronunciation_id = pronunciation_id
        self.IPA = IPA
        self.language = language
        self.dialect = dialect

    def CSV(self):
        return f"{self.pronunciation_id},{self.IPA},{self.language},{self.dialect}"

    def JSON(self):
        json = {
            "pronunciation_id": self.pronunciation_id,
            "IPA": self.IPA,
            "language": self.language,
            "dialect": self.dialect
        }

        return json


class Morpheme:
    __slots__ = ["morpheme_id", "morpheme", "abbreviation"]

    def __init__(self, morpheme_id, morpheme, abbreviation):
        self.morpheme_id = morpheme_id
        self.morpheme = morpheme
        self.abbreviation = abbreviation

    def CSV(self):
        return f"{self.morpheme_id},{self.morpheme},{self.abbreviation}"

    def JSON(self):
        json = {
            "morpheme_id": self.morpheme_id,
            "morpheme": self.morpheme,
            "abbreviation": self.abbreviation
        }

        return json


class Inflection:
    __slots__ = ["inflection_id", "inflection", "morpheme", "language"]

    def __init__(self, inflection_id, inflection, morpheme, language):
        self.inflection_id = inflection_id
        self.inflection = inflection
        self.morpheme = morpheme
        self.language = language

    def CSV(self):
        return f"{self.inflection_id},{self.inflection},{self.morpheme},{self.language}"

    def JSON(self):
        json = {
            "inflection_id": self.inflection_id,
            "inflection": self.inflection,
            "morpheme": self.morpheme,
            "language": self.language
        }

        return json


class Dialect(Model):
    __slots__ = ["dialect_id", "dialect_val", "language_id"]
