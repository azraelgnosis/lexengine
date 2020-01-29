CREATE TABLE languages (
	lang_id INTEGER PRIMARY KEY AUTOINCREMENT,
	language TEXT,
	eng_name TEXT NOT NULL,
	ancestor INTEGER,
	iso_639-1 TEXT,
	iso_639-2 TEXT,
	iso_639-3 TEXT,
	FOREIGN KEY (ancestor) REFERENCES languages (lang_id)
);

CREATE TABLE lexemes (
	lexeme_id INTEGER PRIMARY KEY AUTOINCREMENT,
	lexeme TEXT NOT NULL,
	lemma INTEGER NOT NULL,
	language INTEGER NOT NULL,
	FOREIGN KEY (language) REFERENCES languages (lang_id),
	FOREIGN KEY (lemma) REFERENCES words (word_id)
);

CREATE TABLE morphemes (
	morpheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
	morpheme TEXT NOT NULL,
	abbreviaiton TEXT,
);

CREATE TABLE inflections (
	inflection_id INTEGER PRIMARY KEY AUTOINCREMENT,
	inflection TEXT NOT NULL,
	morpheme INTEGER,
	language INTEGER,
	FOREIGN KEY (morpheme) REFERENCES morphemes (morpheme_id),
	FOREIGN KEY (language) REFERENCES languages (lang_id)
);

CREATE TABLE words (
	word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT NOT NULL,
	IPA INTEGER,
	lexeme INTEGER,
	inflection INTEGER,
	ancestor INTEGER,
	language INTEGER NOT NULL,
	FOREIGN KEY (IPA) REFERENCES pronunciations (pronunciation_id),
	FOREIGN KEY (lexeme) REFERENCES lexemes (lexeme_id),
	FOREIGN KEY (inflection) REFERENCES inflections (inflection_id),
	FOREIGN KEY (ancestor) REFERENCES words (word_id),
	FOREIGN KEY (language) REFERENCES languages (lang_id)
);

CREATE TABLE pronunciations (
	pronunciation_id INTEGER PRIMARY KEY AUTOINCREMENT,
	IPA TEXT NOT NULL,
	language INTEGER NOT NULL,
	dialect INTEGER,
	FOREIGN KEY (language) REFERENCES languages (lang_id),
	FOREIGN KEY (dialect) REFERENCES dialects (dialect_id)
);

CREATE TABLE dialects (
	dialect_id INTEGER PRIMAREY KEY AUTOINCREMENT,
	dialect TEXT NOT NULL,
	language INTEGER NOT NULL,
	FOREIGN KEY (language) REFERENCES languages (lang_id)
);