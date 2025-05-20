import streamlit as st
import pandas as pd
from utils import load_and_merge_data, dropna_column, run_anova, run_kruskal, plot_boxplot

st.set_page_config(page_title="GHI Country Comparison", layout="wide")

st.title("🌍 GHI Comparison Dashboard")
st.markdown("This dashboard compares GHI across countries using statistical tests and visualizations.")

file_paths = [
    "data\\benin-malanville_clean.csv",
    "data\\togo-dapaong_qr_clean.csv",
    "data\\sierraleone-bumbuna_clean.csv"    
]

try:
    df = load_and_merge_data(file_paths, ["Benin", "Togo", "Sierra Leone"])
    
    numeric_columns = df.select_dtypes(include=['float', 'int']).columns.tolist()
    categorical_columns = ['Country']

    with st.sidebar:
        st.header("⚙️ Configuration")
        country_col = st.selectbox("Select Country Column", categorical_columns)
        value_col = st.selectbox("Select Value Column (e.g. GHI)", numeric_columns)
        selected_countries = st.multiselect("Select Countries to Compare", df[country_col].unique().tolist())

        run_button = st.button("Run Analysis")

    # Only run analysis if button is clicked
    if run_button:
        if selected_countries and len(selected_countries) >= 2:
            filtered_df = df[df[country_col].isin(selected_countries)]

            # Plot
            st.plotly_chart(
                plot_boxplot(filtered_df, x=country_col, y=value_col, color=country_col),
                use_container_width=True,
                key="boxplot_chart"
            )

            # Statistical tests
            groups = [
                filtered_df[filtered_df[country_col] == c][value_col].dropna()
                for c in selected_countries
            ]

            f_stat, p_anova = run_anova(*groups)
            h_stat, p_kruskal = run_kruskal(*groups)

            st.subheader("📊 Statistical Test Results")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### One-way ANOVA")
                st.write(f"F-statistic: `{f_stat:.4f}`")
                st.write(f"P-value: `{p_anova:.4f}`")
                if p_anova < 0.05:
                    st.success("✅ Statistically significant differences found.")
                else:
                    st.warning("⚠️ No significant difference found.")
            with col2:
                st.markdown("### Kruskal-Wallis Test")
                st.write(f"H-statistic: `{h_stat:.4f}`")
                st.write(f"P-value: `{p_kruskal:.4f}`")
                if p_kruskal < 0.05:
                    st.success("✅ Statistically significant differences found.")
                else:
                    st.warning("⚠️ No significant difference found.")
        else:
            st.warning("Please select at least two countries to compare.")

    else:
        st.info("Please configure your selections and click **Run Analysis** to see results.")

except Exception as e:
    st.error(f"Error: {e}")
