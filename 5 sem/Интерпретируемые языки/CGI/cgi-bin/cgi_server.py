#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Content-Type: text/html; charset=UTF-8")
print()

html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Music</title>
</head>
<body>
    <h1>Добавление нового артиста</h1>
    <form method="post" action="/cgi-bin/cgi_server.py">
        <label for="artist_name">Имя артиста:</label>
        <input type="text" id="artist_name" name="artist_name" required><br><br>

        <label for="birth_date">Дата рождения:</label>
        <input type="date" id="birth_date" name="birth_date" required><br><br>

        <input type="submit" value="Добавить">
    </form>

    <h2>Список всех артистов</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Имя</th>
            <th>Дата рождения</th>
        </tr>
        {artists_rows}
    </table>

    <h2>Добавить альбом</h2>
    <form method="post" action="/cgi-bin/cgi_server.py">
        <label for="album_title">Название альбома:</label>
        <input type="text" id="album_title" name="album_title" required><br><br>

        <label for="artist_id">ID артиста:</label>
        <input type="number" id="artist_id" name="artist_id" required><br><br>

        <input type="submit" value="Добавить альбом">
    </form>

    <h2>Список альбомов</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Артист</th>
        </tr>
        {albums_rows}
    </table>

    <h2>Добавить трек</h2>
    <form method="post" action="/cgi-bin/cgi_server.py">
        <label for="track_title">Название трека:</label>
        <input type="text" id="track_title" name="track_title" required><br><br>

        <label for="duration">Длительность (в секундах):</label>
        <input type="number" id="duration" name="duration" required><br><br>

        <label for="artist_id">ID артиста:</label>
        <input type="number" id="track_artist_id" name="track_artist_id" required><br><br>

        <input type="submit" value="Добавить трек">
    </form>

    <h2>Список треков</h2>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Длительность (сек)</th>
            <th>Артист</th>
        </tr>
        {tracks_rows}
    </table>
</body>
</html>
"""

# Подключение к базе данных
db_path = './music.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получение данных из формы
form = cgi.FieldStorage()

# Добавление нового артиста
artist_name = form.getvalue("artist_name")
birth_date = form.getvalue("birth_date")

if artist_name and birth_date:
    cursor.execute("INSERT INTO Artists (name, birth_date) VALUES (?, ?)", (artist_name, birth_date))
    conn.commit()

# Добавление альбома
album_title = form.getvalue("album_title")
artist_id = form.getvalue("artist_id")

if album_title and artist_id:
    cursor.execute("INSERT INTO Albums (title, artist_id) VALUES (?, ?)", (album_title, int(artist_id)))
    conn.commit()

# Добавление трека
track_title = form.getvalue("track_title")
duration = form.getvalue("duration")
track_artist_id = form.getvalue("track_artist_id")

if track_title and duration and track_artist_id:
    cursor.execute("INSERT INTO Tracks (title, duration, artist_id) VALUES (?, ?, ?)", (track_title, int(duration), int(track_artist_id)))
    conn.commit()

# Получение всех данных из таблицы Artists
cursor.execute("SELECT * FROM main.Artists")
artists_rows = cursor.fetchall()

# Получение всех данных из таблицы Albums с присоединением к Artists
cursor.execute("SELECT Albums.album_id, Albums.title, Artists.name FROM Albums INNER JOIN Artists ON Albums.artist_id = Artists.artist_id")
albums_rows = cursor.fetchall()

# Получение всех данных из таблицы Tracks с присоединением к Artists
cursor.execute("SELECT Tracks.track_id, Tracks.title, Tracks.duration, Artists.name FROM Tracks INNER JOIN Artists ON Tracks.artist_id = Artists.artist_id")
tracks_rows = cursor.fetchall()

# Генерация HTML-таблиц
artists_html = "".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>" for row in artists_rows)
albums_html = "".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>" for row in albums_rows)
tracks_html = "".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>" for row in tracks_rows)

# Закрытие соединения с базой данных
conn.close()

# Вывод HTML-страницы
print(html_template.format(artists_rows=artists_html, albums_rows=albums_html, tracks_rows=tracks_html))
