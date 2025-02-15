import sqlite3
import xml.etree.ElementTree as ET

def export_to_xml():
    db_path = 'music.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM main.Artists")
    planets_rows = cursor.fetchall()

    root = ET.Element('Artists')

    for row in planets_rows:
        artist = ET.SubElement(root, 'Artist')

        ET.SubElement(artist, 'ID').text = str(row[0])
        ET.SubElement(artist, 'Name').text = row[1]
        ET.SubElement(artist, 'birth_date').text = row[2]

    # Создание XML-документа и запись в файл
    tree = ET.ElementTree(root)
    with open('artists.xml', 'wb') as file:
        tree.write(file, encoding='utf-8', xml_declaration=True)

    conn.close()
    print("Экспорт завершен! Данные сохранены в artists.xml.")

export_to_xml()
