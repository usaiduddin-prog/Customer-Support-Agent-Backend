import sqlite3
from typing import Any, List, Dict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ecommerce.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn


def run_sql(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    except sqlite3.Error as e:
        return [{"error": str(e)}]

    finally:
        if conn:
            conn.close()