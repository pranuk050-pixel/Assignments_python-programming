import numpy as np
import pandas as pd


def clean_data(df):
    """
    Clean basic problems in the dataset.
    """

    data = df.copy()

    # Replace infinity values with NaN
    numeric_columns = data.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:
        data[column] = data[column].replace(
            [np.inf, -np.inf],
            np.nan
        )

    return data


def add_features(df):
    """
    Create new analytical features.
    """

    data = df.copy()

    # ---------------------------------------
    # 1. Income per family member
    # ---------------------------------------

    if {
        "AMT_INCOME_TOTAL",
        "CNT_FAM_MEMBERS"
    }.issubset(data.columns):

        data["INCOME_PER_FAMILY_MEMBER"] = (
            data["AMT_INCOME_TOTAL"]
            /
            data["CNT_FAM_MEMBERS"].replace(
                0,
                np.nan
            )
        )

    # ---------------------------------------
    # 2. Credit-to-Income Ratio
    # ---------------------------------------

    if {
        "AMT_CREDIT",
        "AMT_INCOME_TOTAL"
    }.issubset(data.columns):

        data["CREDIT_TO_INCOME"] = (
            data["AMT_CREDIT"]
            /
            data["AMT_INCOME_TOTAL"].replace(
                0,
                np.nan
            )
        )

    # ---------------------------------------
    # 3. Annuity-to-Income Ratio
    # ---------------------------------------

    if {
        "AMT_ANNUITY",
        "AMT_INCOME_TOTAL"
    }.issubset(data.columns):

        data["ANNUITY_TO_INCOME"] = (
            data["AMT_ANNUITY"]
            /
            data["AMT_INCOME_TOTAL"].replace(
                0,
                np.nan
            )
        )

    # ---------------------------------------
    # 4. Annuity-to-Credit Ratio
    # ---------------------------------------

    if {
        "AMT_ANNUITY",
        "AMT_CREDIT"
    }.issubset(data.columns):

        data["ANNUITY_TO_CREDIT"] = (
            data["AMT_ANNUITY"]
            /
            data["AMT_CREDIT"].replace(
                0,
                np.nan
            )
        )

    # ---------------------------------------
    # 5. Age in years
    # ---------------------------------------

    if "DAYS_BIRTH" in data.columns:

        data["AGE_YEARS"] = (
            -data["DAYS_BIRTH"]
            / 365.25
        ).round(1)

    # ---------------------------------------
    # 6. Employment years
    # ---------------------------------------

    if "DAYS_EMPLOYED" in data.columns:

        employed = data["DAYS_EMPLOYED"].copy()

        # Home Credit has some abnormal
        # positive employment values.
        employed = employed.where(
            employed < 0,
            np.nan
        )

        data["EMPLOYMENT_YEARS"] = (
            -employed
            / 365.25
        ).round(1)

    # ---------------------------------------
    # 7. Phone change years
    # ---------------------------------------

    if "DAYS_LAST_PHONE_CHANGE" in data.columns:

        data["PHONE_CHANGE_YEARS"] = (
            -data["DAYS_LAST_PHONE_CHANGE"]
            / 365.25
        ).round(1)

    return data


def prepare_data(df):
    """
    Complete preprocessing pipeline.
    """

    data = clean_data(df)

    data = add_features(data)

    return data