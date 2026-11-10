
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

# ==========================================
# INDICATOR INFORMATION
# ==========================================

INDICATOR_INFO = {
    "GDP_Per_Capita": {
        "title": "GDP Per Capita",
        "description": "Economic output per person.",
        "unit": "Current US$",
        "color_label": "GDP Per Capita (US$)"
    },
    "FDI": {
        "title": "Foreign Direct Investment (FDI)",
        "description": "Net foreign direct investment inflows.",
        "unit": "Current US$",
        "color_label": "FDI (US$)"
    },
    "Population_Growth": {
        "title": "Population Growth",
        "description": "Annual population growth rate.",
        "unit": "%",
        "color_label": "Population Growth (%)"
    },
    "Unemployment": {
        "title": "Unemployment",
        "description": "Unemployment as a percentage of the labour force.",
        "unit": "%",
        "color_label": "Unemployment (%)"
    }
}

# ==========================================
# TITLE
# ==========================================

st.title("🌍 Economic Intelligence Dashboard")

st.markdown(
    """
    Explore, analyse and compare economic indicators across
    10 countries using World Bank data.
    """
)

st.caption(
    "Data period: 2000–2023 | Source: World Bank"
)

st.divider()

# ==========================================
# LOAD DATA
# ==========================================

file_path = "data/raw/economic_data.csv"

if not os.path.exists(file_path):
    st.error("Dataset not found. Check data/raw/economic_data.csv.")
    st.stop()

df = pd.read_csv(file_path)

required_columns = [
    "Country",
    "Country_Code",
    "Year",
    "Indicator",
    "Value"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(f"Missing columns: {missing_columns}")
    st.stop()

# ==========================================
# CLEAN DATA
# ==========================================

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

df = df.dropna(
    subset=required_columns
).copy()

df["Year"] = df["Year"].astype(int)

df = df.sort_values(
    ["Country", "Indicator", "Year"]
)

if df.empty:
    st.error("The dataset contains no valid records.")
    st.stop()

countries = sorted(df["Country"].unique())
indicators = sorted(df["Indicator"].unique())
available_years = sorted(df["Year"].unique())

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.markdown("### Countries")

selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=countries,
    default=countries
)

st.sidebar.markdown("### Economic Indicators")

selected_indicators = st.sidebar.multiselect(
    "Select indicators",
    options=indicators,
    default=indicators
)

st.sidebar.markdown("### Year Range")

selected_years = st.sidebar.slider(
    "Select year range",
    min_value=int(min(available_years)),
    max_value=int(max(available_years)),
    value=(
        int(min(available_years)),
        int(max(available_years))
    )
)

# ==========================================
# FILTER DATA
# ==========================================

filtered_df = df[
    (df["Country"].isin(selected_countries))
    & (df["Indicator"].isin(selected_indicators))
    & (
        df["Year"].between(
            selected_years[0],
            selected_years[1]
        )
    )
].copy()

st.divider()

# ==========================================
# OVERALL ECONOMIC OVERVIEW
# ==========================================

st.header("📊 Economic Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Countries",
    len(selected_countries)
)

col2.metric(
    "Indicators Selected",
    len(selected_indicators)
)

col3.metric(
    "Total Records",
    f"{len(filtered_df):,}"
)

if not filtered_df.empty:
    latest_year = int(filtered_df["Year"].max())
else:
    latest_year = "N/A"

col4.metric(
    "Latest Available Year",
    latest_year
)

st.divider()

# ==========================================
# DATA COVERAGE
# ==========================================

st.subheader("📌 Dataset Coverage")

coverage = (
    filtered_df.groupby("Indicator")
    .agg(
        Countries=("Country", "nunique"),
        Records=("Value", "count"),
        First_Year=("Year", "min"),
        Last_Year=("Year", "max")
    )
    .reset_index()
)

if not coverage.empty:
    st.dataframe(
        coverage,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No data available for the selected filters.")

st.divider()

# ==========================================
# INDIVIDUAL INDICATOR ANALYSIS
# ==========================================

st.header("📈 Economic Indicator Analysis")

st.markdown(
    "Each indicator has its own chart because the units and scales differ."
)

if filtered_df.empty:
    st.warning("No data available. Please change your filters.")

else:

    available_tabs = [
        indicator
        for indicator in indicators
        if indicator in selected_indicators
    ]

    if available_tabs:

        tabs = st.tabs([
            INDICATOR_INFO.get(
                indicator,
                {"title": indicator}
            )["title"]
            for indicator in available_tabs
        ])

        for tab, indicator in zip(tabs, available_tabs):

            with tab:

                indicator_df = filtered_df[
                    filtered_df["Indicator"] == indicator
                ]

                info = INDICATOR_INFO.get(
                    indicator,
                    {
                        "title": indicator,
                        "description": "Economic indicator.",
                        "unit": "Dataset units",
                        "color_label": "Value"
                    }
                )

                st.subheader(info["title"])

                st.write(info["description"])

                st.caption(f"Unit: {info['unit']}")

                chart = px.line(
                    indicator_df,
                    x="Year",
                    y="Value",
                    color="Country",
                    markers=True,
                    title=f"{info['title']} — Country Comparison",
                    labels={
                        "Year": "Year",
                        "Value": info["color_label"],
                        "Country": "Country"
                    }
                )

                chart.update_layout(
                    hovermode="x unified",
                    legend_title="Country"
                )

                st.plotly_chart(
                    chart,
                    use_container_width=True
                )

                st.markdown("#### Country-wise Summary")

                summary = (
                    indicator_df.groupby("Country")["Value"]
                    .agg(
                        Average="mean",
                        Minimum="min",
                        Maximum="max"
                    )
                    .reset_index()
                    .round(2)
                )

                st.dataframe(
                    summary,
                    use_container_width=True,
                    hide_index=True
                )

st.divider()

# ==========================================
# SUMMARY STATISTICS
# ==========================================

st.header("📉 Overall Summary Statistics")

if not filtered_df.empty:

    statistics = (
        filtered_df.groupby("Indicator")["Value"]
        .agg(
            Average="mean",
            Median="median",
            Minimum="min",
            Maximum="max",
            Records="count"
        )
        .reset_index()
        .round(2)
    )

    st.dataframe(
        statistics,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================================
# COMPLETE ECONOMIC DATA TABLE
# ==========================================

st.header("📋 Complete Economic Data")

st.markdown(
    "Explore the individual records containing all five dataset columns."
)

if not filtered_df.empty:

    display_df = filtered_df[
        [
            "Country",
            "Country_Code",
            "Year",
            "Indicator",
            "Value"
        ]
    ].sort_values(
        ["Country", "Indicator", "Year"]
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv_data,
        file_name="economic_analysis_filtered.csv",
        mime="text/csv"
    )

else:
    st.info("No records available.")

# ==========================================
# DOWNLOAD COMPLETE ORIGINAL DATASET
# ==========================================

st.subheader("📥 Download Complete Dataset")

full_csv = df[
    required_columns
].to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download All Economic Data (CSV)",
    data=full_csv,
    file_name="complete_economic_dataset.csv",
    mime="text/csv"
)

# ==========================================
# DATA SOURCE AND FOOTER
# ==========================================

st.divider()

st.subheader("ℹ️ About This Project")

st.markdown(
    """
    **Data Source:** World Bank Open Data

    **Countries:** India, Germany, United States, China,
    Japan, France, United Kingdom, Brazil, South Africa
    and Indonesia.

    **Economic Indicators:**
    - GDP Per Capita
    - Foreign Direct Investment (FDI)
    - Population Growth
    - Unemployment

    **Technologies:** Python, Pandas, Plotly, SQL, SQLite and Streamlit.
    """
)

st.caption(
    "Economic Intelligence Project | Built with Python and Streamlit"
)
