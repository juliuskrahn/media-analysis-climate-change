import matplotlib.pyplot as plt
import matplotlib.ticker as plt_ticker


class Graph:

    def __init__(self):
        self.fig, [self.type_ax, self.repr_ax] = plt.subplots(2, figsize=(10, 4.2))

    def plot_type(self, name, published_date_array, values_array):
        self.type_ax.plot(published_date_array, values_array, label=name)

    def plot_repr(self, name, published_date_array, values_array):
        self.repr_ax.plot(published_date_array, values_array, label=name)

    def save(self):
        self.type_ax.set_xlabel("Jahr")
        self.repr_ax.set_xlabel("Jahr")
        self.type_ax.set_ylabel("% Artikeltyp")
        self.repr_ax.set_ylabel("% Darstellungsart")
        self.type_ax.set_title("Artikeltypen")
        self.repr_ax.set_title("Darstellungsarten")
        self.type_ax.yaxis.set_major_formatter(plt_ticker.PercentFormatter(1, decimals=1))
        self.repr_ax.yaxis.set_major_formatter(plt_ticker.PercentFormatter(1, decimals=1))
        self.type_ax.legend()
        self.repr_ax.legend()
        self.fig.tight_layout()
        self.fig.savefig(f"result")
