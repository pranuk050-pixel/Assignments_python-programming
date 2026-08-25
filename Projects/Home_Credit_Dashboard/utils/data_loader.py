from pathlib import Path
import pandas as pd
import streamlit as st


DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"
DATA_PATHS = (
    DATA_DIRECTORY / "application_train.csv",
    DATA_DIRECTORY / "application_train (1).csv",
)


@st.cache_resource
def load_data():
    """
    Load Home Credit application training data.
    """

    data_path = next((path for path in DATA_PATHS if path.exists()), None)
    if data_path is None:
        st.error(
            "Dataset not found. Expected application_train.csv "
            "or application_train (1).csv in the data folder."
        )
        return pd.DataFrame()

    df = pd.read_csv(data_path)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
    )

    return df
