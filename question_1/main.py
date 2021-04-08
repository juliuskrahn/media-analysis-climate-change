import pandas as pd
import utils
from graph import Graph


is_about_climate_change_sql_statement = {
    "en":
        """
        ((title ~* 'climat' AND title ~* '(chang|catastroph|disaster|transform|adjust|trend|warm|heat|cool|variab|chill|
        politic|project|target|goal|conference|protect|effect|harm|damage|impact|contract|law|mission|demonstrat|protest
        |activis|plan|resolution|decision|strategy)')
        OR (title ~* '(global|earth|world|international|hemisphere)' 
            AND (
                title ~* '(warm|heat|cool|chill)'
                OR (title ~* 'temperature' AND title ~* '(increas|rising|rise|decreas)')
            )
        )
        OR (title ~* 'greenhouse' AND title ~* '(gas|effect|emission)'))
        """,
    "de":
        """
        ((title ~* 'klima' AND title ~* '(wandel|änder|wechsel|krise|erwärm|warm|kält|kalt|erhitz|problem|zustand|
        politik|desaster|schwank|projekt|schutz|schädlich|schadet|schaden|auswirk|ziel|plan|gipfel|treffen|vertrag|
        ausschuss|beschluss|strategie|aktivis|demo|einsatz|einsetz|streik|katastroph|trend|gesetz)')
        OR (title ~* '(global|erde|welt|international)'
            AND (
                title ~* '(wärm|erhitz|hitze|heiz|warm|temperatur)'
                OR (title ~* 'temperatur' AND title ~* '(steig|stieg|senk|sink|sank)')
            )
        )
        OR (title ~* 'treibhaus' AND title ~* '(gas|effekt|emission)'))
        """,
}


def main():
    graph = Graph()

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

        graph.plot(publisher, df["published_date"], df["articles_about_climate_change_percent"])

    graph.save()


if __name__ == '__main__':
    main()
