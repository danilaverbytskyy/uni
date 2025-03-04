import sqlite3

conn = sqlite3.connect('music.db')
cursor = conn.cursor()

cursor.executemany('''
INSERT INTO Artists (name, birth_date) VALUES (?, ?)
''', [
    ('Halsey', '1994-09-29'),
    ('Taylor Swift', '1989-12-13'),
    ('Linkin Park', '1977-02-11')
])

cursor.executemany('''
INSERT INTO Albums (title, artist_id) VALUES (?, ?)
''', [
    ('Manic', 1),
    ('The Great Impersonator', 1),
    ('Midnights', 2),
    ('evermore', 2),
    ('From Zero', 3),
    ('Hybrid Theory', 3),
])

cursor.executemany('''
INSERT INTO Tracks (title, duration, artist_id) VALUES (?, ?, ?)
''', [
    ('Graveyard', 182, 1),
    ('Without Me', 201, 1),
    ('Only Living Girl in LA', 225, 1),
    ('I Never Love You', 230, 1),

    ('Anti-Hero', 200, 2),
    ('Lavender Haze', 202, 2),
    ('willow', 214, 2),
    ('champagne problems', 244, 2),

    ('Cut the Bridge', 220, 3),
    ('Heavy Is The Crown', 210, 3),
    ('In the End', 216, 3),
    ('One Step Closer', 155, 3),
    ('Crawling', 209, 3),
    ('Papercut', 184, 3),
    ('Points of Authority', 200, 3)
])


cursor.executemany('''
INSERT INTO AlbumsTracks (album_id, track_id) VALUES (?, ?)
''', [
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 6),
    (4, 7),
    (4, 8),
    (5, 9),
    (5, 10),
    (6, 11),
    (6, 12),
    (6, 13),
    (6, 14),
    (6, 15)
])

conn.commit()
conn.close()
