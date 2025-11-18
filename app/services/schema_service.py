import pandas as pd

def extract_schema(df):
    try:
        describe_data = df.describe(include="all", datetime_is_numeric=True).fillna("").to_dict()
    except:
        describe_data = df.describe(include="all").fillna("").to_dict()

    column_summaries = {}

    for col in df.columns:
        series = df[col]

        if series.dtype == "object":
            column_summaries[col] = series.value_counts().head(5).to_dict()
            continue

        numeric_series = pd.to_numeric(series, errors="coerce")

        if numeric_series.notnull().any():
            # numeric column
            column_summaries[col] = {
                "min": float(numeric_series.min()),
                "max": float(numeric_series.max()),
                "mean": float(numeric_series.mean()),
            }
            continue

        if pd.api.types.is_datetime64_any_dtype(series):
            column_summaries[col] = {
                "min": str(series.min()) if series.notnull().any() else None,
                "max": str(series.max()) if series.notnull().any() else None,
                "mean": None,  
            }
            continue

        column_summaries[col] = {
            "min": None,
            "max": None,
            "mean": None,
        }

    return {
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "shape": df.shape,
        "describe": describe_data,
        "column_summaries": column_summaries,
    }
