import sqlite3


def execute(query, db_path, *params):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception:
        raise
    finally:
        conn.close()

    return result
