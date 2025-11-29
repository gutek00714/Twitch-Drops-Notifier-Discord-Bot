import sqlite3

#connecto to datebase
con = sqlite3.connect("games.db")

cur = con.cursor()

#create database
cur.execute("CREATE TABLE IF NOT EXISTS games (user_id, game_name )")
cur.execute("CREATE TABLE IF NOT EXISTS rewards (game_name, rewards_id )")

con.commit()
con.close()