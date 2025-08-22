import pandas as pd


def find_cell(df: pd.DataFrame, target: str) -> tuple[int, int] | None:
    """Return (row_idx, col_idx) of a case-insensitive exact match anywhere in the sheet."""
    t = str(target).strip().lower()
    for ridx, row in df.iterrows():
        for cidx, val in enumerate(row):
            if pd.isna(val):
                continue
            if str(val).strip().lower() == t:
                return ridx, cidx
    return None
