import sqlite3

conn = sqlite3.connect('music.db')
cursor = conn.cursor()

# 1. Имя и дата рождения исполнителей
cursor.execute('''
SELECT name, birth_date
from Artists
GROUP BY name;
''')
print(cursor.fetchall())

# 2 Все песни, длительность которых дольше 3 минут
cursor.execute('''
SELECT title, duration
from Tracks
WHERE duration>180
GROUP BY title
order by duration;
''')
print(cursor.fetchall())

# 3. Альбомы и количество песен в них, отсортированные по убыванию
cursor.execute('''
SELECT title, COUNT(*) as Количество
FROM AlbumsTracks
join main.Albums A on A.album_id = AlbumsTracks.album_id
GROUP BY A.album_id
order by Количество desc;
''')
print(cursor.fetchall())

conn.close()
