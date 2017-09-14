"""functions that deal with the database logic."""
import yaml
import sqlite3
import base64 as b64
from random import randint

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

def connect(database):
    """Return sqlite3 Connection."""
    return sqlite3.connect(database)


def shorten():
    """Generate a random Integer converted to base64."""
    r = str(randint(0, 1e100))  # 0 to googol so 1x10^100
    short = b64.b64encode(r)[:8]
    while short in getShorts(connect(cfg['general']['sqlite_location'])):
        r = str(randint(0, 1e100))
        short = b64.b64encode(r)[:8]
    return short


def addEntry(longURl, conn):
    """Add entry to database, checking if url was shortend before."""
    c = conn.cursor()
    (shortFromDB, check) = longURlInDB(longURl, conn)
    if check:
        return shortFromDB[3:-3]
    else:
        short = shorten()
        c.execute('CREATE TABLE if not exists urls (url text, short text)')
        c.execute('INSERT INTO urls VALUES (?,?)', (longURl, short))
        conn.commit()
        conn.close()
        return short


def longURlInDB(longUrl, conn):
    """Check if the url to be shortend was already shortened before."""
    c = conn.cursor()
    found = False
    c.execute('CREATE TABLE if not exists urls (url text, short text)')
    c.execute('select short from urls where url=' + '"' + longUrl + '"')
    short = c.fetchone()
    if short:
        found = True
    return (str(short), found)


def resolve(shortURL, conn):
    """ Resolve short Url IDs."""
    c = conn.cursor()
    c.execute('select url from urls where short=' + '"' + shortURL + '"')
    longUrl = str(c.fetchone())
    conn.close()
    return longUrl[3:-3]


def getShorts(conn):
    """Get Short urls which are in DB."""
    c = conn.cursor()
    c.execute('SELECT short from urls')
    shorts = c.fetchall()
    return shorts
