import sqlite3

connection = sqlite3.connect("hotel.db")
cursor = connection.cursor()

criar_tabela = "CREATE TABLE IF NOT EXISTS hoteis \
 (hotel_id text PRIMARY KEY, name text, daily real, rating real, cidade text)"

cursor.execute(criar_tabela)
connection.commit()

cursor.close()
connection.close()
