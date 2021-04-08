import pandas as pd
import utils
from is_about_climate_change_sql_statement import is_about_climate_change_sql_statement
from graph import Graph


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
