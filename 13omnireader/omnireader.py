import os
import pandas as pd

default_dir = os.path.dirname(os.path.abspath(__file__)) # this one sets default path and is fucking important 


def resolve_path(filename: str) -> str:
    """Resolve a file name against the script's directory (not the CWD)."""
    if os.path.isabs(filename):
        return filename
    return os.path.join(default_dir, filename)


def load_dataframe(filename: str) -> pd.DataFrame:
    """Load a CSV, Excel, or TXT file into a pandas DataFrame based on its extension."""
    filename = resolve_path(filename)
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    ext = os.path.splitext(filename)[1].lower()

    if ext == ".csv":
        return pd.read_csv(filename)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(filename)
    if ext == ".txt":
        # Try common delimiters, fall back to whitespace
        for sep in (",", ";", "\t"):
            try:
                df = pd.read_csv(filename, sep=sep)
                if df.shape[1] > 1:
                    return df
            except pd.errors.ParserError:
                continue
        return pd.read_csv(filename, sep=r"\s+", engine="python")
    raise ValueError(f"Unsupported file format: {ext}")


def main():
    filename = input("Enter the file name: ").strip()
    try:
        df = load_dataframe(filename)
        print(f"\nLoaded {len(df)} rows and {df.shape[1]} columns.\n")
        print(df.head())
        return df
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    main()
