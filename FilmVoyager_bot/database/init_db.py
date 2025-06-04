import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()


create_tables_sql = """
-- Фильмы/сериалы
CREATE TABLE IF NOT EXISTS movies(
    tconst TEXT PRIMARY KEY,
    titleType TEXT,
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult INTEGER,
    startYear INTEGER,
    endYear INTEGER,
    runtimeMinutes INTEGER,
    genres TEXT,
    averageRating REAL,
    numVotes INTEGER,
    posters_url TEXT
);

-- Жанры (многие-ко-многим)
CREATE TABLE IF NOT EXISTS genres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS movie_genres (
    movie_id TEXT,
    genre_id INTEGER,
    FOREIGN KEY(movie_id) REFERENCES movies(tconst),
    FOREIGN KEY(genre_id) REFERENCES genres(id)
);

-- Люди (актеры, режиссеры, сценаристы)
CREATE TABLE IF NOT EXISTS persons (
    nconst TEXT PRIMARY KEY,
    primaryName TEXT,
    birthYear INTEGER,
    deathYear INTEGER,
    primaryProfession TEXT,
    knownForTitles TEXT
);

-- Режиссеры
CREATE TABLE IF NOT EXISTS directors (
    tconst TEXT,
    nconst TEXT,
    FOREIGN KEY(tconst) REFERENCES movies(tconst),
    FOREIGN KEY(nconst) REFERENCES persons(nconst)
);

-- Сценаристы
CREATE TABLE IF NOT EXISTS writers (
    tconst TEXT,
    nconst TEXT,
    FOREIGN KEY(tconst) REFERENCES movies(tconst),
    FOREIGN KEY(nconst) REFERENCES persons(nconst)
);

-- Эпизоды сериалов
CREATE TABLE IF NOT EXISTS episodes (
    tconst TEXT PRIMARY KEY,
    parentTconst TEXT,
    seasonNumber INTEGER,
    episodeNumber INTEGER,
    FOREIGN KEY(tconst) REFERENCES movies(tconst),
    FOREIGN KEY(parentTconst) REFERENCES movies(tconst)
);

-- Альтернативные названия
CREATE TABLE movie_akas (
    titleId TEXT,
    title TEXT,
    region TEXT,
    language TEXT,
    type TEXT,
    FOREIGN KEY(titleId) REFERENCES movies(tconst)
);

-- Связи людей и фильмов
CREATE TABLE IF NOT EXISTS movie_crew (
    tconst TEXT,
    nconst TEXT,
    role TEXT,
    FOREIGN KEY(tconst) REFERENCES movies(tconst),
    FOREIGN KEY(nconst) REFERENCES persons(nconst)
);
"""

cursor.executescript(create_tables_sql)
conn.commit()
conn.close()
print("Таблицы созданы!")