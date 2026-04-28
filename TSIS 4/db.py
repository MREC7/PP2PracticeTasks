import psycopg2
from config import load_config

DB_NAME = "snake"

def connect(db=None):
    cfg = load_config()
    if db:
        cfg["database"] = db
    return psycopg2.connect(**cfg)

def create_db():
    conn = connect("postgres")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DB_NAME}")

    cur.close()
    conn.close()

def init_db():
    create_db()
    conn = connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS players(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions(
        id SERIAL PRIMARY KEY,
        player_id INT REFERENCES players(id),
        score INT NOT NULL,
        level_reached INT NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

def save_score(username, score, level):
    conn = connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()

    if row:
        pid = row[0]
    else:
        cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
        pid = cur.fetchone()[0]

    cur.execute("""
    INSERT INTO game_sessions(player_id, score, level_reached)
    VALUES (%s,%s,%s)
    """, (pid, score, level))

    conn.commit()
    cur.close()
    conn.close()

def get_top():
    conn = connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    SELECT p.username, g.score, g.level_reached, g.played_at
    FROM game_sessions g
    JOIN players p ON p.id=g.player_id
    ORDER BY g.score DESC
    LIMIT 10
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_best(username):
    conn = connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    SELECT MAX(score)
    FROM game_sessions g
    JOIN players p ON p.id=g.player_id
    WHERE p.username=%s
    """, (username,))

    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res or 0