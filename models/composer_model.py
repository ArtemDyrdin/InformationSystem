from db import get_connection

def get_all_composers():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM Composer").fetchall()

def add_composer(first, last, middle, birth, death):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO Composer (first_name, last_name, middle_name, birth_date, death_date)
            VALUES (?, ?, ?, ?, ?)
        """, (first, last, middle, birth, death))

def update_composer(id, first, last, middle, birth, death):
    with get_connection() as conn:
        conn.execute("""
            UPDATE Composer
            SET first_name = ?, last_name = ?, middle_name = ?, birth_date = ?, death_date = ?
            WHERE id = ?
        """, (first, last, middle, birth, death, id))

def delete_composer(id):
    with get_connection() as conn:
        conn.execute("DELETE FROM Composer WHERE id = ?", (id,))
