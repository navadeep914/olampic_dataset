import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Olympic Data Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM STYLE
# =========================
st.markdown("""
<style>
.main-header {
    font-size: 2.8rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA LOADER (ROBUST)
# =========================
@st.cache_data
def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    # Normalize column names
    df.columns = [c.strip().title() for c in df.columns]

    # Required columns
    required_columns = {
        "Athlete", "Age", "Country", "Year",
        "Sport", "Gold", "Silver", "Bronze"
    }

    if not required_columns.issubset(df.columns):
        st.error("❌ Dataset does not contain required columns.")
        st.write("Required columns:")
        st.write(sorted(required_columns))
        st.write("Found columns:")
        st.write(list(df.columns))
        st.stop()

    # Convert medal columns to numeric
    for col in ["Gold", "Silver", "Bronze"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # Convert Age & Year
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)

    # Total medals
    df["Total_Medals"] = df["Gold"] + df["Silver"] + df["Bronze"]

    return df

# =========================
# MAIN APP
# =========================
def main():
    st.markdown('<div class="main-header">🏅 Olympic Data Analysis Dashboard</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Olympic Dataset (CSV format)",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info("👆 Please upload an Olympic CSV dataset to begin")
        return

    df = load_data(uploaded_file)

    # =========================
    # SIDEBAR FILTERS
    # =========================
    st.sidebar.header("🔍 Filters")

    years = sorted(df["Year"].dropna().unique())
    selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years)

    countries = sorted(df["Country"].dropna().unique())
    selected_countries = st.sidebar.multiselect("Select Country(s)", countries)

    sports = sorted(df["Sport"].dropna().unique())
    selected_sports = st.sidebar.multiselect("Select Sport(s)", sports)

    filtered_df = df[df["Year"].isin(selected_years)]

    if selected_countries:
        filtered_df = filtered_df[filtered_df["Country"].isin(selected_countries)]

    if selected_sports:
        filtered_df = filtered_df[filtered_df["Sport"].isin(selected_sports)]

    # =========================
    # METRICS
    # =========================
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Athletes", filtered_df["Athlete"].nunique())
    c2.metric("Countries", filtered_df["Country"].nunique())
    c3.metric("Gold Medals", int(filtered_df["Gold"].sum()))
    c4.metric("Total Medals", int(filtered_df["Total_Medals"].sum()))

    # =========================
    # TABS
    # =========================
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Top Athletes",
        "🌍 Country Analysis",
        "📊 Year Trends",
        "🏃 Sport Analysis"
    ])

    # -------- TAB 1 --------
    with tab1:
        top_athletes = (
            filtered_df.groupby("Athlete")["Total_Medals"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_athletes,
            x="Athlete",
            y="Total_Medals",
            color="Total_Medals",
            title="Top 10 Athletes by Total Medals"
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(top_athletes, use_container_width=True)

    # -------- TAB 2 --------
    with tab2:
        country_medals = (
            filtered_df.groupby("Country")["Total_Medals"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            country_medals,
            x="Country",
            y="Total_Medals",
            color="Total_Medals",
            title="Top Countries by Total Medals"
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # -------- TAB 3 --------
    with tab3:
        year_trend = (
            filtered_df.groupby("Year")["Total_Medals"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            year_trend,
            x="Year",
            y="Total_Medals",
            markers=True,
            title="Total Medals Over the Years"
        )
        st.plotly_chart(fig, use_container_width=True)

    # -------- TAB 4 --------
    with tab4:
        sport_medals = (
            filtered_df.groupby("Sport")["Total_Medals"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            sport_medals,
            x="Sport",
            y="Total_Medals",
            color="Total_Medals",
            title="Top Sports by Medals"
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # RAW DATA + DOWNLOAD
    # =========================
    st.header("📋 Raw Data")

    if st.checkbox("Show filtered data"):
        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "Download Filtered Data",
            csv,
            "filtered_olympic_data.csv",
            "text/csv"
        )

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    main()
