import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_insights(metrics: dict, context: str = "") -> str:
    """
    Send analysed metrics to Gemini and get back strategic recommendations.
    Uses direct HTTP request instead of Google's library.
    """
    metrics_text = f"""
Total rows analysed: {metrics['total_rows']}
Columns in dataset: {', '.join(metrics['columns'])}

Numeric metrics:
"""
    for col, stats in metrics["numeric_summary"].items():
        metrics_text += f"  - {col}: average={stats['mean']}, min={stats['min']}, max={stats['max']}, total={stats['total']}\n"

    if metrics["top_categories"]:
        metrics_text += "\nTop categories:\n"
        for col, vals in metrics["top_categories"].items():
            top = list(vals.keys())[0] if vals else "N/A"
            metrics_text += f"  - {col}: most common = '{top}'\n"

    prompt = f"""You are a senior marketing analyst reviewing campaign performance data.

Here is a summary of the dataset:
{metrics_text}

{f"Additional context from the user: {context}" if context else ""}

Please provide:
1. A 2-3 sentence plain-English summary of what this data shows
2. 3 specific strategic recommendations based on the patterns you can see
3. One key risk or watch-out the marketing team should be aware of

Be specific, practical and direct. Write as if presenting to a marketing director.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error {response.status_code}: {response.json()}"


# ----- TEST BLOCK -----
if __name__ == "__main__":
    test_metrics = {
        "total_rows": 6,
        "columns": ["channel", "spend", "clicks", "conversions", "revenue"],
        "numeric_summary": {
            "spend": {"mean": 483.33, "min": 250, "max": 800, "total": 2900},
            "clicks": {"mean": 115.83, "min": 60, "max": 200, "total": 695},
            "conversions": {"mean": 11.33, "min": 3, "max": 25, "total": 68},
            "revenue": {"mean": 1158.33, "min": 200, "max": 2800, "total": 6950}
        },
        "top_categories": {
            "channel": {"Email": 3, "Social": 2, "Search": 1}
        }
    }

    print("Sending data to Gemini...\n")
    insights = generate_insights(test_metrics, context="This is a 6-month campaign across three channels")
    print("=== Gemini's Insights ===")
    print(insights)