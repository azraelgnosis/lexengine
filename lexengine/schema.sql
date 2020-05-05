DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS lexemes;
DROP TABLE IF EXISTS morphological_categories;
DROP TABLE IF EXISTS morphemes;
DROP TABLE IF EXISTS inflections;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS pronunciations;
DROP TABLE IF EXISTS dialects;

CREATE TABLE languages (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
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

CREATE TABLE morphological_categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category TEXT NOT NULL
);

CREATE TABLE morphemes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	morpheme TEXT NOT NULL,
	abbreviaiton TEXT,
	category_id INTEGER,
	FOREIGN KEY (category_id) REFERENCES morphological_categories (id)
);

CREATE TABLE inflections (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	inflection TEXT NOT NULL,
	morpheme_id INTEGER,
	language_id INTEGER,
	FOREIGN KEY (morpheme_id) REFERENCES morphemes (id),
	FOREIGN KEY (language_id) REFERENCES languages (id)
);

CREATE TABLE words (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT NOT NULL,
	lexeme_id INTEGER,
	inflection_id INTEGER,
	FOREIGN KEY (lexeme_id) REFERENCES lexemes (id),
	FOREIGN KEY (inflection_id) REFERENCES inflections (id)
);

-- CREATE TABLE map_glosses (
-- 	gloss_id INTEGER PRIMARY KEY AUTOINCREMENT,

-- );

CREATE TABLE dialects (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	dialect TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	FOREIGN KEY (language_id) REFERENCES languages (id)
);

CREATE TABLE pronunciations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	IPA TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	dialect_id INTEGER,
	word_id INTEGER,
	FOREIGN KEY (language_id) REFERENCES languages (id),
	FOREIGN KEY (dialect_id) REFERENCES dialects (id)
	FOREIGN KEY (word_id) REFERENCES words (id)
);