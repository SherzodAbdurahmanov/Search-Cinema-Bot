# database.py
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database/messages.db')
    return conn


def store_user_message(user_id, message_text):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO user_messages (user_id, message_text)
        VALUES (?, ?)
    ''', (user_id, message_text))

    conn.commit()
    conn.close()


def get_user_message_history(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT message_text, timestamp
        FROM user_messages
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 10
    ''', (user_id,))

    messages = cursor.fetchall()
    conn.close()

    return messages
