import streamlit as st


def sidebar_filters(df):
    """
    Create common sidebar filters.
    """

    filtered_df = df.copy()

    # =======================================
    # CONTRACT TYPE
    # =======================================

    if "NAME_CONTRACT_TYPE" in filtered_df.columns:

        options = sorted(
            filtered_df[
                "NAME_CONTRACT_TYPE"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected = st.sidebar.multiselect(
            "Contract Type",
            options,
            default=options
        )

        if selected:

            filtered_df = filtered_df[
                filtered_df[
                    "NAME_CONTRACT_TYPE"
                ].isin(selected)
            ]

    # =======================================
    # GENDER
    # =======================================

    if "CODE_GENDER" in filtered_df.columns:

        options = sorted(
            filtered_df[
                "CODE_GENDER"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected = st.sidebar.multiselect(
            "Gender",
            options,
            default=options
        )

        if selected:

            filtered_df = filtered_df[
                filtered_df[
                    "CODE_GENDER"
                ].isin(selected)
            ]

    # =======================================
    # EDUCATION
    # =======================================

    if "NAME_EDUCATION_TYPE" in filtered_df.columns:

        options = sorted(
            filtered_df[
                "NAME_EDUCATION_TYPE"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected = st.sidebar.multiselect(
            "Education",
            options,
            default=options
        )

        if selected:

            filtered_df = filtered_df[
                filtered_df[
                    "NAME_EDUCATION_TYPE"
                ].isin(selected)
            ]

    # =======================================
    # TARGET
    # =======================================

    if "TARGET" in filtered_df.columns:

        selected_target = st.sidebar.multiselect(
            "Default Status",
            [0, 1],
            default=[0, 1],

            format_func=lambda value:
                "Default / Repayment Difficulty"
                if value == 1
                else "No Default"
        )

        if selected_target:

            filtered_df = filtered_df[
                filtered_df[
                    "TARGET"
                ].isin(selected_target)
            ]

    return filtered_df
