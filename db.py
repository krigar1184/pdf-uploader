import sqlite3


__db_path = None


def execute(query, **params):
    conn = sqlite3.connect(__db_path)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
    except Exception:
        raise
    else:
        conn.commit()
    finally:
        conn.close()

    return result


def init(db_path):
    global __db_path
    __db_path = db_path
