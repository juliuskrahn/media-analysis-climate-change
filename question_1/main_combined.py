import pandas as pd
import utils
from is_about_climate_change_sql_statement import is_about_climate_change_sql_statement
from graph_combined import Graph


def main():

    dfs = []

    for publisher in utils.publishers:

        with utils.db_conn() as conn:
            dfs.append(pd.read_sql_query(
                f"""
                SELECT articles_total.published_date AS published_date,
                    (SELECT CAST(articles_about_climate_change_absolute.n AS real) / articles_total.n) * 100
                    AS articles_about_climate_change_percent
                FROM (
                    SELECT TO_CHAR(published, 'YYYY') AS published_date, COUNT(*) as n
                    FROM article
                    WHERE publisher = '{publisher}' AND ((SELECT EXTRACT(YEAR FROM published)) BETWEEN 2015 AND 2020)
                    AND {is_about_climate_change_sql_statement[publisher.language]}
                    GROUP BY TO_CHAR(published, 'YYYY')
                ) AS articles_about_climate_change_absolute
                JOIN (
                    SELECT TO_CHAR(published, 'YYYY') AS published_date, COUNT(*) AS n
                    FROM article
                    WHERE publisher = '{publisher}' AND ((SELECT EXTRACT(YEAR FROM published)) BETWEEN 2015 AND 2020)
                    GROUP BY TO_CHAR(published, 'YYYY')
                ) AS articles_total
                ON articles_total.published_date = articles_about_climate_change_absolute.published_date
                ORDER BY articles_total.published_date;
                """
                , conn)
            )

    graph = Graph()

    df_combined = pd.concat(dfs)
    df_combined = df_combined.groupby(df_combined["published_date"]).mean()
    graph.plot(df_combined.index, df_combined["articles_about_climate_change_percent"])

    graph.save()


if __name__ == '__main__':
    main()
