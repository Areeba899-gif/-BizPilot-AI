
import sqlite3


def create_database():

    connection = sqlite3.connect("database/bizpilot.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            assistant_response TEXT,
            selected_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_chat(user_message, assistant_response, selected_agent):

    connection = sqlite3.connect("database/bizpilot.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO chat_history
        (user_message, assistant_response, selected_agent)
        VALUES (?, ?, ?)
    """, (user_message, assistant_response, selected_agent))

    connection.commit()
    connection.close()


def get_chat_history():

    connection = sqlite3.connect("database/bizpilot.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT user_message, assistant_response,
               selected_agent, created_at
        FROM chat_history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history
