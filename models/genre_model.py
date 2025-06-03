from db import get_connection

def get_all_genres():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM Genre").fetchall()

def add_genre(name):
    with get_connection() as conn:
        conn.execute("INSERT INTO Genre (name) VALUES (?)", (name,))

def update_genre(id, name):
    with get_connection() as conn:
        conn.execute("UPDATE Genre SET name = ? WHERE id = ?", (name, id))

def delete_genre(id):
    with get_connection() as conn:
        conn.execute("DELETE FROM Genre WHERE id = ?", (id,))
