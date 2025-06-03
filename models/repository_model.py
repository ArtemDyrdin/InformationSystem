from db import get_connection

def get_all_repositories():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM Repository").fetchall()

def add_repository(name, type):
    with get_connection() as conn:
        conn.execute("INSERT INTO Repository (name, type) VALUES (?, ?)", (name, type))

def update_repository(id, name, type):
    with get_connection() as conn:
        conn.execute("UPDATE Repository SET name = ?, type = ? WHERE id = ?", (name, type, id))

def delete_repository(id):
    with get_connection() as conn:
        conn.execute("DELETE FROM Repository WHERE id = ?", (id,))
