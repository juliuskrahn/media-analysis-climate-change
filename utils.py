import psycopg2
from contextlib import contextmanager


publishers = [
    "ABCNews",
    "ABSCBNNews",
    "Bild",
    "CNN",
    "DailyMail",
    "Emol",
    "FoxNews",
    "Huffpost",
    "KenyansCoKe",
    "NewsComAu",
    "PeoplesDaily",
    "RT",
    "Spiegel",
    "SZ",
    "Tagesschau",
    "TheGuardian",
    "TheTimes",
    "TheTimesOfIndia",
    "USAToday",
    "VG",
]


@contextmanager
def db_conn():
    conn = psycopg2.connect(dbname="media_analysis", user="julius", password="", host="localhost", port=5432)
    yield conn
    conn.close()

        
@contextmanager
def db_conn_cur():
    conn = psycopg2.connect(dbname="media_analysis", user="julius", password="", host="localhost", port=5432)
    with conn.cursor() as cur:
        yield cur
    conn.commit()
    conn.close()
