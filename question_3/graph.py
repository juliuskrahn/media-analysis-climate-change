import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker


class Graph:

    def __init__(self):
        self.fig, self.ax = plt.subplots(1, figsize=(10, 4.2))

    def plot(self, name, articles_about_climate_change_percent_array, values_array):
        self.ax.plot(articles_about_climate_change_percent_array, values_array, "-o", label=name, alpha=0.8)

    def save(self):
        self.ax.set_xlabel("Artikel über Klimawandel pro Monat")
        self.ax.set_ylabel("% Darstellungsart")
        self.ax.set_title("Darstellungsarten")
        self.ax.xaxis.set_major_formatter(plt_ticker.PercentFormatter(100, decimals=1))
        self.ax.yaxis.set_major_formatter(plt_ticker.PercentFormatter(1, decimals=1))
        self.ax.legend()
        self.fig.tight_layout()
        self.fig.savefig(f"result")
