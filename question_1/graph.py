import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker
import utils
import typing


class Graph:

    def __init__(self):
        countries = []
        for publisher in utils.publishers:
            if publisher.country not in countries:
                countries.append(publisher.country)
        _ = plt.subplots(len(countries), figsize=(10, len(countries) * 4.2))
        self.fig: plt.Figure = _[0]
        self.grouped_axs: typing.Dict[str, plt.Axes] = {}
        for i, country in enumerate(countries):
            self.grouped_axs[country] = _[1][i]

    def plot(self, publisher, published_date_array, articles_about_climate_change_percent_array):
        self.grouped_axs[publisher.country].plot(published_date_array,
                                                 articles_about_climate_change_percent_array,
                                                 label=publisher)

    def save(self):
        for country, ax in self.grouped_axs.items():
            ax.set_ylim(ymin=0, ymax=3, auto=False)
            ax.set_xlabel("Jahr")
            ax.set_ylabel("Artikel über Klimawandel pro Monat")
            ax.set_title(country)
            ax.yaxis.set_major_formatter(plt_ticker.PercentFormatter(100, decimals=1))
            ax.legend()
        self.fig.tight_layout()
        self.fig.savefig(f"result")
