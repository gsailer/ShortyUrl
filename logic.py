# logic.py
import sqlite3
import base64 as b64
from random import randint

DATABASE = "urls.db"
TABLE = "urls"

def connect(database):
	return sqlite3.connect(database)		

def shorten():
	r = str(randint(0,1e100)) # 0 to googol so 1x10^100
	short = b64.b64encode(r)[:8]
	while short in getShorts(connect(DATABASE), TABLE):
		r = str(randint(0,1e100))
		short = b64.b64encode(r)[:8]
	return short

def addEntry(longURl, conn, table):
	c = conn.cursor()
	short = shorten()
	c.execute('CREATE TABLE if not exists urls (url text, short text)')
	c.execute('INSERT INTO urls VALUES (?,?)', (longURl, short))
	conn.commit()
	conn.close()
	return short

def resolve(shortURL, conn):
	c = conn.cursor()
	c.execute('select url from urls where short='+'"'+shortURL+'"')
	longUrl = str(c.fetchone())
	conn.close()
	return longUrl[3:-3]

def getShorts(conn, table):
	c = conn.cursor()
	c.execute('SELECT short from urls')
	shorts = c.fetchall()
	return shorts
