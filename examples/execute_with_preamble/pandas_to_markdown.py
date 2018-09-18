import pandas as pd
import tabulate as tabulate


def to_md(self):
    return tabulate.tabulate(self.head(), self.columns, tablefmt="pipe")


get_ipython().display_formatter.formatters["text/html"].for_type(pd.DataFrame, to_md)
