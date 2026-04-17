import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="France Top 50 Analysis", layout="wide")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Atlantic_France.csv")

    # Data preprocessing
    df['date'] = pd.to_datetime(df['date'])
    df['duration_min'] = df['duration_ms'] / 60000
    df['album_type'] = df['album_type'].str.lower()

    # Duration buckets
    def duration_bucket(x):
        if x < 2.5:
            return "Short"
        elif x <= 4:
            return "Medium"
        else:
            return "Long"

    df['duration_type'] = df['duration_min'].apply(duration_bucket)

    # Rank tiers
    def rank_tier(pos):
        if pos <= 10:
            return "Top 10"
        elif pos <= 25:
            return "Top 25"
        else:
            return "Top 50"

    df['rank_tier'] = df['position'].apply(rank_tier)

    return df


df = load_data()

# -------------------------------
# Title
# -------------------------------
st.title("🇫🇷 France Top 50 Playlist Analysis Dashboard")

# -------------------------------
# Sidebar Filters (User Capabilities)
# -------------------------------
st.sidebar.header("🔍 Filters")

# Date range selector
min_date = df['date'].min()
max_date = df['date'].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Rank tier filter
rank_filter = st.sidebar.selectbox(
    "Rank Tier",
    ["All", "Top 10", "Top 25", "Top 50"]
)

# Explicit toggle
explicit_filter = st.sidebar.selectbox(
    "Explicit Content",
    ["All", "Explicit", "Clean"]
)

# Album type filter
album_filter = st.sidebar.selectbox(
    "Album Type",
    ["All", "single", "album"]
)

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = df.copy()

# Date filter
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['date'] >= pd.to_datetime(date_range[0])) &
        (filtered_df['date'] <= pd.to_datetime(date_range[1]))
    ]

# Rank filter
if rank_filter != "All":
    filtered_df = filtered_df[filtered_df['rank_tier'] == rank_filter]

# Explicit filter
if explicit_filter == "Explicit":
    filtered_df = filtered_df[filtered_df['is_explicit'] == 1]
elif explicit_filter == "Clean":
    filtered_df = filtered_df[filtered_df['is_explicit'] == 0]

# Album filter
if album_filter != "All":
    filtered_df = filtered_df[filtered_df['album_type'] == album_filter]

# -------------------------------
# CORE MODULES
# -------------------------------

# 1️⃣ Explicit vs Clean Analysis
st.subheader("1️⃣ Explicit vs Clean Content Analysis")
st.bar_chart(filtered_df['is_explicit'].value_counts())

# 2️⃣ Album Format Distribution
st.subheader("2️⃣ Album Format Distribution")
st.bar_chart(filtered_df['album_type'].value_counts())

# 3️⃣ Song Duration Histogram
st.subheader("3️⃣ Song Duration Histogram")
fig, ax = plt.subplots()
ax.hist(filtered_df['duration_min'])
ax.set_xlabel("Duration (minutes)")
ax.set_ylabel("Count")
st.pyplot(fig)

# 4️⃣ Rank-Tier Content Attribute Comparison
st.subheader("4️⃣ Rank-Tier Content Attribute Comparison")
comparison = filtered_df.groupby('rank_tier').agg({
    'is_explicit': 'mean',
    'duration_min': 'mean'
})
st.dataframe(comparison)

# 5️⃣ Content Compliance Summary Panel
st.subheader("5️⃣ Content Compliance Summary Panel")

col1, col2, col3 = st.columns(3)

explicit_share = filtered_df['is_explicit'].mean() * 100
avg_duration = filtered_df['duration_min'].mean()
single_ratio = (filtered_df['album_type'] == 'single').mean() * 100

col1.metric("Explicit Content %", f"{explicit_share:.2f}%")
col2.metric("Avg Duration (min)", f"{avg_duration:.2f}")
col3.metric("Single Track %", f"{single_ratio:.2f}%")

# -------------------------------
# Insights Section
# -------------------------------
st.subheader("📌 Key Insights")

if explicit_share < 40:
    st.write("✔ French audience prefers clean content")

if 2.5 <= avg_duration <= 4:
    st.write("✔ Medium duration songs perform best")

if single_ratio > 60:
    st.write("✔ Singles dominate the playlist")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built for France Top 50 Playlist Analysis | Data Analytics Project")