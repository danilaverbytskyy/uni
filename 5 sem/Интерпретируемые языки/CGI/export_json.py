import sqlite3
import json

def export_to_json():
    db_path = 'music.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM main.Artists")
    planets_rows = cursor.fetchall()

    planets_data = []
    for row in planets_rows:
        planet = {
            "ID": row[0],
            "Name": row[1],
            "Birth_date": row[2],
        }
        planets_data.append(planet)

    with open('artists.json', 'w', encoding='utf-8') as file:
        json.dump(planets_data, file, ensure_ascii=False, indent=4)

    conn.close()
    print("Экспорт завершен! Данные сохранены в artists.json.")


export_to_json()
