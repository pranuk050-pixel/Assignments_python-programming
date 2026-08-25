def overview_kpis(df):
    """
    Calculate main dashboard KPIs.
    """

    # Number of applications
    applications = len(df)

    # Default rate
    if "TARGET" in df.columns:
        default_rate = (
            df["TARGET"].mean()
            * 100
        )
    else:
        default_rate = 0

    # Average income
    if "AMT_INCOME_TOTAL" in df.columns:
        avg_income = (
            df["AMT_INCOME_TOTAL"]
            .mean()
        )
    else:
        avg_income = 0

    # Average credit
    if "AMT_CREDIT" in df.columns:
        avg_credit = (
            df["AMT_CREDIT"]
            .mean()
        )
    else:
        avg_credit = 0

    return {
        "applications": applications,
        "default_rate": default_rate,
        "avg_income": avg_income,
        "avg_credit": avg_credit
    }