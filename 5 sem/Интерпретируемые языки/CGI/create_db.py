import sqlite3

conn = sqlite3.connect('music.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE Artists(
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30),
    birth_date DATE
);
''')

cursor.execute("""
CREATE TABLE Tracks(
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(20),
    duration INTEGER,
    artist_id INTEGER,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);
""")

cursor.execute("""
CREATE TABLE Albums(
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(20),
    artist_id INTEGER,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);
""")

cursor.execute("""
CREATE TABLE AlbumsTracks(
    album_id INTEGER,
    track_id INTEGER,
    PRIMARY KEY (album_id, track_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id),
    FOREIGN KEY (track_id) REFERENCES Tracks(track_id)
);
""")

conn.commit()
conn.close()
