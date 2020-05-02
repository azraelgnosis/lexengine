import sqlite3
class Row(sqlite3.Row):
    def __init__(self, cursor, values):
        self.cursor = cursor
        self.values = values
        self.columns = [col[0] for col in cursor.description]
        
        for col, val in zip(self.columns, self.values):
            setattr(self, col, val)

    def __repr__(self): return ", ".join([f"{key}: {self[key]}" for key in self.keys()])


class Model:
    __slots__ = []

    def __init__(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)
        
        self._init()
    
    def _init(self): ...

    @classmethod
    def from_row(cls, row:Row) -> None:
        # new_obj = cls()

        # for key in row.keys():
        #     setattr(new_obj, key, row[key])

        return cls(**{key: row[key] for key in row.keys()})


class Table(Model):
    __slots__ = ['db', 'name', 'columns', 'size', 'rows']
    def __init__(self, name:str, db:sqlite3.Connection) -> None:
        self.name = name
        self.db = db

        self.columns = []
        self.size = -1

        self._set_columns()
        self._set_size()

    def _set_columns(self) -> None:
        """
        Retrieves the table columns from the database and assigns them to `self.columns` as a list.
        """

        cursor = self.db.execute(f"SELECT * FROM {self.name}")
        self.columns = [col[0] for col in cursor.description]

    def _set_size(self) -> None:
        """
        Retrieves the number of rows from database and assigns that to `self.size`.
        """

        self.size = self.db.execute(
                f"SELECT COUNT(*) AS count FROM {self.name}"
            ).fetchone()['count']

    def __len__(self): return self.size
    def __repr__(self): return f"{self.name}: {', '.join(self.columns)}"


class Word:
    __slots__ = ["word_id", "word", "IPA", "lexeme", "inflection", "ancestor", "language"]

    def __init__(self, word_id=None, word=None, IPA=None, lexeme=None, inflection=None, ancestor=None, language=None):
        self.word_id = word_id
        self.word = word
        self.IPA = IPA
        self.lexeme = lexeme
        self.inflection = inflection
        self.ancestor = ancestor
        self.language = language

    def CSV(self):
        return f"{self.word_id},{self.word},{self.IPA},{self.lexeme},{self.inflection},{self.ancestor},{self.language}"

    def JSON(self):
        json = {
            "word_id": self.word_id,
            "word": self.word,
            "IPA": self.IPA,
            "lexeme": self.lexeme,
            "inflection": self.inflection,
            "ancestor": self.ancestor,
            "language": self.language
        }

        return json

class Lexeme:
    __slots__ = ["lexeme_id", "lexeme", "lemma", "language"]

    def __init__(self, lexeme_id, lexeme, lemma, language):
        self.lexeme_id = lexeme_id
        self.lexeme = lexeme
        self.lemma = lemma
        self.language = language
    
    def CSV(self):
        return f"{self.lexeme_id},{self.lexeme},{self.lemma},{self.language}"

    def JSON(self):
        json = {
            "lexeme_id": self.lexeme_id,
            "lexeme": self.lexeme,
            "lemma": self.lemma,
            "language": self.language
        }

        return json


class Language(Model):
    __slots__ = ["language_id", "name", "eng_name", "ancestor_id", "ancestor", "iso_639_1", "iso_639_2", "iso_639_3"]


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

class Dialect:
    __slots__ = ["dialect_id", "dialect", "language"]

    def __init__(self, dialect_id, dialect, language):
        self.dialect_id = dialect_id
        self.dialect = dialect
        self.language = language

    def CSV(self):
        return f"{self.dialect_id},{self.dialect},{self.language}"

    def JSON(self):
        json = {
            "dialect_id": self.dialect_id,
            "dialect": self.dialect,
            "language": self.language
        }

        return json