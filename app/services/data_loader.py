import pandas as pd
from io import BytesIO
from typing import Union

def load_dataframe(source: Union[str, BytesIO], filename: str = None) -> pd.DataFrame:
    # If a path is provided
    if isinstance(source, str):
        if source.endswith(".csv"):
            return pd.read_csv(source)
        if source.endswith(".xlsx") or source.endswith(".xls"):
            return pd.read_excel(source)
        raise ValueError("Unsupported file format.")

    # If a BytesIO object is provided (in-memory)
    if isinstance(source, BytesIO):
        if filename is None:
            raise ValueError("Filename must be provided when using BytesIO.")

        if filename.endswith(".csv"):
            return pd.read_csv(source)
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            return pd.read_excel(source)
        raise ValueError("Unsupported file format.")

    raise TypeError("Source must be a file path or BytesIO.")
