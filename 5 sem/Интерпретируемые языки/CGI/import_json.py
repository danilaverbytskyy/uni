import sqlite3
import json


def import_from_json():
    db_path = 'music.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open('artists.json', 'r', encoding='utf-8') as file:
        artists_data = json.load(file)

    # Вставляем только новые данные (проверка на существующий id)
    for artist in artists_data:
        cursor.execute("SELECT COUNT(*) FROM main.Artists WHERE artist_id = ?", (artist["ID"],))
        count = cursor.fetchone()[0]

        if count == 0:  # Только если такого ID нет
            cursor.execute("INSERT INTO main.Artists (artist_id, name, birth_date) VALUES (?, ?, ?)",
                           (artist["ID"], artist["Name"], artist["Birth_date"]))

    conn.commit()

    conn.close()
    print("Данные импортированы из artists.json в базу данных.")


import_from_json()
