import psycopg2
from contextlib import contextmanager


class Publisher:

    def __init__(self, name, language):
        self.name = name
        self.language = language

    def __str__(self):
        return self.name


publishers = [Publisher(name, language) for name, language in [
    ("ABCNews", "en"),
    ("ABSCBNNews", "en"),
    ("Bild", "de"),
    ("CNN", "en"),
    ("DailyMail", "en"),
    ("Emol", "sp"),
    ("FoxNews", "en"),
    ("Huffpost", "en"),
    ("KenyansCoKe", "en"),
    ("NewsComAu", "en"),
    ("PeoplesDaily", "en"),
    ("RT", "en"),
    ("Spiegel", "de"),
    ("SZ", "de"),
    ("Tagesschau", "de"),
    ("TheGuardian", "en"),
    ("TheTimes", "en"),
    ("TheTimesOfIndia", "en"),
    ("USAToday", "en"),
    ("VG", "nw"),
]]


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
