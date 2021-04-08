"""Load article sample (1%) into spreadsheet for manual content analysis"""
import pandas as pd
import utils
from question_1.is_about_climate_change_sql_statement import is_about_climate_change_sql_statement
import os.path


def main():

    if not os.path.isdir("output"):
        os.mkdir("output")

    for publisher in utils.publishers:
        with utils.db_conn() as conn:
            df = pd.read_sql_query(
                f"""
                SELECT url, publisher, TO_CHAR(published, 'YYYY-MM-DD') AS published
                FROM article
                TABLESAMPLE BERNOULLI(2)
                WHERE publisher = '{publisher}' AND (SELECT EXTRACT(YEAR FROM published)) >= 2015
                AND {is_about_climate_change_sql_statement[publisher.language]};
                """
                , conn)
            df.to_excel(f"output/{publisher}.ods", engine="odf")


if __name__ == "__main__":
    main()
