import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash


BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "security_system.db"


def get_connection():

    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            input_text TEXT NOT NULL,
            persona TEXT NOT NULL,
            privacy_risk TEXT NOT NULL,
            leakage_risk TEXT NOT NULL,
            detected_data TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    connection.commit()

    connection.close()


def create_user(username, password):

    connection = get_connection()

    try:

        hashed_password = generate_password_hash(password)

        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


def verify_user(username, password):

    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    if user and check_password_hash(
        user["password"],
        password
    ):

        return dict(user)

    return None


def save_analysis(
    user_id,
    input_text,
    persona,
    privacy_risk,
    leakage_risk,
    detected_data,
    recommendations
):

    connection = get_connection()

    connection.execute("""
        INSERT INTO analyses
        (
            user_id,
            input_text,
            persona,
            privacy_risk,
            leakage_risk,
            detected_data,
            recommendations
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        input_text,
        persona,
        privacy_risk,
        leakage_risk,
        detected_data,
        recommendations
    ))

    connection.commit()

    connection.close()


def get_user_analyses(user_id):

    connection = get_connection()

    analyses = connection.execute("""
        SELECT *
        FROM analyses
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()

    connection.close()

    return analyses
