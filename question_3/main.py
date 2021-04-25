import typing
import numpy as np
import pandas as pd
import utils
from question_1.is_about_climate_change_sql_statement import is_about_climate_change_sql_statement
from graph import Graph


def get_publisher_specific_is_about_climate_change_dfs() -> typing.Dict[typing.Any, pd.DataFrame]:
    dfs = {}

    for publisher in utils.publishers:
        with utils.db_conn() as conn:
            dfs[publisher] = pd.read_sql_query(
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
                , conn, index_col="published")
            dfs[publisher].index = pd.to_datetime(dfs[publisher].index, format="%Y")
    return dfs


def main():
    publisher_specific_is_about_climate_change_dfs = get_publisher_specific_is_about_climate_change_dfs()

    content_analysis_df = pd.read_excel("../question_2/analysed_data_combined.ods", engine="odf")
    content_analysis_df["published"] = pd.to_datetime(content_analysis_df["published"], format="%Y-%M-%d")

    publisher_specific_content_and_is_about_cc_comparison_dfs = []
    for publisher, is_about_climate_change_df in publisher_specific_is_about_climate_change_dfs.items():
        content_df = content_analysis_df[content_analysis_df["publisher"] == publisher.name]
        content_df = content_df.groupby(pd.Grouper(key="published", freq='YS')).agg(np.mean)
        publisher_specific_content_and_is_about_cc_comparison_dfs.append(
            pd.concat((is_about_climate_change_df, content_df), axis=1)
        )

    result_df = pd.concat(publisher_specific_content_and_is_about_cc_comparison_dfs).sort_values(
        by="articles_about_climate_change_percent"
    )

    graph = Graph()

    graph.plot("verleugnet", result_df["articles_about_climate_change_percent"], result_df["content:verleugnet"])
    graph.plot("zugespitzt", result_df["articles_about_climate_change_percent"], result_df["content:zugespitzt"])
    graph.plot("runtergespielt", result_df["articles_about_climate_change_percent"],
               result_df["content:runtergespielt"])

    graph.save()


if __name__ == '__main__':
    main()
