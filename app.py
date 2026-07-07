import streamlit as st
import pandas as pd
import plotly.express as px
from data_analyser import analyse_csv
from insights_generator import generate_insights

# Page config
st.set_page_config(
    page_title="Marketing Insights Tool",
    page_icon="📈",
    layout="wide"
)

# ---- Header ----
st.title("Marketing Insights Tool 📈")
st.markdown("*Upload your marketing data and get AI-powered strategic recommendations*")
st.divider()

# ---- Sidebar ----
with st.sidebar:
    st.header("Settings")

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"],
        help="Upload any marketing or campaign CSV"
    )

    context = st.text_area(
        "Add context (optional)",
        placeholder="e.g. This is a 3-month email campaign for our winter sale targeting existing customers",
        height=100
    )

    analyse_button = st.button("Generate Insights ✨", type="primary")

    st.divider()
    st.caption("Built by Sami Winter · Marketing Insights Tool")

# ---- Main content ----
if uploaded_file is not None:

    # Load and preview the CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Your data")
    st.dataframe(df.head(10), use_container_width=True)
    st.caption(f"{len(df)} rows · {len(df.columns)} columns")

    if analyse_button:

        # Step 1: Analyse
        with st.spinner("Analysing your data..."):
            metrics = analyse_csv(df)

        # Step 2: Generate insights
        with st.spinner("Generating AI insights..."):
            insights = generate_insights(metrics, context=context)

        st.divider()

        # ---- Metrics row ----
        st.subheader("Data summary")
        numeric = metrics["numeric_summary"]

        if numeric:
            cols = st.columns(min(len(numeric), 4))
            for i, (col_name, stats) in enumerate(numeric.items()):
                with cols[i % 4]:
                    st.metric(
                        label=col_name.replace("_", " ").title(),
                        value=f"{stats['total']:,.0f}",
                        help=f"Average: {stats['mean']} · Min: {stats['min']} · Max: {stats['max']}"
                    )

        st.divider()

        # ---- Charts ----
        if len(numeric) >= 2:
            chart_col1, chart_col2 = st.columns(2)

            col_names = list(numeric.keys())

            with chart_col1:
                fig = px.bar(
                    df,
                    x=df.columns[0],
                    y=col_names[0],
                    title=f"{col_names[0].replace('_', ' ').title()} breakdown",
                    color_discrete_sequence=["#6B2737"]
                )
                st.plotly_chart(fig, use_container_width=True)

            with chart_col2:
                fig2 = px.bar(
                    df,
                    x=df.columns[0],
                    y=col_names[1],
                    title=f"{col_names[1].replace('_', ' ').title()} breakdown",
                    color_discrete_sequence=["#D17A4A"]
                )
                st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # ---- AI Insights ----
        st.subheader("AI-generated insights")
        st.markdown(insights)

        st.divider()

        # ---- Download ----
        with st.expander("Download summary"):
            summary_text = f"MARKETING INSIGHTS REPORT\n\n{insights}"
            st.download_button(
                label="Download insights as .txt",
                data=summary_text,
                file_name="marketing_insights.txt",
                mime="text/plain"
            )

else:
    st.info("👈 Upload a CSV file in the sidebar to get started.")

    st.markdown("""
    ### How it works
    1. Upload any marketing or campaign CSV
    2. Add optional context about your data
    3. Click **Generate Insights** to run the AI
    4. Get a data summary, charts, and strategic recommendations

    ### What kind of CSV can I upload?
    Any marketing data works — campaign performance, email metrics,
    social media analytics, sales data, or e-commerce reports.
    The tool automatically detects your columns and adapts.

    ### Example columns it works well with
    | Column | Example values |
    |--------|---------------|
    | channel | Email, Social, Search |
    | spend | 500, 300, 800 |
    | clicks | 120, 80, 200 |
    | conversions | 12, 5, 25 |
    | revenue | 1200, 400, 2800 |
    """)