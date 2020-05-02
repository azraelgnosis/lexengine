DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS lexemes;
DROP TABLE IF EXISTS morphological_categories;
DROP TABLE IF EXISTS morphemes;
DROP TABLE IF EXISTS inflections;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS pronunciations;
DROP TABLE IF EXISTS dialects;

CREATE TABLE languages (
	language_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	eng_name TEXT NOT NULL,
	ancestor_id INTEGER,
	iso_639_1 TEXT,
	iso_639_2 TEXT,
	iso_639_3 TEXT,
	FOREIGN KEY (ancestor_id) REFERENCES languages (language_id)
);

CREATE TABLE lexemes (
	lexeme_id INTEGER PRIMARY KEY AUTOINCREMENT,
	lemma_id INTEGER NOT NULL,
	language_id INTEGER NOT NULL,
	ancestor_id INTEGER,
	FOREIGN KEY (language_id) REFERENCES languages (language_id),
	FOREIGN KEY (lemma_id) REFERENCES words (word_id),
	FOREIGN KEY (ancestor_id) REFERENCES words (word_id)
);

CREATE TABLE morphological_categories (
	category_id INTEGER PRIMARY KEY AUTOINCREMENT,
	category TEXT NOT NULL
);

CREATE TABLE morphemes (
	morpheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
	morpheme TEXT NOT NULL,
	abbreviaiton TEXT,
	category_id INTEGER,
	FOREIGN KEY (category_id) REFERENCES morphological_categories (category_id)
);

CREATE TABLE inflections (
	inflection_id INTEGER PRIMARY KEY AUTOINCREMENT,
	inflection TEXT NOT NULL,
	morpheme_id INTEGER,
	language_id INTEGER,
	FOREIGN KEY (morpheme_id) REFERENCES morphemes (morpheme_id),
	FOREIGN KEY (language_id) REFERENCES languages (language_id)
);

CREATE TABLE words (
	word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT NOT NULL,
	lexeme_id INTEGER,
	inflection_id INTEGER,
	FOREIGN KEY (lexeme_id) REFERENCES lexemes (lexeme_id),
	FOREIGN KEY (inflection_id) REFERENCES inflections (inflection_id)
);

CREATE TABLE dialects (
	dialect_id INTEGER PRIMARY KEY AUTOINCREMENT,
	dialect TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	FOREIGN KEY (language_id) REFERENCES languages (language_id)
);

CREATE TABLE pronunciations (
	pronunciation_id INTEGER PRIMARY KEY AUTOINCREMENT,
	IPA TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	dialect_id INTEGER,
	word_id INTEGER,
	FOREIGN KEY (language_id) REFERENCES languages (language_id),
	FOREIGN KEY (dialect_id) REFERENCES dialects (dialect_id)
	FOREIGN KEY (word_id) REFERENCES words (word_id)
);