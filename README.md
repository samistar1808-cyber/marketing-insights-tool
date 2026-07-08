# Marketing Insights Tool 📈
### AI-powered marketing analysis — upload your data, get strategic recommendations instantly

[Live Demo](https://samistar-marketing-insights-tool.streamlit.app) · 

---

## What it does

Upload any marketing or campaign CSV and get back:
- An automated data summary with key metrics and charts
- AI-generated plain-English strategic recommendations
- A downloadable insights report

No technical knowledge required — just upload your data and click.

---

## The problem it solves

Marketing teams sit on enormous amounts of campaign data but often 
lack the time or technical skills to turn raw numbers into actionable 
strategy. This tool bridges that gap — automating the analysis layer 
and using AI to surface the insights that matter.

---

## How it works

1. **Upload** any marketing CSV — campaign performance, email metrics, 
   sales data, e-commerce reports
2. **Analyse** — Pandas automatically detects your columns and 
   calculates key metrics regardless of data format
3. **Generate** — metrics are structured into a prompt and sent to 
   Google Gemini, which returns strategic recommendations written 
   for a marketing director
4. **Download** — export your insights report as a .txt file

---

## What makes it different

The tool is deliberately data-agnostic. It doesn't look for specific 
column names — it detects whatever numeric and categorical columns 
exist and adapts automatically. This means it works for any marketing 
team regardless of their platform or data format.

---

## Tech stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Automatic data detection and metric calculation |
| Google Gemini API | AI-generated strategic insights |
| Plotly | Interactive charts |
| Streamlit | Web app and deployment |

---

## Setup

```bash
# Clone the repo
git clone https://github.com/samistar1808-cyber/marketing-insights-tool.git
cd marketing-insights-tool

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Google AI Studio API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

## Technical challenge worth noting

During development, Google deprecated their official `google.generativeai` 
Python library mid-build, breaking API key authentication. Rather than 
waiting for a fix, I bypassed the library entirely and called the 
Gemini REST API directly using Python's `requests` library. This 
resolved the issue immediately and gave me a clearer understanding 
of how APIs work under the hood.

---

## What I'd build next

- **Multi-file comparison** — upload two campaigns and compare performance
- **Trend detection** — identify whether metrics are improving or declining over time
- **Custom prompt templates** — let users choose the type of analysis they want
- **Slack/email integration** — automatically send insights reports to a team
- **Competitor benchmarking** — compare your metrics against industry averages

---

## About

Built by [Sami Winter](https://github.com/samistar1808-cyber) — 
second-year AI + Commerce student at Macquarie University, building 
tools that bridge data, AI and business strategy.