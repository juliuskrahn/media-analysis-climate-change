import pandas as pd
import matplotlib.pyplot as plt
import utils


for publisher in utils.publishers:
    with utils.db_conn() as conn:
        df_m = pd.read_sql_query(
            f"""
            SELECT to_timestamp(TO_CHAR(published, 'YYYYMM'), 'YYYYMM') AS published_date, COUNT(*) AS n
            FROM article
            WHERE publisher = '{publisher}' AND (SELECT EXTRACT(YEAR FROM published)) >= 2015
            GROUP BY TO_CHAR(published, 'YYYYMM')
            ORDER BY TO_CHAR(published, 'YYYYMM');
            """
            , conn)
        df_d = pd.read_sql_query(
            f"""
            SELECT DATE(published) AS published_date, COUNT(*) AS n
            FROM article
            WHERE publisher = '{publisher}' AND (SELECT EXTRACT(YEAR FROM published)) >= 2015
            GROUP BY DATE(published)
            ORDER BY DATE(published);
            """
            , conn)

    fig, ax = plt.subplots(2, figsize=(42, 4.2))

    ax[0].plot(df_m["published_date"], df_m["n"])
    ax[1].plot(df_d["published_date"], df_d["n"])

    fig.savefig(f"{publisher}_article_freq.png")
