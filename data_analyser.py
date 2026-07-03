
import pandas as pd

def analyse_csv(df):
    """
    Analyse a marketing CSV DataFrame and return a dictionary of key metrics.
    
    Parameters:
        df: a pandas DataFrame uploaded by the user
    
    Returns:
        A dictionary summarising the key metrics found in the data
    """
    metrics = {}
    col = [c.lower().strip() for c in df.columns]
    df.columns = col

    metrics["total_rows"] = len(df)
    metrics["columns"] = list(df.columns)

    # Identify numeric columns and summarise them
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    metrics["numeric_summary"] = {}

    for c in numeric_cols:
        metrics["numeric_summary"][c] = {
            "mean": round(df[c].mean(), 2),
            "min": round(df[c].min(), 2),
            "max": round(df[c].max(), 2),
            "total": round(df[c].sum(), 2)
        }

    # Identify categorical columns and find the most common value in each
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    metrics["top_categories"] = {}

    for c in categorical_cols:
        top = df[c].value_counts().head(3).to_dict()
        metrics["top_categories"][c] = top

    return metrics


# ----- TEST BLOCK -----
if __name__ == "__main__":
    # Create a small fake marketing dataset to test with
    test_data = {
        "channel": ["Email", "Social", "Email", "Search", "Social", "Email"],
        "spend": [500, 300, 450, 800, 250, 600],
        "clicks": [120, 80, 95, 200, 60, 140],
        "conversions": [12, 5, 8, 25, 3, 15],
        "revenue": [1200, 400, 750, 2800, 200, 1600]
    }

    df = pd.DataFrame(test_data)
    results = analyse_csv(df)

    print("=== Analysis Results ===")
    print(f"Total rows: {results['total_rows']}")
    print(f"Columns: {results['columns']}")
    print("\nNumeric summary:")
    for col, stats in results["numeric_summary"].items():
        print(f"  {col}: mean={stats['mean']}, total={stats['total']}")
    print("\nTop categories:")
    for col, vals in results["top_categories"].items():
        print(f"  {col}: {vals}")