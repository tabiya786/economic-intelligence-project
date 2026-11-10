
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# ECONOMIC INTELLIGENCE DASHBOARD
# ==========================================

st.set_page_config(
    page_title="Economic Intelligence Dashboard",
    page_icon="🌍",
    layout="wide"
)

# TITLE

st.title("🌍 Economic Intelligence Dashboard")
st.markdown(
    "Explore and compare economic indicators across countries."
)

st.divider()

# LOAD DATA

file_path = "data/raw/economic_data.csv"

if not os.path.exists(file_path):
    st.error("Dataset not found. Check the CSV file location.")
    st.stop()

df = pd.read_csv(file_path)

# CLEAN DATA

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

df = df.dropna(
    subset=["Country", "Country_Code", "Year", "Indicator", "Value"]
)

# SIDEBAR FILTERS

st.sidebar.header("Dashboard Filters")

countries = sorted(df["Country"].unique())

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    countries,
    default=countries
)

indicators = sorted(df["Indicator"].unique())

selected_indicator = st.sidebar.selectbox(
    "Select Economic Indicator",
    indicators
)

available_years = sorted(df["Year"].astype(int).unique())

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=int(min(available_years)),
    max_value=int(max(available_years)),
    value=(
        int(min(available_years)),
        int(max(available_years))
    )
)

# FILTER DATA

filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Indicator"] == selected_indicator) &
    (df["Year"].between(selected_years[0], selected_years[1]))
].copy()

# KEY METRICS

st.subheader("Economic Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Countries Selected", len(selected_countries))

col2.metric("Records Available", len(filtered_df))

if not filtered_df.empty:
    latest_year = int(filtered_df["Year"].max())
    col3.metric("Latest Available Year", latest_year)
else:
    col3.metric("Latest Available Year", "N/A")

st.divider()

# INTERACTIVE LINE CHART

st.subheader(f"{selected_indicator} Comparison")

if not filtered_df.empty:

    chart = px.line(
        filtered_df,
        x="Year",
        y="Value",
        color="Country",
        markers=True,
        title=f"{selected_indicator} Across Selected Countries"
    )

    chart.update_layout(
        xaxis_title="Year",
        yaxis_title="Value (Dataset Units)",
        legend_title="Country",
        hovermode="x unified"
    )

    st.plotly_chart(chart, use_container_width=True)

else:
    st.warning("No data available for the selected filters.")

# DATA TABLE

st.subheader("Economic Data Table")

if not filtered_df.empty:

    display_df = filtered_df[
        ["Country", "Country_Code", "Year", "Indicator", "Value"]
    ].sort_values(["Country", "Year"])

    st.dataframe(
        display_df,
        use_container_width=True
    )

    # DOWNLOAD BUTTON

    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv_data,
        file_name="economic_analysis.csv",
        mime="text/csv"
    )

else:
    st.info("No records to display.")

# FOOTER

st.divider()

st.caption(
    "Economic Intelligence Project | Built using Python, "
    "Pandas, Plotly and Streamlit"
)
