from db import get_connection

def get_all_countries():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM Country").fetchall()

def add_country(name):
    with get_connection() as conn:
        conn.execute("INSERT INTO Country (name) VALUES (?)", (name,))

def update_country(id, name):
    with get_connection() as conn:
        conn.execute("UPDATE Country SET name = ? WHERE id = ?", (name, id))

def delete_country(id):
    with get_connection() as conn:
        conn.execute("DELETE FROM Country WHERE id = ?", (id,))
