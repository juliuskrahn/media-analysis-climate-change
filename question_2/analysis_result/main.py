import numpy as np
import pandas as pd
from graph import Graph


def main():
    graph = Graph()

    df = pd.read_excel("../analysed_data_combined.ods", engine="odf")
    df["published"] = pd.to_datetime(df["published"], format="%Y-%M-%d")
    df_result = df.groupby(pd.Grouper(key="published", freq='YS')).agg(np.mean)
    graph.plot_repr("verleugnet", df_result.index, df_result["content:verleugnet"])
    graph.plot_repr("zugespitzt", df_result.index, df_result["content:zugespitzt"])
    graph.plot_repr("runtergespielt", df_result.index, df_result["content:runtergespielt"])
    graph.plot_type("Bericht", df_result.index, df_result["content:bericht"])
    graph.plot_type("Reportage", df_result.index, df_result["content:reportage"])
    graph.plot_type("Kolumne", df_result.index, df_result["content:kolumne"])

    graph.save()


if __name__ == '__main__':
    main()
