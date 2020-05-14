DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS lexemes;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS map_glosses;
DROP TABLE IF EXISTS definitions;
DROP TABLE IF EXISTS dialects;
DROP TABLE IF EXISTS pronunciations;


CREATE TABLE languages (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	val TEXT,
	eng_name TEXT NOT NULL,
	ancestor_id INTEGER,
	iso_639_1 TEXT,
	iso_639_2 TEXT,
	iso_639_3 TEXT,
	FOREIGN KEY (ancestor_id) REFERENCES languages (id)
);

CREATE TABLE lexemes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	lemma_id INTEGER NOT NULL,
	language_id INTEGER NOT NULL,
	ancestor_id INTEGER,
	FOREIGN KEY (language_id) REFERENCES languages (id),
	FOREIGN KEY (lemma_id) REFERENCES words (id),
	FOREIGN KEY (ancestor_id) REFERENCES words (id)
);

CREATE TABLE words (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT NOT NULL,
	lexeme_id INTEGER,
	language_id INTEGER NOT NULL,
	FOREIGN KEY (lexeme_id) REFERENCES lexemes (id),
	FOREIGN KEY (language_id) REFERENCES languages (id)
);

CREATE TABLE map_glosses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	gloss_id INTEGER NOT NULL,
	word_id INTEGER NOT NULL,
	FOREIGN KEY (gloss_id) REFERENCES words (id),
	FOREIGN KEY (word_id) REFERENCES words (id)
);

CREATE TABLE definitions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	val TEXT NOT NULL,
	word_id INTEGER NOT NULL,
	FOREIGN KEY (word_id) REFERENCES words (id)
);

CREATE TABLE dialects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	val TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	FOREIGN KEY (language_id) REFERENCES languages (id)
);

CREATE TABLE pronunciations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	val TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	dialect_id INTEGER,
	word_id INTEGER,
	FOREIGN KEY (language_id) REFERENCES languages (id),
	FOREIGN KEY (dialect_id) REFERENCES dialects (id)
	FOREIGN KEY (word_id) REFERENCES words (id)
);