import psycopg2
from contextlib import contextmanager


class Publisher:

    def __init__(self, name, language, country):
        self.name = name
        self.language = language
        self.country = country

    def __repr__(self):
        return self.name


publishers = [Publisher(name, language, country) for name, language, country in [
    ("ABCNews", "en", "Australien"),
    ("ABSCBNNews", "en", "Philippinen"),
    ("Bild", "de", "Deutschland"),
    ("CNN", "en", "USA"),
    ("DailyMail", "en", "UK"),
    # ("Emol", "sp", "cl"),  # cancelled
    ("FoxNews", "en", "USA"),
    ("Huffpost", "en", "USA"),
    ("KenyansCoKe", "en", "Kenya"),
    ("NewsComAu", "en", "Australien"),
    ("PeoplesDaily", "en", "China"),
    ("RT", "en", "Russland"),
    ("Spiegel", "de", "Deutschland"),
    ("SZ", "de", "Deutschland"),
    ("Tagesschau", "de", "Deutschland"),
    ("TheGuardian", "en", "UK"),
    ("TheTimes", "en", "UK"),
    ("TheTimesOfIndia", "en", "Indien"),
    ("USAToday", "en", "USA"),
    # ("VG", "no", "no"),  # cancelled
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
