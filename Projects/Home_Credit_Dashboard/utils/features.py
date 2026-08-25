import pandas as pd


def available(df, columns):

    return all(
        column in df.columns
        for column in columns
    )


def default_rate(df):

    if "TARGET" not in df.columns:
        return 0.0

    if len(df) == 0:
        return 0.0

    return df["TARGET"].mean() * 100


def group_default(df, group_column):

    if not available(
        df,
        [group_column, "TARGET"]
    ):
        return pd.DataFrame()

    result = (
        df.groupby(
            group_column,
            dropna=False
        )["TARGET"]
        .agg(["count", "mean"])
        .reset_index()
    )

    result["default_rate"] = (
        result["mean"] * 100
    )

    result = result.drop(
        columns="mean"
    )

    return result