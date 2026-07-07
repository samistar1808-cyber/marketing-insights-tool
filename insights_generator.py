import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_insights(metrics: dict, context: str = "") -> str:
    """
    Send analysed metrics to Gemini and get back strategic recommendations.
    
    Parameters:
        metrics: dictionary of metrics from data_analyser.py
        context: optional extra context the user provides about their data
    
    Returns:
        A string containing Gemini's plain-English insights and recommendations
    """
    
    # Format the metrics into readable text for the prompt
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

    # Build the prompt
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
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text

# ----- TEST BLOCK -----
if __name__ == "__main__":
    # Use the same fake data structure as data_analyser.py
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