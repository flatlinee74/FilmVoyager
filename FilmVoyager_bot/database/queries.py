def get_random_movie():
    return """
        SELECT * FROM movies 
        WHERE titleType='movie'
            AND numVotes >= 50000
        ORDER BY RANDOM() LIMIT 1
    """

GET_TOP_100_MOVIES = """
    SELECT 
        primaryTitle,
        startYear,
        averageRating
    FROM movies
    WHERE titleType = 'movie'
      AND averageRating IS NOT NULL
      AND numVotes >= 50000
    ORDER BY averageRating DESC
    LIMIT 100;
"""
GET_TOP_100_SERIES = """
    SELECT primaryTitle, startYear, averageRating
    FROM movies
    WHERE titleType IN ('tvShow', 'tvMiniSeries', 'tvSeries')
      AND averageRating IS NOT NULL
      AND numVotes >= 10000
    ORDER BY averageRating DESC
    LIMIT 100;
"""

GET_GENRES = """
    SELECT id, name FROM genres ORDER BY name;
"""

def GET_MOVIES_BY_GENRE_IDS(genre_ids, limit=20, offset=0):
    placeholders = ",".join(map(str, genre_ids))
    return f"""
        SELECT m.primaryTitle, m.startYear, m.averageRating
        FROM movies m
        JOIN movie_genres mg ON m.tconst = mg.movie_id
        WHERE mg.genre_id IN ({placeholders})
          AND m.titleType = 'movie'
          AND m.numVotes >= 10000
        GROUP BY m.tconst
        HAVING COUNT(DISTINCT mg.genre_id) = {len(genre_ids)}
        ORDER BY m.averageRating DESC
        LIMIT {limit} OFFSET {offset};
    """

def COUNT_GENRE_MOVIES(genre_ids):
    placeholders = ",".join(map(str, genre_ids))
    return f"""
        SELECT COUNT(*) FROM (
            SELECT m.tconst
            FROM movies m
            JOIN movie_genres mg ON m.tconst = mg.movie_id
            WHERE mg.genre_id IN ({placeholders})
              AND m.titleType = 'movie'
              AND m.numVotes >= 10000
            GROUP BY m.tconst
            HAVING COUNT(DISTINCT mg.genre_id) = {len(genre_ids)}
        ) sub;
    """

GET_NEWEST_MOVIES = """
    SELECT primaryTitle, startYear, averageRating
    FROM movies
    WHERE startYear IS NOT NULL
      AND titleType = 'movie'
    ORDER BY startYear DESC, primaryTitle ASC
    LIMIT ? OFFSET ?;
"""


def SEARCH_MOVIE_BY_TITLE(query):
    return f"""
        SELECT m.tconst, m.primaryTitle, m.titleType, m.startYear, m.endYear,
               m.averageRating, m.numVotes, m.runtimeMinutes
        FROM movies m
        WHERE m.primaryTitle LIKE '%{query}%'
          AND m.titleType IN ('movie', 'tvShow', 'tvSeries', 'tvMiniSeries', 'short', 'tvMovie')
          AND m.numVotes >= 1000
        ORDER BY m.averageRating DESC
        LIMIT 10;
    """


GET_GENRES_FOR_MOVIE = """
    SELECT g.name
    FROM movie_genres mg
    JOIN genres g ON mg.genre_id = g.id
    WHERE mg.movie_id = ?;
"""


GET_DIRECTORS_FOR_MOVIE = """
    SELECT p.primaryName
    FROM directors d
    JOIN persons p ON d.nconst = p.nconst
    WHERE d.tconst = ?
    LIMIT 5;
"""


GET_WRITERS_FOR_MOVIE = """
    SELECT p.primaryName
    FROM writers w
    JOIN persons p ON w.nconst = p.nconst
    WHERE w.tconst = ?
    LIMIT 5;
"""

GET_FAVORITES = """
    SELECT movie_id FROM favorites WHERE user_id = ?
"""

GET_MOVIE_BY_ID = """
    SELECT primaryTitle, startYear, averageRating
    FROM movies
    WHERE tconst = ?
"""