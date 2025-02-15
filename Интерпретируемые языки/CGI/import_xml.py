import sqlite3
import xml.etree.ElementTree as ET

def import_from_xml():
    db_path = 'music.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Парсинг XML-файла
    tree = ET.parse('artists.xml')
    root = tree.getroot()

    for artist in root.findall('Artist'):
        # Извлечение данных из элементов
        artist_id = int(artist.find('ID').text)
        name = artist.find('Name').text
        birth_date = artist.find('birth_date').text

        # Проверка на существование записи в базе данных
        cursor.execute("SELECT COUNT(*) FROM main.Artists WHERE artist_id = ?", (artist_id,))
        count = cursor.fetchone()[0]

        if count == 0:  # Если записи нет, добавляем новую
            cursor.execute(
                "INSERT INTO main.Artists (artist_id, name, birth_date) VALUES (?, ?, ?)",
                (artist_id, name, birth_date)
            )
        else:
            print(f"Запись {artist_id} уже существует.")

    conn.commit()
    conn.close()
    print("Импорт завершён!")

import_from_xml()
