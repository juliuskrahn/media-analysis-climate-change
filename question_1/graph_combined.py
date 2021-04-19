import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker


class Graph:

    def __init__(self):
        self.fig, self.ax = plt.subplots(1, figsize=(10, 4.2))

    def plot(self, published_date_array, articles_about_climate_change_percent_array):
        self.ax.plot(published_date_array, articles_about_climate_change_percent_array)

    def save(self):
        self.ax.set_ylim(ymin=0, ymax=3, auto=False)
        self.ax.set_xlabel("Jahr")
        self.ax.set_ylabel("Artikel über Klimawandel pro Monat")
        self.ax.set_title("Untersuchte News-Portale kombiniert")
        self.ax.yaxis.set_major_formatter(plt_ticker.PercentFormatter(100, decimals=1))
        self.fig.tight_layout()
        self.fig.savefig(f"result_combined")
