DROP TABLE IF EXISTS languages;
DROP TABLE IF EXISTS lexemes;
DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS map_glosses;
DROP TABLE IF EXISTS definitions;
DROP TABLE IF EXISTS dialects;
DROP TABLE IF EXISTS pronunciations;
DROP TABLE IF EXISTS grapheme;


CREATE TABLE language (
	language_id INTEGER PRIMARY KEY AUTOINCREMENT,
	language_val TEXT,
	eng_name TEXT NOT NULL,
	ancestor_id INTEGER,
	iso_639_1 TEXT,
	iso_639_2 TEXT,
	iso_639_3 TEXT,
	FOREIGN KEY (ancestor_id) REFERENCES language (language_id)
);

CREATE TABLE word (
	word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	is_lemma INTEGER NOT NULL,
	lemma_id INTEGER NOT NULL,
	FOREIGN KEY (lemma_id) REFERENCES word (word_id),
	FOREIGN KEY (language_id) REFERENCES language (language_id)
);

CREATE TABLE map_glosses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	gloss_id INTEGER NOT NULL,
	word_id INTEGER NOT NULL,
	FOREIGN KEY (gloss_id) REFERENCES word (word_id),
	FOREIGN KEY (word_id) REFERENCES word (word_id)
);

CREATE TABLE definition (
	definition_id INTEGER PRIMARY KEY AUTOINCREMENT,
	definition_val TEXT NOT NULL,
	word_id INTEGER NOT NULL,
	FOREIGN KEY (word_id) REFERENCES word (word_id)
);

CREATE TABLE dialect (
	dialect_id INTEGER PRIMARY KEY AUTOINCREMENT,
	dialect_val TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	FOREIGN KEY (language_id) REFERENCES language (language_id)
);

CREATE TABLE pronunciation (
	pronunciation_id INTEGER PRIMARY KEY AUTOINCREMENT,
	pronunciation_val TEXT NOT NULL,
	language_id INTEGER NOT NULL,
	dialect_id INTEGER,
	word_id INTEGER,
	FOREIGN KEY (language_id) REFERENCES language (language_id),
	FOREIGN KEY (dialect_id) REFERENCES dialect (dialect_id)
	FOREIGN KEY (word_id) REFERENCES word (word_id)
);

CREATE TABLE script (
	script_id INTEGER PRIMARY KEY AUTOINCREMENT,
	script_val TEXT NOT NULL
);

CREATE TABLE grapheme (
	grapheme_id INTEGER PRIMARY KEY AUTOINCREMENT,
	grapheme_val TEXT NOT NULL,
	script_id INTEGER NOT NULL,
	FOREIGN KEY (script_id) REFERENCES script (script_id)
);