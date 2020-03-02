try:
    import pandas as pd
    import tabulate

    get_ipython().display_formatter.formatters["text/markdown"].for_type(
        pd.DataFrame, lambda x: x.to_markdown()
    )
    get_ipython().display_formatter.formatters["text/html"].for_type(
        pd.DataFrame, lambda x: x.to_markdown()
    )
except ImportError:
    pass  # No pandas or no tabulate
