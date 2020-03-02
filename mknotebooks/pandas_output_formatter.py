try:
    import pandas as pd
    import tabulate

    def to_md(df, max_colwidth=50):
        """
        Wrapper around `DataFrame.to_markdown`, to display MultiIndex headers on multiple lines,
        and truncate entries longer than max_colwidth characters.
        """
        if df.columns.nlevels == 1:
            col_headers = map(str, df.columns.tolist())
        else:
            # If multi-level column headers, split over multiple lines
            col_headers = ("<br>".join(map(str, col)) for col in df.columns.tolist())
        # Add column level names in left-hand column
        headers = ["<br>".join((name or "" for name in df.columns.names))] + list(
            col_headers
        )
        if any(df.index.names):
            # Add index name (if there is one) on a new header line
            headers[0] += "<br><br>" + ", ".join(map(str, df.index.names))
            headers[1:] = [h + "<br><br>&nbsp;" for h in headers[1:]]

        # Truncate entries wider than max_colwidth
        return (
            df.astype(str)
            .apply(
                lambda x: [
                    (a if len(a) <= max_colwidth else a[: max_colwidth - 3] + "...")
                    for a in x
                ]
            )
            .to_markdown(headers=headers)
        )

    get_ipython().display_formatter.formatters["text/markdown"].for_type(
        pd.DataFrame, to_md
    )
    get_ipython().display_formatter.formatters["text/html"].for_type(
        pd.DataFrame, to_md
    )
except ImportError:
    pass  # No pandas or no tabulate
