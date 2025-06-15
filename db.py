import sqlite3

DB_NAME = "db/composers.sqlite"

def get_connection():
    return sqlite3.connect(DB_NAME)

def fetch_all_composers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, birth_year, death_year FROM Composer")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_composer(full_name, birth_year, death_year):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Composer (full_name, birth_year, death_year) VALUES (?, ?, ?)",
        (full_name, birth_year, death_year)
    )
    conn.commit()
    conn.close()

def update_composer(composer_id, full_name, birth_year, death_year):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Composer SET full_name=?, birth_year=?, death_year=? WHERE id=?",
        (full_name, birth_year, death_year, composer_id)
    )
    conn.commit()
    conn.close()

def delete_composer(composer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Composer WHERE id=?", (composer_id,))
    conn.commit()
    conn.close()

def fetch_all_countries():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Country")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_country(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Country (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def update_country(country_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Country SET name=? WHERE id=?", (name, country_id))
    conn.commit()
    conn.close()

def delete_country(country_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Country WHERE id=?", (country_id,))
    conn.commit()
    conn.close()

def fetch_all_composers_short():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name FROM Composer")
    result = cursor.fetchall()
    conn.close()
    return result

def fetch_all_countries_short():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Country")
    result = cursor.fetchall()
    conn.close()
    return result

def fetch_countries_by_composer(composer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT country_id FROM ComposerCountry WHERE composer_id=?
    """, (composer_id,))
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result

def set_composer_countries(composer_id, country_ids):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ComposerCountry WHERE composer_id=?", (composer_id,))
    for cid in country_ids:
        cursor.execute("INSERT INTO ComposerCountry (composer_id, country_id) VALUES (?, ?)",
                       (composer_id, cid))
    conn.commit()
    conn.close()

def fetch_all_works():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT Work.id, Work.title, Work.year_written,
           Composer.id, Composer.full_name,
           Genre.id, Genre.name
    FROM Work
    JOIN Composer ON Work.composer_id = Composer.id
    JOIN Genre ON Work.genre_id = Genre.id
    ORDER BY Work.id;
    """
    return cursor.execute(query).fetchall()

def insert_work(title, year, composer_id, genre_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Work (title, year_written, composer_id, genre_id) VALUES (?, ?, ?, ?)",
        (title, year, composer_id, genre_id)
    )
    conn.commit()

def update_work(work_id, title, year, composer_id, genre_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Work SET title = ?, year_written = ?, composer_id = ?, genre_id = ? WHERE id = ?",
        (title, year, composer_id, genre_id, work_id)
    )
    conn.commit()

def delete_work(work_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Work WHERE id = ?", (work_id,))
    conn.commit()

def fetch_all_genres_short():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM Genre ORDER BY id")
    return cursor.fetchall()
