"""
================================================================================
 NETFLIX CONTENT ANALYTICS DASHBOARD  —  v2 (Enhanced / Interactive Edition)
================================================================================
A modern, dark, glassmorphism-styled Streamlit dashboard for exploring the
cleaned Netflix Movies & TV Shows dataset.

Author : Hassam Ali
Stack  : Streamlit + Plotly + Pandas
Notes  : Dataset is assumed ALREADY cleaned (nulls handled, dates parsed,
         duplicates removed) via the companion EDA notebook. Only
         visualization-oriented parsing (splitting multi-value columns,
         extracting numeric duration) happens here — no cleaning logic.
================================================================================
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 2. THEME — FONTS, GLASSMORPHISM CSS, GRADIENTS, ANIMATIONS
# ==============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* ---------- App background: deep gradient + subtle vignette ---------- */
.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(229,9,20,0.10) 0%, rgba(15,17,23,0) 45%),
        radial-gradient(circle at 85% 100%, rgba(139,0,20,0.10) 0%, rgba(15,17,23,0) 45%),
        linear-gradient(180deg, #0b0c11 0%, #0f1117 100%);
    color: #e8e8ea;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14151d 0%, #0d0e13 100%);
    border-right: 1px solid rgba(229,9,20,0.15);
}
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stSelectbox label {
    color: #c9c9cc !important;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

/* ---------- Headings ---------- */
h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif !important;
    color: #f7f7f8 !important;
}

/* ---------- Hero banner ---------- */
.hero {
    background: linear-gradient(120deg, rgba(229,9,20,0.16), rgba(60,10,18,0.05) 60%);
    border: 1px solid rgba(229,9,20,0.25);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45);
}
.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 34px;
    font-weight: 800;
    background: linear-gradient(90deg, #ffffff, #ff4d55 70%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero-subtitle {
    color: #b9b9bd;
    font-size: 15px;
    margin-top: 6px;
}

/* ---------- KPI cards (glassmorphism + hover lift) ---------- */
.kpi-card {
    position: relative;
    background: rgba(255, 255, 255, 0.035);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.kpi-card:hover {
    transform: translateY(-5px);
    border-color: rgba(229,9,20,0.55);
    box-shadow: 0 12px 28px rgba(229,9,20,0.18);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: -40%; left: -40%;
    width: 60%; height: 180%;
    background: linear-gradient(120deg, rgba(229,9,20,0.18), transparent 60%);
    transform: rotate(20deg);
    pointer-events: none;
}
.kpi-icon {
    font-size: 24px;
    margin-bottom: 6px;
    opacity: 0.9;
}
.kpi-value {
    font-family: 'Poppins', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
}
.kpi-label {
    font-size: 12.5px;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    color: #9a9aa0;
    margin-top: 4px;
}
.kpi-accent { color: #ff3b47; }

/* ---------- Section titles ---------- */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f5f5f5;
    margin: 26px 0 10px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::before {
    content: "";
    display: inline-block;
    width: 5px;
    height: 20px;
    background: linear-gradient(180deg, #ff3b47, #7a0d13);
    border-radius: 3px;
}
.section-caption {
    color: #93939a;
    font-size: 13px;
    margin-bottom: 14px;
    margin-top: -6px;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;                                   /* wider gap between pills */
    background: rgba(255,255,255,0.03);
    padding: 14px;                                /* more inner padding around the pills */
    border-radius: 20px;                          /* rounder outer container */
    border: 1px solid rgba(255,255,255,0.07);
    margin: 4px 0 30px 0;                         /* top + bottom spacing around the whole bar */
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 16px !important;               /* rounder pill corners */
    padding: 16px 30px !important;                 /* larger click target */
    margin: 0 !important;
    color: #b4b4ba;
    font-weight: 600;
    font-size: 16px;                               /* larger tab label text */
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    overflow: hidden;                              /* clips the highlight bar to the rounded corners */
    transition: all 0.25s ease;                    /* smooth hover/select animation */
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(229,9,20,0.12);
    border-color: rgba(229,9,20,0.35);
    color: #ffffff;
    transform: translateY(-2px);                   /* subtle lift on hover */
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #e50914, #b0060d) !important;
    color: white !important;
    border-radius: 16px !important;
    border-color: transparent !important;
    box-shadow: 0 6px 16px rgba(229,9,20,0.35);    /* glow to make the active tab pop */
}
.stTabs [aria-selected="true"]:hover {
    transform: none;                               /* keep the active tab steady */
}
/* BaseWeb draws a thin underline under the active tab by default — it sits
   flush at the bottom edge and makes the corners look square. Since we're
   already highlighting the active tab with a full background color, we hide
   that underline entirely. */
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}
/* Removes the bottom border-line BaseWeb adds under the whole tab list */
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ---------- Chart card wrapper ---------- */
.chart-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 10px 14px 2px 14px;
    margin-bottom: 14px;
}

/* ---------- Dataframe ---------- */
.stDataFrame {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    overflow: hidden;
}

/* ---------- Misc ---------- */
hr { border-color: rgba(255,255,255,0.08); }
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #3a1216; border-radius: 8px; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------- Shared Plotly styling ----------
PLOTLY_TEMPLATE = "plotly_dark"
PAPER_BG = "rgba(0,0,0,0)"
PLOT_BG = "rgba(0,0,0,0)"
RED_SCALE = ["#3a0a0f", "#7a0d13", "#b0060d", "#e50914", "#ff5a63"]

CHART_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToAdd": ["toggleSpikelines"],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "netflix_chart",
        "height": 800,
        "width": 1200,
        "scale": 2,
    },
}


def style_fig(fig: go.Figure, title: str, height: int = 400) -> go.Figure:
    """Apply consistent dark glass styling + subtle entrance animation to a figure."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        title=dict(text=title, font=dict(
            size=16, family="Poppins, sans-serif", color="#f5f5f5")),
        font=dict(color="#d3d3d8", family="Inter, sans-serif"),
        margin=dict(l=10, r=10, t=55, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=height,
        hoverlabel=dict(bgcolor="#1b1d27", font_size=13,
                        font_family="Inter, sans-serif"),
        transition=dict(duration=400, easing="cubic-in-out"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)",
                     zerolinecolor="rgba(255,255,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)",
                     zerolinecolor="rgba(255,255,255,0.08)")
    return fig


def chart_card(fig: go.Figure):
    """Render a Plotly figure inside a styled 'glass card' container."""
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# 3. DATA LOADING
# ==============================================================================
DEFAULT_PATH = "netflix_titles_cleaned.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date_added" in df.columns:
        df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    return df


def get_dataframe() -> pd.DataFrame:
    """Load the default cleaned CSV, falling back to a sidebar uploader if missing."""
    try:
        return load_data(DEFAULT_PATH)
    except FileNotFoundError:
        st.sidebar.warning(
            f"Default file not found at `{DEFAULT_PATH}`. Upload your cleaned CSV below."
        )
        uploaded = st.sidebar.file_uploader(
            "Upload netflix_titles_cleaned.csv", type=["csv"])
        if uploaded is not None:
            df = pd.read_csv(uploaded)
            if "date_added" in df.columns:
                df["date_added"] = pd.to_datetime(
                    df["date_added"], errors="coerce")
            return df
        st.stop()


df_raw = get_dataframe()

# ==============================================================================
# 4. VISUALIZATION-ONLY HELPERS (not data cleaning)
# ==============================================================================


def explode_column(data: pd.DataFrame, column: str) -> pd.Series:
    """Split a comma-separated column (country, listed_in, director, cast) into a flat Series."""
    return data[column].dropna().astype(str).str.split(",").explode().str.strip()


@st.cache_data
def get_country_options(data: pd.DataFrame) -> list:
    countries = explode_column(data, "country")
    return sorted(c for c in countries.unique() if c and c.lower() != "unknown")


@st.cache_data
def get_movie_durations(data: pd.DataFrame) -> pd.DataFrame:
    movies = data[data["type"] == "Movie"].copy()
    movies["duration_minutes"] = movies["duration"].astype(
        str).str.extract(r"(\d+)").astype(float)
    return movies.dropna(subset=["duration_minutes"])


country_options_full = get_country_options(df_raw)
rating_options_full = sorted(df_raw["rating"].dropna().unique().tolist())
year_min, year_max = int(df_raw["release_year"].min()), int(
    df_raw["release_year"].max())

# ==============================================================================
# 5. SIDEBAR FILTERS
# ==============================================================================
st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown("Refine every chart, KPI, and table on this page.")
st.sidebar.markdown("---")

type_filter = st.sidebar.multiselect(
    "🎞️ Content Type",
    options=sorted(df_raw["type"].dropna().unique().tolist()),
    default=sorted(df_raw["type"].dropna().unique().tolist()),
)

country_filter = st.sidebar.multiselect(
    "🌍 Country",
    options=country_options_full,
    default=[],
    help="Leave empty to include all countries.",
)

rating_filter = st.sidebar.multiselect(
    "🔖 Rating",
    options=rating_options_full,
    default=[],
    help="Leave empty to include all ratings.",
)

year_filter = st.sidebar.slider(
    "📅 Release Year",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + Plotly · Netflix Titles Dataset")

# ==============================================================================
# 6. APPLY FILTERS
# ==============================================================================
mask = pd.Series(True, index=df_raw.index)

if type_filter:
    mask &= df_raw["type"].isin(type_filter)

if country_filter:
    mask &= df_raw["country"].astype(str).apply(
        lambda cell: any(c.strip() in country_filter for c in cell.split(","))
    )

if rating_filter:
    mask &= df_raw["rating"].isin(rating_filter)

mask &= df_raw["release_year"].between(year_filter[0], year_filter[1])

df = df_raw[mask].copy()

# ==============================================================================
# 7. HERO HEADER
# ==============================================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🎬 Netflix Content Analytics Dashboard</div>
        <div class="hero-subtitle">
            Explore Netflix's global catalog — content mix, geographic reach, ratings,
            release trends, genres, and durations — all in real time.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 8. KPI CARDS
# ==============================================================================
total_titles = len(df)
total_movies = int((df["type"] == "Movie").sum())
total_tv_shows = int((df["type"] == "TV Show").sum())
total_countries = len(get_country_options(df)) if total_titles else 0

kpi_cols = st.columns(4)
kpi_data = [
    ("🎬", f"{total_titles:,}", "Total Titles"),
    ("🎥", f"{total_movies:,}", "Total Movies"),
    ("📺", f"{total_tv_shows:,}", "Total TV Shows"),
    ("🌍", f"{total_countries:,}", "Countries Represented"),
]
for col, (icon, value, label) in zip(kpi_cols, kpi_data):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if total_titles == 0:
    st.warning("No titles match the current filters. Try widening your selection.")
    st.stop()

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 9. TABBED LAYOUT
# ==============================================================================
tab_overview, tab_geo, tab_trends, tab_data = st.tabs(
    ["📊 Overview", "🌍 Geography & Genres", "📈 Trends & Duration", "📋 Explore Data"]
)

# ------------------------------------------------------------------------------
# TAB 1 — OVERVIEW
# ------------------------------------------------------------------------------
with tab_overview:
    st.markdown('<div class="section-title">Content Mix Snapshot</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">A quick read on the split between Movies and TV Shows, '
        'and how ratings are distributed across the catalog.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1.3])

    with c1:
        type_counts = df["type"].value_counts().reset_index()
        type_counts.columns = ["type", "count"]
        fig_type = px.pie(
            type_counts, names="type", values="count", hole=0.6,
            color="type",
            color_discrete_map={"Movie": "#e50914", "TV Show": "#3f434f"},
        )
        fig_type.update_traces(
            textinfo="percent+label",
            pull=[0.04] * len(type_counts),
            marker=dict(line=dict(color="#0f1117", width=2)),
            hovertemplate="<b>%{label}</b><br>Titles: %{value}<br>Share: %{percent}<extra></extra>",
        )
        fig_type = style_fig(fig_type, "Content Type Distribution")
        chart_card(fig_type)

    with c2:
        rating_counts = df["rating"].value_counts().reset_index()
        rating_counts.columns = ["rating", "count"]
        rating_counts = rating_counts.sort_values("count", ascending=True)
        fig_rating = px.bar(
            rating_counts, x="count", y="rating", orientation="h",
            color="count", color_continuous_scale=RED_SCALE,
            labels={"count": "Number of Titles", "rating": "Rating"},
            text="count",
        )
        fig_rating.update_traces(
            hovertemplate="<b>%{y}</b><br>Titles: %{x}<extra></extra>",
            textposition="outside",
        )
        fig_rating.update_layout(coloraxis_showscale=False)
        fig_rating = style_fig(fig_rating, "Rating Distribution")
        chart_card(fig_rating)

    st.markdown('<div class="section-title">Type × Rating Heatmap</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Where each content rating skews — toward Movies or TV Shows.</div>',
        unsafe_allow_html=True,
    )
    heat_data = pd.crosstab(df["rating"], df["type"])
    fig_heat = px.imshow(
        heat_data,
        color_continuous_scale=RED_SCALE,
        labels=dict(x="Content Type", y="Rating", color="Titles"),
        aspect="auto",
        text_auto=True,
    )
    fig_heat.update_traces(
        hovertemplate="Rating: %{y}<br>Type: %{x}<br>Titles: %{z}<extra></extra>")
    fig_heat = style_fig(
        fig_heat, "Rating vs. Content Type Heatmap", height=420)
    chart_card(fig_heat)

# ------------------------------------------------------------------------------
# TAB 2 — GEOGRAPHY & GENRES
# ------------------------------------------------------------------------------
with tab_geo:
    st.markdown('<div class="section-title">Where Netflix Content Comes From</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Country contributions are counted per co-production credit '
        '(a title with multiple countries counts once for each).</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.3, 1])

    with c1:
        country_series = explode_column(df, "country")
        country_series = country_series[country_series.str.lower(
        ) != "unknown"]
        top_countries = country_series.value_counts().head(10).sort_values()
        fig_country = px.bar(
            x=top_countries.values, y=top_countries.index, orientation="h",
            color=top_countries.values, color_continuous_scale=RED_SCALE,
            labels={"x": "Number of Titles", "y": "Country"}, text=top_countries.values,
        )
        fig_country.update_traces(
            hovertemplate="<b>%{y}</b><br>Titles: %{x}<extra></extra>", textposition="outside",
        )
        fig_country.update_layout(coloraxis_showscale=False)
        fig_country = style_fig(
            fig_country, "Top 10 Countries by Number of Titles", height=440)
        chart_card(fig_country)

    with c2:
        top_countries_treemap = country_series.value_counts().head(12).reset_index()
        top_countries_treemap.columns = ["country", "count"]
        fig_tree = px.treemap(
            top_countries_treemap, path=["country"], values="count",
            color="count", color_continuous_scale=RED_SCALE,
        )
        fig_tree.update_traces(
            hovertemplate="<b>%{label}</b><br>Titles: %{value}<extra></extra>",
            textinfo="label+value",
        )
        fig_tree.update_layout(coloraxis_showscale=False)
        fig_tree = style_fig(fig_tree, "Country Share (Treemap)", height=440)
        chart_card(fig_tree)

    st.markdown('<div class="section-title">Genre Landscape</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Most common genres, and how each content type leans genre-wise.</div>',
        unsafe_allow_html=True,
    )

    c3, c4 = st.columns([1, 1])

    with c3:
        genre_series = explode_column(df, "listed_in")
        top_genres = genre_series.value_counts().head(10).sort_values()
        fig_genre = px.bar(
            x=top_genres.values, y=top_genres.index, orientation="h",
            color=top_genres.values, color_continuous_scale=RED_SCALE,
            labels={"x": "Number of Titles", "y": "Genre"}, text=top_genres.values,
        )
        fig_genre.update_traces(
            hovertemplate="<b>%{y}</b><br>Titles: %{x}<extra></extra>", textposition="outside",
        )
        fig_genre.update_layout(coloraxis_showscale=False)
        fig_genre = style_fig(fig_genre, "Top 10 Genres")
        chart_card(fig_genre)

    with c4:
        genre_df = df[["type", "listed_in"]].dropna().copy()
        genre_df["listed_in"] = genre_df["listed_in"].str.split(", ")
        genre_df = genre_df.explode("listed_in")
        top_genre_names = genre_df["listed_in"].value_counts().head(8).index
        genre_df = genre_df[genre_df["listed_in"].isin(top_genre_names)]
        genre_sun = genre_df.groupby(
            ["type", "listed_in"]).size().reset_index(name="count")
        fig_sun = px.sunburst(
            genre_sun, path=["type", "listed_in"], values="count",
            color="count", color_continuous_scale=RED_SCALE,
        )
        fig_sun.update_traces(
            hovertemplate="<b>%{label}</b><br>Titles: %{value}<extra></extra>")
        fig_sun.update_layout(coloraxis_showscale=False)
        fig_sun = style_fig(
            fig_sun, "Genre Breakdown by Content Type (Sunburst)")
        chart_card(fig_sun)

# ------------------------------------------------------------------------------
# TAB 3 — TRENDS & DURATION
# ------------------------------------------------------------------------------
with tab_trends:
    st.markdown('<div class="section-title">Release Trends Over Time</div>',
                unsafe_allow_html=True)

    c1, c2 = st.columns([1.4, 1])

    with c1:
        year_type_counts = df.groupby(
            ["release_year", "type"]).size().reset_index(name="count")
        fig_year = px.area(
            year_type_counts, x="release_year", y="count", color="type",
            color_discrete_map={"Movie": "#e50914", "TV Show": "#5a5f6e"},
            labels={"release_year": "Release Year",
                    "count": "Number of Titles", "type": "Type"},
        )
        fig_year.update_traces(
            hovertemplate="Year: %{x}<br>Titles: %{y}<extra></extra>")
        fig_year = style_fig(
            fig_year, "Titles Released by Year (by Type)", height=440)
        chart_card(fig_year)

    with c2:
        if "date_added" in df.columns and df["date_added"].notna().any():
            added = df.dropna(subset=["date_added"]).copy()
            added["year_month"] = added["date_added"].dt.to_period(
                "M").dt.to_timestamp()
            monthly = added.groupby(
                "year_month").size().reset_index(name="count")
            fig_added = px.line(
                monthly, x="year_month", y="count", markers=True,
                labels={"year_month": "Date Added", "count": "Titles Added"},
            )
            fig_added.update_traces(
                line=dict(color="#ff3b47", width=2.5),
                hovertemplate="%{x|%b %Y}<br>Added: %{y}<extra></extra>",
            )
            fig_added = style_fig(
                fig_added, "Titles Added to Netflix Over Time", height=440)
            chart_card(fig_added)
        else:
            st.info("`date_added` column not available for this view.")

    st.markdown('<div class="section-title">Duration Analysis</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Movie runtimes and how release year relates to duration.</div>',
        unsafe_allow_html=True,
    )

    c3, c4 = st.columns([1, 1])

    with c3:
        movie_durations = get_movie_durations(df)
        if not movie_durations.empty:
            fig_duration = px.histogram(
                movie_durations, x="duration_minutes", nbins=30,
                color_discrete_sequence=["#e50914"],
                labels={"duration_minutes": "Duration (minutes)"},
                marginal="box",
            )
            fig_duration.update_traces(
                hovertemplate="Duration: %{x} min<br>Movies: %{y}<extra></extra>",
                selector=dict(type="histogram"),
            )
            fig_duration.update_layout(yaxis_title="Number of Movies")
            fig_duration = style_fig(
                fig_duration, "Movie Duration Distribution", height=440)
            chart_card(fig_duration)
        else:
            st.info("No movies in the current filter selection to show duration for.")

    with c4:
        if not movie_durations.empty:
            recent_decades = movie_durations.copy()
            recent_decades["decade"] = (
                recent_decades["release_year"] // 10 * 10).astype(str) + "s"
            fig_box = px.box(
                recent_decades, x="decade", y="duration_minutes",
                color="decade", color_discrete_sequence=px.colors.sequential.Reds[::-1],
                labels={"decade": "Decade",
                        "duration_minutes": "Duration (minutes)"},
            )
            fig_box.update_traces(
                hovertemplate="Decade: %{x}<br>Duration: %{y} min<extra></extra>")
            fig_box.update_layout(showlegend=False)
            fig_box = style_fig(
                fig_box, "Movie Duration by Decade", height=440)
            chart_card(fig_box)
        else:
            st.info("No movies available to break down by decade.")

# ------------------------------------------------------------------------------
# TAB 4 — EXPLORE DATA
# ------------------------------------------------------------------------------
with tab_data:
    st.markdown('<div class="section-title">Filtered Dataset</div>',
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-caption">Showing {total_titles:,} of {len(df_raw):,} total titles '
        "based on current filters.</div>",
        unsafe_allow_html=True,
    )

    search_term = st.text_input(
        "🔎 Search by title", placeholder="Type a title to filter the table...")

    display_cols = [
        c for c in [
            "title", "type", "country", "release_year",
            "rating", "duration", "listed_in", "date_added",
        ] if c in df.columns
    ]

    table_df = df[display_cols]
    if search_term:
        table_df = table_df[table_df["title"].str.contains(
            search_term, case=False, na=False)]

    st.dataframe(table_df, use_container_width=True, height=420)

    csv_bytes = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="netflix_filtered_data.csv",
        mime="text/csv",
    )

# ==============================================================================
# 10. FOOTER
# ==============================================================================
st.markdown("---")
st.caption(
    "Netflix Content Analytics Dashboard · Built with Streamlit & Plotly · "
    "Data cleaned and analyzed in a companion EDA notebook."
)
