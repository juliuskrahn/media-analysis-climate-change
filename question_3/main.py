import numpy as np
import pandas as pd
import utils
from question_1.is_about_climate_change_sql_statement import is_about_climate_change_sql_statement
from graph import Graph


def get_is_about_climate_change_df():
    dfs = []

    for publisher in utils.publishers:
        with utils.db_conn() as conn:
            dfs.append(pd.read_sql_query(
                f"""
                SELECT articles_total.published_date AS published,
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

    df_combined = pd.concat(dfs)
    df_combined = df_combined.groupby(df_combined["published"]).mean()
    df_combined.index = pd.to_datetime(df_combined.index, format="%Y")
    return df_combined


def main():
    is_about_climate_change_df = get_is_about_climate_change_df()

    article_content_df = pd.read_excel("../question_2/analysed_data_combined.ods", engine="odf")
    article_content_df["published"] = pd.to_datetime(article_content_df["published"], format="%Y-%M-%d")
    article_content_df = article_content_df.groupby(pd.Grouper(key="published", freq='YS')).agg(np.mean)

    df_combined = pd.concat((is_about_climate_change_df, article_content_df), axis=1)
    df_combined = df_combined.sort_values(by="articles_about_climate_change_percent")

    graph = Graph()

    graph.plot("verleugnet", df_combined["articles_about_climate_change_percent"], df_combined["content:verleugnet"])
    graph.plot("zugespitzt", df_combined["articles_about_climate_change_percent"], df_combined["content:zugespitzt"])
    graph.plot("runtergespielt", df_combined["articles_about_climate_change_percent"], df_combined["content:runtergespielt"])

    graph.save()


if __name__ == '__main__':
    main()
