import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Tech Industry Workforce Dashboard",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Background ── */
.stApp {
    background: linear-gradient(160deg, #0d1117 0%, #161b22 60%, #0d1f3c 100%);
    background-attachment: fixed;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(13,17,23,0.95) !important;
    border-right: 1px solid rgba(99,179,237,0.15) !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label { color: rgba(255,255,255,0.6) !important; font-size: 0.82rem; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 20px;
    padding: 44px 56px;
    margin-bottom: 28px;
    box-shadow: 0 8px 40px rgba(0,0,0,0.6);
    text-align: center;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #63b3ed, #b794f4, #fc8181);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 10px;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: rgba(255,255,255,0.55);
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

/* ── KPI Cards ── */
.kpi-row { display: flex; gap: 16px; margin-bottom: 28px; }
.kpi-card {
    flex: 1;
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 22px 20px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.4); }
.kpi-icon  { font-size: 1.8rem; margin-bottom: 8px; }
.kpi-label { color: rgba(255,255,255,0.45); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; margin-bottom: 6px; }
.kpi-value { color: #fff; font-size: 1.75rem; font-weight: 700; line-height: 1; }
.kpi-card.blue  { border-top: 3px solid #63b3ed; }
.kpi-card.green { border-top: 3px solid #68d391; }
.kpi-card.orange{ border-top: 3px solid #f6ad55; }
.kpi-card.red   { border-top: 3px solid #fc8181; }

/* ── Section cards ── */
.section-wrap {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 28px 28px 8px;
    margin-bottom: 24px;
}
.section-title {
    color: #fff;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title span.pill {
    background: rgba(99,179,237,0.15);
    color: #63b3ed;
    font-size: 0.7rem;
    padding: 3px 10px;
    border-radius: 99px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Insight box ── */
.insight-box {
    background: linear-gradient(135deg, rgba(99,179,237,0.08), rgba(183,148,244,0.08));
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 14px;
    padding: 20px 24px;
    margin-top: 8px;
}
.insight-box ul { margin: 0; padding-left: 18px; }
.insight-box li { color: rgba(255,255,255,0.75); font-size: 0.93rem; margin-bottom: 6px; line-height: 1.6; }
.insight-box li strong { color: #fff; }

/* ── Correlation badge ── */
.corr-badge {
    display: inline-block;
    background: rgba(99,179,237,0.12);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 8px;
    padding: 8px 18px;
    color: #63b3ed;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 8px;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 28px !important;
    transition: all 0.25s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(102,126,234,0.45) !important;
}

/* ── Radio ── */
.stRadio [data-testid="stMarkdownContainer"] p { color: rgba(255,255,255,0.7) !important; }
.stRadio label { color: rgba(255,255,255,0.8) !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── Misc ── */
hr { border-color: rgba(255,255,255,0.07) !important; }
#MainMenu, footer { visibility: hidden; }
.stAlert { border-radius: 12px; }

/* override white text for main area */
.stApp p, .stApp label, .stApp span { color: rgba(255,255,255,0.85); }
</style>
""", unsafe_allow_html=True)

def style_fig(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="rgba(255,255,255,0.8)", size=12),
        margin=dict(l=16, r=16, t=56, b=16),
        height=height,
        title_font=dict(size=14, color="rgba(255,255,255,0.9)", family="Inter"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.04)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)"),
    )
    return fig

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("tech_employment_2000_2025.csv")
    df["is_estimated"] = df["is_estimated"].astype(str).str.lower() == "true"
    return df

df_all = load_data()

with st.sidebar:
    st.markdown("### Filters")
    st.markdown("---")

    all_companies = sorted(df_all["company"].unique())
    selected_companies = st.multiselect(
        "Companies",
        options=all_companies,
        default=["Apple", "Microsoft", "Meta", "Amazon", "NVIDIA", "Intel"],
    )
    if not selected_companies:
        selected_companies = all_companies

    year_min = int(df_all["year"].min())
    year_max = int(df_all["year"].max())
    year_range = st.slider("Year Range", year_min, year_max, (2010, 2025))

    confidence_opts = sorted(df_all["confidence_level"].unique())
    selected_conf = st.multiselect(
        "Confidence Level", options=confidence_opts, default=confidence_opts
    )
    if not selected_conf:
        selected_conf = confidence_opts

    st.markdown("---")
    st.markdown("<small style='color:rgba(255,255,255,0.35)'>Source: tech_employment_2000_2025.csv</small>", unsafe_allow_html=True)

df = df_all[
    df_all["company"].isin(selected_companies)
    & df_all["year"].between(year_range[0], year_range[1])
    & df_all["confidence_level"].isin(selected_conf)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust the filters.")
    st.stop()

st.markdown("""
<div class="hero">
    <div class="hero-title">Tech Industry Workforce Dashboard</div>
    <p class="hero-sub">Analyzing hiring, layoffs, revenue &amp; stock trends across 25 major tech companies · 2001–2025</p>
</div>
""", unsafe_allow_html=True)

total_layoffs = int(df["layoffs"].sum())
total_hires   = int(df["new_hires"].sum())
peak_layoff_year = int(df.groupby("year")["layoffs"].sum().idxmax())
biggest_event_row = df_all.loc[df["layoffs"].idxmax()]
biggest_event = f"{biggest_event_row['company']} {int(biggest_event_row['year'])}"

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-card red">
        <div class="kpi-icon">📉</div>
        <div class="kpi-label">Total Layoffs</div>
        <div class="kpi-value">{total_layoffs:,}</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-icon">🚀</div>
        <div class="kpi-label">Total New Hires</div>
        <div class="kpi-value">{total_hires:,}</div>
    </div>
    <div class="kpi-card orange">
        <div class="kpi-icon">📅</div>
        <div class="kpi-label">Peak Layoff Year</div>
        <div class="kpi-value">{peak_layoff_year}</div>
    </div>
    <div class="kpi-card blue">
        <div class="kpi-icon">⚡</div>
        <div class="kpi-label">Biggest Layoff Event</div>
        <div class="kpi-value" style="font-size:1.1rem;padding-top:4px">{biggest_event}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">📈 Employment Over Time <span class="pill">by Company</span></div>', unsafe_allow_html=True)

fig_timeline = px.line(
    df, x="year", y="employees_end", color="company", markers=True,
    title="Year-End Headcount by Company",
    labels={"employees_end": "Employees (Year-End)", "year": "Year", "company": "Company"},
)
style_fig(fig_timeline, height=420)
fig_timeline.update_traces(line=dict(width=2.2), marker=dict(size=6))
st.plotly_chart(fig_timeline, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">⚖️ Hiring vs Layoffs <span class="pill">Total in Period</span></div>', unsafe_allow_html=True)

hv = (
    df.groupby("company")[["new_hires", "layoffs"]]
    .sum().reset_index().sort_values("layoffs", ascending=False)
)

fig_hv = go.Figure()
fig_hv.add_bar(x=hv["company"], y=hv["new_hires"], name="New Hires",
               marker_color="#4fc3f7", marker_opacity=0.9)
fig_hv.add_bar(x=hv["company"], y=hv["layoffs"], name="Layoffs",
               marker_color="#ef5350", marker_opacity=0.9)
fig_hv.update_layout(barmode="group", title="New Hires vs Layoffs by Company",
                     xaxis_title="Company", yaxis_title="Headcount")
style_fig(fig_hv, height=400)
st.plotly_chart(fig_hv, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">🔥 Layoff Heatmap <span class="pill">Company × Year</span></div>', unsafe_allow_html=True)

pivot = df.pivot_table(index="company", columns="year", values="layoffs", aggfunc="sum").fillna(0)
fig_heat = px.imshow(
    pivot, color_continuous_scale="Inferno",
    title="Layoffs Heatmap — brighter = more layoffs",
    labels=dict(x="Year", y="Company", color="Layoffs"),
    aspect="auto",
)
style_fig(fig_heat, height=450)
fig_heat.update_coloraxes(colorbar=dict(tickfont=dict(color="rgba(255,255,255,0.6)")))
st.plotly_chart(fig_heat, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">💰 Revenue vs Headcount <span class="pill">Bubble = Layoffs</span></div>', unsafe_allow_html=True)

fig_rev = px.scatter(
    df, x="employees_end", y="revenue_billions_usd", color="company",
    size="layoffs", size_max=40,
    hover_data={"year": True, "layoffs": True, "new_hires": True},
    trendline="ols", trendline_scope="overall",
    title="Revenue (USD bn) vs Employees",
    labels={"employees_end": "Employees (Year-End)", "revenue_billions_usd": "Revenue (USD bn)"},
)
style_fig(fig_rev, height=460)
fig_rev.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.2)")))
st.plotly_chart(fig_rev, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">📉 Do Layoffs Affect Stock Price? <span class="pill">Scatter</span></div>', unsafe_allow_html=True)

fig_stock = px.scatter(
    df, x="layoffs", y="stock_price_change_pct", color="company",
    size="layoffs", size_max=35,
    hover_data={"year": True, "layoffs": True},
    trendline="ols", trendline_scope="overall",
    title="Layoffs vs Stock Price Change (%) — each point = 1 company-year",
    labels={"layoffs": "Layoffs", "stock_price_change_pct": "Stock Price Change (%)"},
)
fig_stock.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)", line_width=1)
style_fig(fig_stock, height=430)
fig_stock.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.15)")))
st.plotly_chart(fig_stock, use_container_width=True)

corr_val = df[["layoffs", "stock_price_change_pct"]].corr().iloc[0, 1]
st.markdown(f'<div class="corr-badge">📊 Pearson correlation (layoffs ↔ stock change): <strong>{corr_val:.3f}</strong></div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">⚠️ Industry-Wide Layoffs <span class="pill">Crisis Periods</span></div>', unsafe_allow_html=True)

agg_year = df.groupby("year")["layoffs"].sum().reset_index()
fig_crisis = px.bar(
    agg_year, x="year", y="layoffs",
    title="Total Layoffs per Year (all selected companies)",
    labels={"layoffs": "Total Layoffs", "year": "Year"},
    color="layoffs", color_continuous_scale="Sunset",
)
style_fig(fig_crisis, height=390)
fig_crisis.update_traces(marker_line_width=0)

crisis_years = {2001: "Dot-com bust", 2008: "Financial crisis", 2020: "COVID-19", 2022: "Tech downturn"}
for yr, label in crisis_years.items():
    if year_range[0] <= yr <= year_range[1]:
        fig_crisis.add_vline(x=yr, line_dash="dot", line_color="rgba(252,129,129,0.7)", line_width=1.5)
        fig_crisis.add_annotation(
            x=yr, y=agg_year["layoffs"].max() * 0.92,
            text=label, showarrow=False, textangle=-45,
            font=dict(size=10, color="#fc8181"),
        )

st.plotly_chart(fig_crisis, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">🌐 Macro Economy vs Tech Layoffs <span class="pill">Dual Axis</span></div>', unsafe_allow_html=True)

macro = df.groupby("year").agg(
    total_layoffs=("layoffs", "sum"),
    avg_unemployment=("unemployment_rate_us_pct", "mean"),
    avg_gdp=("gdp_growth_us_pct", "mean"),
).reset_index()

fig_macro = make_subplots(specs=[[{"secondary_y": True}]])
fig_macro.add_trace(
    go.Bar(x=macro["year"], y=macro["total_layoffs"], name="Total Layoffs",
           marker_color="#ef5350", marker_opacity=0.8, marker_line_width=0),
    secondary_y=False,
)
fig_macro.add_trace(
    go.Scatter(x=macro["year"], y=macro["avg_unemployment"],
               name="US Unemployment (%)", mode="lines+markers",
               line=dict(color="#4fc3f7", width=2.5),
               marker=dict(size=6)),
    secondary_y=True,
)
fig_macro.add_trace(
    go.Scatter(x=macro["year"], y=macro["avg_gdp"],
               name="US GDP Growth (%)", mode="lines+markers",
               line=dict(color="#81c784", width=2.5, dash="dash"),
               marker=dict(size=6)),
    secondary_y=True,
)
fig_macro.update_layout(
    title="Total Layoffs vs US Unemployment Rate & GDP Growth",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(255,255,255,0.04)",
                bordercolor="rgba(255,255,255,0.08)", borderwidth=1),
)
style_fig(fig_macro, height=430)
fig_macro.update_yaxes(title_text="Total Layoffs", secondary_y=False,
                        gridcolor="rgba(255,255,255,0.05)", color="rgba(255,255,255,0.7)")
fig_macro.update_yaxes(title_text="Rate (%)", secondary_y=True,
                        color="rgba(255,255,255,0.7)")
st.plotly_chart(fig_macro, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">🏆 Company Ranking <span class="pill">by Metric</span></div>', unsafe_allow_html=True)

rank_metric = st.radio(
    "Rank by:",
    ["Net Change (headcount)", "Hiring Rate (%)", "Attrition Rate (%)", "Revenue (USD bn)"],
    horizontal=True,
)
metric_map = {
    "Net Change (headcount)": "net_change",
    "Hiring Rate (%)": "hiring_rate_pct",
    "Attrition Rate (%)": "attrition_rate_pct",
    "Revenue (USD bn)": "revenue_billions_usd",
}
col = metric_map[rank_metric]
rank_df = df.groupby("company")[col].mean().reset_index().sort_values(col, ascending=True)

fig_rank = px.bar(
    rank_df, x=col, y="company", orientation="h",
    title=f"Average {rank_metric} per Company (selected period)",
    labels={"company": "Company", col: rank_metric},
    color=col, color_continuous_scale="Viridis",
)
style_fig(fig_rank, height=460)
fig_rank.update_traces(marker_line_width=0)
st.plotly_chart(fig_rank, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">📊 Attrition Rate Trend <span class="pill">by Company</span></div>', unsafe_allow_html=True)

fig_attr = px.line(
    df, x="year", y="attrition_rate_pct", color="company", markers=True,
    title="Attrition Rate (%) Over Time",
    labels={"attrition_rate_pct": "Attrition Rate (%)", "year": "Year"},
)
style_fig(fig_attr, height=390)
fig_attr.update_traces(line=dict(width=2.2), marker=dict(size=6))
st.plotly_chart(fig_attr, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-wrap"><div class="section-title">🗂️ Data Table</div>', unsafe_allow_html=True)

show_cols = [
    "company", "year", "employees_start", "employees_end",
    "new_hires", "layoffs", "net_change", "hiring_rate_pct",
    "attrition_rate_pct", "revenue_billions_usd",
    "stock_price_change_pct", "confidence_level",
]
st.dataframe(df[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True)

csv_bytes = df[show_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered Data (CSV)",
    data=csv_bytes,
    file_name="tech_workforce_filtered.csv",
    mime="text/csv",
)
st.markdown("</div>", unsafe_allow_html=True)

top_layoff_co = df.groupby("company")["layoffs"].sum().idxmax()
top_hire_co   = df.groupby("company")["new_hires"].sum().idxmax()
avg_attrition = df["attrition_rate_pct"].mean()
net_industry  = int(df["net_change"].sum())

st.markdown(f"""
<div class="section-wrap">
    <div class="section-title">📝 Summary Insights</div>
    <div class="insight-box">
        <ul>
            <li><strong>Highest total layoffs</strong> in selected period: <strong>{top_layoff_co}</strong></li>
            <li><strong>Highest total hires</strong> in selected period: <strong>{top_hire_co}</strong></li>
            <li><strong>Average attrition rate:</strong> <strong>{avg_attrition:.1f}%</strong> across all selected companies/years</li>
            <li><strong>Net industry headcount change:</strong> <strong>{net_industry:+,}</strong> (selected period)</li>
            <li>Crisis years (2001, 2008, 2020, 2022) show distinct spikes in layoff activity.</li>
            <li>Correlation between layoffs and stock price is often <strong>weak or even positive</strong> — markets sometimes reward cost-cutting.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)
