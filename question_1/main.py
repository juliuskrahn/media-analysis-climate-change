import pandas as pd
import matplotlib.pyplot as plt
import utils


is_about_climate_change_sql_statement = {
    "en":
        """
        ((title ~* 'climat' AND title ~* '(chang|catastroph|disaster|transform|adjust|trend|warm|heat|cool|variab|chill)')
        OR (title ~* 'greenhouse' AND title ~* 'effect')
        OR (title ~* '(global|earth|world|international|hemisphere)' AND title ~* '(warm|heat|cool|chill)')
        OR (title ~* '(global|earth|world|international|hemisphere)' AND title ~* 'temperature' AND title ~*
        '(increas|rising|rise|decreas)'))
        """,
    "de": 
        """
        ((title ~* 'klima' AND title ~* '(wandel|änder|wechsel|krise|erwärm|erhitz|problem|zustand|katastroph|trend|
        politik|desaster|schwank|projekt|schutz|schädlich|schadet|schaden|auswirk|ziel|plan|gipfel|treffen|vertrag|
        ausschuss|beschluss|strategie|aktivis|demo|einsatz|einsetz|streik)')
        OR (title ~* '(global|erde|welt|international)' AND title ~* '(erwärm|erhitz|temperatur)')
        OR (title ~* 'treibhaus' AND title ~* '(gas|effekt)'))
        """,
    "nw": "",  # TODO
    "sp": "",  # TODO
}

fig, ax = plt.subplots(1, figsize=(12, 4))
ax.set_xlabel("Jahr")
ax.set_ylabel("Anteil [Artikel über Klimawandel] pro Monat")
ax.set_title("Zeitungen im Vergleich")

for publisher in utils.publishers:

    with utils.db_conn() as conn:
        df = pd.read_sql_query(
            f"""
            SELECT articles_total.published_date AS published_date,
                (SELECT CAST(articles_about_climate_change_absolute.n AS real) / articles_total.n) * 100
                AS articles_about_climate_change_percent
            FROM (
                SELECT to_timestamp(TO_CHAR(published, 'YYYYMM'), 'YYYYMM') AS published_date, COUNT(*) as n
                FROM article
                WHERE publisher = '{publisher}' AND (SELECT EXTRACT(YEAR FROM published)) >= 2015
                AND {is_about_climate_change_sql_statement[publisher.language]}
                GROUP BY TO_CHAR(published, 'YYYYMM')
            ) AS articles_about_climate_change_absolute
            JOIN (
                SELECT to_timestamp(TO_CHAR(published, 'YYYYMM'), 'YYYYMM') AS published_date, COUNT(*) AS n
                FROM article
                WHERE publisher = '{publisher}' AND (SELECT EXTRACT(YEAR FROM published)) >= 2015
                GROUP BY TO_CHAR(published, 'YYYYMM')
            ) AS articles_total
            ON articles_total.published_date = articles_about_climate_change_absolute.published_date
            ORDER BY TO_CHAR(articles_total.published_date, 'YYYYMM');
            """
            , conn)

    ax.plot(df["published_date"], df["articles_about_climate_change_percent"], label=publisher)

ax.legend()
fig.savefig(f"main_results")
