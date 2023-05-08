import sqlite3

connection = sqlite3.connect('database.db')

with open('schema1.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
  "UPDATE teams SET name = 'St. Charles', logo = 'logo/1.png' WHERE team_id = 1;"
)
cur.execute(
  "UPDATE teams SET name = 'Columbia', logo = 'logo/2.png' WHERE team_id = 2;")
cur.execute(
  "UPDATE teams SET name = 'New Orleans', logo = 'logo/3.png' WHERE team_id = 3;"
)
cur.execute(
  "UPDATE teams SET name = 'Baton Rouge', logo = 'logo/4.png' WHERE team_id = 4;"
)
cur.execute(
  "UPDATE teams SET name = 'Carlsbad', logo = 'logo/5.png' WHERE team_id = 5;")
cur.execute(
  "UPDATE teams SET name = 'Quincy', logo = 'logo/6.png' WHERE team_id = 6;")
cur.execute(
  "UPDATE teams SET name = 'Mendon', logo = 'logo/7.png' WHERE team_id = 7;")
cur.execute(
  "UPDATE teams SET name = 'Antioch', logo = 'logo/8.png' WHERE team_id = 8;")

connection.commit()
connection.close()
