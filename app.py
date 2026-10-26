import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie & TV Insights", page_icon="🎬", layout="wide")
st.title("🎬 Movie & TV Content Analytics")
st.caption("Prepared for Shalu | Big Data Mini Project")
st.write("Explore a sample entertainment catalogue with interactive filters and visual analytics.")

@st.cache_data
def load_data():
    return pd.read_csv("movie_dataset.csv")

uploaded = st.sidebar.file_uploader("Upload your own CSV (optional)", type=["csv"])
try:
    df = pd.read_csv(uploaded) if uploaded else load_data()
except Exception as e:
    st.error(f"Unable to read the CSV file: {e}")
    st.stop()

required = {"Title", "Type", "Genre", "Country", "Release_Year", "Rating"}
missing = required - set(df.columns)
if missing:
    st.error("Dataset is missing required columns: " + ", ".join(sorted(missing)))
    st.stop()

st.sidebar.header("Explore catalogue")
types = sorted(df["Type"].dropna().astype(str).unique())
genres = sorted(df["Genre"].dropna().astype(str).unique())
countries = sorted(df["Country"].dropna().astype(str).unique())
ratings = sorted(df["Rating"].dropna().astype(str).unique())
sel_types = st.sidebar.multiselect("Content type", types, default=types)
sel_genres = st.sidebar.multiselect("Genre", genres, default=genres)
sel_countries = st.sidebar.multiselect("Country", countries, default=countries)
sel_ratings = st.sidebar.multiselect("Rating", ratings, default=ratings)

filtered = df[
    df["Type"].astype(str).isin(sel_types) &
    df["Genre"].astype(str).isin(sel_genres) &
    df["Country"].astype(str).isin(sel_countries) &
    df["Rating"].astype(str).isin(sel_ratings)
].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Titles in view", f"{len(filtered):,}")
c2.metric("Movies", f"{(filtered['Type'] == 'Movie').sum():,}")
c3.metric("TV Shows", f"{(filtered['Type'] == 'TV Show').sum():,}")
c4.metric("Countries", f"{filtered['Country'].nunique():,}")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Titles by Genre")
    genre_counts = filtered.groupby("Genre").size().reset_index(name="Titles").sort_values("Titles", ascending=False)
    st.plotly_chart(px.bar(genre_counts, x="Genre", y="Titles", color="Genre", title="Catalogue by genre"), use_container_width=True)
with right:
    st.subheader("Movie vs TV Show")
    type_counts = filtered.groupby("Type").size().reset_index(name="Titles")
    st.plotly_chart(px.pie(type_counts, names="Type", values="Titles", hole=.4, title="Content type split"), use_container_width=True)

st.subheader("Release Trends")
year_counts = filtered.groupby("Release_Year").size().reset_index(name="Titles")
st.plotly_chart(px.line(year_counts, x="Release_Year", y="Titles", markers=True, title="Titles by release year"), use_container_width=True)

st.subheader("Country Contribution")
country_counts = filtered.groupby("Country").size().reset_index(name="Titles").sort_values("Titles", ascending=False)
st.plotly_chart(px.bar(country_counts, x="Country", y="Titles", color="Country", title="Titles by country"), use_container_width=True)

st.subheader("Catalogue Data")
st.write(f"Showing {len(filtered):,} records after applying filters.")
st.dataframe(filtered, use_container_width=True, hide_index=True)
st.download_button("⬇️ Download filtered catalogue (CSV)", filtered.to_csv(index=False).encode("utf-8"), "filtered_movie_catalogue.csv", "text/csv")

with st.expander("Project explanation"):
    st.markdown("""
    **Aim:** Explore an entertainment catalogue using data analytics and interactive visualizations.

    **Concepts demonstrated:** CSV data ingestion, filtering, grouping, counting, trend analysis,
    interactive charts, and exporting processed data.

    **Dataset note:** This is a generated sample dataset for a college mini-project demonstration.
    It is not an official catalogue from a streaming service and does not represent real platform statistics.
    """)
