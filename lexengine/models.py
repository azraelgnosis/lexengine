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

class Language:
    __slots__ = ["lang_id", "language", "eng_name", "ancestor", "iso_639_1", "iso_639_2", "iso_639_3"]
	
    def __init__(self, lang_id=None, language=None, eng_name=None, ancestor=None, iso_639_1=None, iso_639_2=None, iso_639_3=None):
        self.lang_id = lang_id
        self.language = language
        self.eng_name = eng_name
        self.ancestor = ancestor
        self.iso_639_1 = iso_639_1
        self.iso_639_2 = iso_639_2
        self.iso_639_3 = iso_639_3

    def CSV(self):
        return f"{self.lang_id},{self.language},{self.eng_name},{self.ancestor},{self.iso_639_1},{self.iso_639_2},{self.iso_639_3}"

    def JSON(self):
        json = {
            "lang_id": self.lang_id,
            "language": self.language,
            "eng_name": self.eng_name,
            "ancestor": self.ancestor,
            "iso_639_1": self.iso_639_1,
            "iso_639_2": self.iso_639_2,
            "iso_639_3": self.iso_639_3
        }

        return json

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