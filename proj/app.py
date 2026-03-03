import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(
    page_title='Tech Hiring & Layoffs: Workforce Data (2000–2025)',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background with ambient blobs */
.stApp {
    background: #0d1117;
    background-image:
        radial-gradient(ellipse 50% 35% at 15% 10%, rgba(0,210,255,0.05) 0%, transparent 65%),
        radial-gradient(ellipse 40% 30% at 85% 85%, rgba(123,47,255,0.05) 0%, transparent 65%),
        radial-gradient(ellipse 30% 25% at 50% 50%, rgba(0,150,255,0.02) 0%, transparent 70%);
    color: #e6edf3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d1117;
    border-right: 1px solid rgba(0,210,255,0.12);
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* Sidebar label & text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    color: #8b949e !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

/* Sidebar multiselect */
[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 8px !important;
    color: #c9d1d9 !important;
}
[data-testid="stSidebar"] [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(0,210,255,0.12) !important;
    border: 1px solid rgba(0,210,255,0.25) !important;
    border-radius: 6px !important;
    color: #00d2ff !important;
    font-size: 0.72rem !important;
}

/* Sidebar slider */
[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
    background: #00d2ff !important;
    border-color: #00d2ff !important;
}
[data-testid="stSidebar"] [data-testid="stSlider"] div[data-baseweb="slider"] div[data-testid="stThumbValue"] {
    color: #00d2ff !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #21262d !important;
    margin: 0.8rem 0 !important;
}

/* Sidebar title card */
.sidebar-title {
    background: linear-gradient(135deg, rgba(0,210,255,0.08) 0%, rgba(123,47,255,0.06) 100%);
    border: 1px solid rgba(0,210,255,0.15);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 1.2rem;
}
.sidebar-title-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #00d2ff;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.sidebar-title-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #f0f6fc;
}

/* Sidebar status pill */
.sidebar-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(63,185,80,0.07);
    border: 1px solid rgba(63,185,80,0.2);
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    margin-top: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #6e7681;
}
.sidebar-status .dot-green {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #3fb950;
    flex-shrink: 0;
    animation: pulse-glow 2s ease-in-out infinite;
}
.sidebar-status span { color: #3fb950; }

/* Main content padding */
.main .block-container {
    padding: 2rem 3rem 3rem 3rem;
    max-width: 1400px;
}

/* Hero header */
@keyframes scanline {
    0%   { transform: translateY(-100%); }
    100% { transform: translateY(400%); }
}
@keyframes pulse-glow {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.6; }
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
}

.hero-header {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(ellipse 80% 60% at 50% 0%, rgba(0,210,255,0.07) 0%, transparent 70%),
        linear-gradient(160deg, #070d1a 0%, #0a1628 40%, #080d1c 100%);
    border: 1px solid rgba(0, 210, 255, 0.18);
    border-radius: 16px;
    padding: 2.8rem 3rem 2.4rem 3rem;
    margin-bottom: 2rem;
    box-shadow:
        0 0 0 1px rgba(0,210,255,0.05),
        0 8px 40px rgba(0,0,0,0.6),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

/* dot-grid background */
.hero-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(0,210,255,0.12) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
}

/* animated scan line */
.hero-header::after {
    content: '';
    position: absolute;
    left: 0; right: 0;
    height: 60px;
    background: linear-gradient(to bottom,
        transparent 0%,
        rgba(0,210,255,0.04) 50%,
        transparent 100%);
    animation: scanline 4s linear infinite;
    pointer-events: none;
}

/* top accent bar */
.hero-top-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        #00d2ff 30%,
        #7b2fff 70%,
        transparent 100%);
    border-radius: 16px 16px 0 0;
}

.hero-inner { position: relative; z-index: 1; text-align: center; }

/* prompt tag */
.hero-prompt {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #00d2ff;
    background: rgba(0,210,255,0.08);
    border: 1px solid rgba(0,210,255,0.2);
    border-radius: 6px;
    padding: 0.25rem 0.7rem;
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
}
.hero-prompt .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00d2ff;
    animation: pulse-glow 2s ease-in-out infinite;
}

/* main title */
.hero-title {
    font-family: 'Space Grotesk', 'Inter', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.15;
    margin: 0 0 0.9rem 0;
    letter-spacing: -0.5px;
    background: linear-gradient(120deg, #e0f7ff 0%, #58cfff 35%, #a78bfa 70%, #e0f7ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 20px rgba(0,210,255,0.3));
}

/* subtitle row */
.hero-sub {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.hero-sub-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #6e7681;
    letter-spacing: 0.02em;
}
.hero-sub-text span { color: #58a6ff; }
.hero-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    color: #3fb950;
    background: rgba(63,185,80,0.1);
    border: 1px solid rgba(63,185,80,0.25);
    border-radius: 20px;
    padding: 0.2rem 0.65rem;
    letter-spacing: 0.05em;
}

/* corner brackets */
.hero-corner {
    position: absolute;
    width: 16px; height: 16px;
    border-color: rgba(0,210,255,0.35);
    border-style: solid;
}
.hero-corner.tl { top: 10px; left: 10px; border-width: 2px 0 0 2px; border-radius: 3px 0 0 0; }
.hero-corner.tr { top: 10px; right: 10px; border-width: 2px 2px 0 0; border-radius: 0 3px 0 0; }
.hero-corner.bl { bottom: 10px; left: 10px; border-width: 0 0 2px 2px; border-radius: 0 0 0 3px; }
.hero-corner.br { bottom: 10px; right: 10px; border-width: 0 2px 2px 0; border-radius: 0 0 3px 0; }

/* Metric cards */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    flex: 1;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #388bfd; }
.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f0f6fc;
}
.metric-value.green { color: #3fb950; }
.metric-value.red   { color: #f85149; }
.metric-value.blue  { color: #58a6ff; }
.metric-value.purple{ color: #bc8cff; }

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.5rem 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid transparent;
    background-image: linear-gradient(#0d1117, #0d1117),
                      linear-gradient(90deg, rgba(0,210,255,0.4) 0%, rgba(123,47,255,0.2) 50%, transparent 100%);
    background-origin: border-box;
    background-clip: padding-box, border-box;
    border-image: linear-gradient(90deg, rgba(0,210,255,0.35), rgba(123,47,255,0.15), transparent) 1;
    border-bottom-width: 1px;
    border-bottom-style: solid;
}
.section-number {
    background: linear-gradient(135deg, #1f6feb 0%, #7b2fff 100%);
    color: white;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    width: 26px;
    height: 26px;
    border-radius: 7px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 10px rgba(31,111,235,0.4);
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f0f6fc;
    letter-spacing: -0.2px;
}

/* Plotly chart container glow */
[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #21262d;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), 0 0 0 1px rgba(0,210,255,0.04);
    transition: border-color 0.3s, box-shadow 0.3s;
}
[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(0,210,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 20px rgba(0,210,255,0.06);
}

/* Chart caption */
.chart-caption {
    text-align: center;
    color: #484f58;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    margin-top: 0.4rem;
    padding-bottom: 0.6rem;
    letter-spacing: 0.02em;
}

/* Insight block (description under charts) */
.insight {
    position: relative;
    color: #8b949e;
    font-size: 0.87rem;
    line-height: 1.8;
    margin: 0.6rem 0 1.2rem 0;
    padding: 0.9rem 1.2rem;
    background: rgba(0,210,255,0.025);
    border-left: 2px solid rgba(0,210,255,0.35);
    border-radius: 0 8px 8px 0;
}
.insight strong { color: #c9d1d9; }

/* Gradient divider */
.custom-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(0,210,255,0.2) 30%,
        rgba(123,47,255,0.15) 70%,
        transparent 100%);
    margin: 2rem 0;
}

/* Hide default Streamlit elements */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* Keep sidebar toggle button visible */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    color: #8b949e;
}
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('tech_employment_2000_2025.csv')

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
      <div class="sidebar-title-label">⚙ Control Panel</div>
      <div class="sidebar-title-text">データフィルター</div>
    </div>
    """, unsafe_allow_html=True)

    all_companies = sorted(df['company'].unique())
    selected = st.multiselect(
        '企業を選択',
        all_companies,
        default=all_companies,
    )
    st.markdown("")
    year_range = st.slider(
        '年の範囲',
        int(df['year'].min()), int(df['year'].max()),
        (2000, 2025),
    )
    st.markdown(f"""
    <div class="sidebar-status">
      <div class="dot-green"></div>
      <span>{len(selected)}</span> 社選択中 &nbsp;·&nbsp; {year_range[0]}–{year_range[1]} 年
    </div>
    """, unsafe_allow_html=True)

if not selected:
    st.warning('企業を 1 社以上選択してください。')
    st.stop()

filtered_df = df[df['company'].isin(selected) & df['year'].between(*year_range)]

# ── Plotly shared theme ───────────────────────────────────────────────────────
CHART_BG   = '#0d1117'
PAPER_BG   = '#161b22'
GRID_COLOR = '#21262d'
FONT_COLOR = '#c9d1d9'
AXIS_COLOR = '#6e7681'

def apply_theme(fig, height=420):
    fig.update_layout(
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family='Inter', color=FONT_COLOR, size=12),
        margin=dict(l=20, r=20, t=40, b=40),
        legend=dict(
            bgcolor='rgba(22,27,34,0.8)',
            bordercolor='#21262d',
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR, linecolor=AXIS_COLOR,
            tickcolor=AXIS_COLOR, tickfont=dict(color=AXIS_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR, linecolor=AXIS_COLOR,
            tickcolor=AXIS_COLOR, tickfont=dict(color=AXIS_COLOR),
            title_font=dict(color=FONT_COLOR),
        ),
    )
    return fig

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <div class="hero-top-bar"></div>
  <div class="hero-corner tl"></div>
  <div class="hero-corner tr"></div>
  <div class="hero-corner bl"></div>
  <div class="hero-corner br"></div>
  <div class="hero-inner">
    <div class="hero-prompt">
      <span class="dot"></span>
      WORKFORCE_ANALYTICS &nbsp;/&nbsp; LIVE DASHBOARD
    </div>
    <div class="hero-title">テクノロジー業界<br>雇用データ 2001–2025</div>
    <div class="hero-sub">
      <div class="hero-sub-text">出典: Aryan Mishra 提供データを基に作成</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Section 1: Line Chart ─────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-number">1</div>
  <div class="section-title">従業員数の推移</div>
</div>
""", unsafe_allow_html=True)

metric_options = {
    '従業員数（人）': 'employees_end',
    '採用数（人）':   'new_hires',
    'レイオフ数':     'layoffs',
    '売上高':         'revenue_billions_usd',
}
chosen_label = st.selectbox('指標を選択', list(metric_options.keys()), label_visibility='collapsed')
chosen_col   = metric_options[chosen_label]

COLOR_SEQ = px.colors.qualitative.Vivid
fig1 = px.line(
    filtered_df, x='year', y=chosen_col, color='company',
    markers=True,
    color_discrete_sequence=COLOR_SEQ,
    labels={'year': '年', chosen_col: chosen_label, 'company': '企業'},
)
fig1.update_traces(line=dict(width=2.5), marker=dict(size=6))
fig1 = apply_theme(fig1)
st.plotly_chart(fig1, use_container_width=True)
st.markdown(f'<div class="chart-caption">図1. 企業別{chosen_label}の推移（{year_range[0]}〜{year_range[1]}年）</div>', unsafe_allow_html=True)
st.markdown("""
<p class="insight">
本折れ線グラフは、各テクノロジー企業における従業員数、採用数、レイオフ数および売上高の経年推移を示したものである。数値の変動を時系列で比較することにより、各企業の成長過程や事業規模の拡大・縮小の動向を把握することができる。また、急激な上昇は事業拡大期を示唆し、下降は人員削減や景気後退の影響を反映していると考えられる。これにより、IT業界全体における構造的変化を時系列的に分析することが可能である。
</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── Section 2: Bar Chart ──────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-number">2</div>
  <div class="section-title">採用数とレイオフ数の比較</div>
</div>
""", unsafe_allow_html=True)

yearly = (
    filtered_df.groupby('year')
    .agg(sum_newhire=('new_hires', 'sum'), sum_layoff=('layoffs', 'sum'))
    .reset_index()
)

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=yearly['year'], y=yearly['sum_newhire'],
    name='採用合計', marker_color='#3fb950',
    marker_line_width=0,
))
fig2.add_trace(go.Bar(
    x=yearly['year'], y=-yearly['sum_layoff'],
    name='レイオフ合計', marker_color='#f85149',
    marker_line_width=0,
))
fig2.update_layout(
    barmode='relative',
    xaxis_title='年', yaxis_title='人数（人）',
    legend=dict(orientation='h', y=1.06, x=0),
)
fig2 = apply_theme(fig2)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('<div class="chart-caption">図2. 選択企業の年間採用合計とレイオフ合計の比較</div>', unsafe_allow_html=True)
st.markdown("""
<p class="insight">
本グラフは、選択したテクノロジー企業における年間採用数の合計とレイオフ数の合計を比較したものである。採用数は正の値、レイオフ数は負の値として表示することで、各年における人員の増減傾向を明確に把握することができる。
全体的に見ると、採用数は複数の期間において増加傾向を示しており、業界の拡大を反映していると考えられる。一方で、特定の年にはレイオフ数の増加も見られ、景気の減速や企業の組織再編・経営戦略の見直しなどの影響が示唆される。
</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── Section 3: Histogram / KDE ────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-number">3</div>
  <div class="section-title">採用率の分布</div>
</div>
""", unsafe_allow_html=True)

COLORS = px.colors.qualitative.Vivid
fig3 = go.Figure()
for i, company in enumerate(selected):
    vals  = filtered_df[filtered_df['company'] == company]['hiring_rate_pct'].dropna()
    if vals.empty:
        continue
    color = COLORS[i % len(COLORS)]
    fig3.add_trace(go.Histogram(
        x=vals, name=company, opacity=0.45,
        histnorm='probability density',
        nbinsx=20, marker_color=color,
        marker_line_width=0,
    ))
    if len(vals) >= 5:
        kde = stats.gaussian_kde(vals)
        xs  = np.linspace(vals.min(), vals.max(), 200)
        fig3.add_trace(go.Scatter(
            x=xs, y=kde(xs), mode='lines',
            name=f'{company} KDE', showlegend=False,
            line=dict(color=color, width=2.5),
        ))

fig3.update_layout(
    barmode='overlay',
    xaxis_title='採用率（%）', yaxis_title='確率密度',
)
fig3 = apply_theme(fig3)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('<div class="chart-caption">図3. 企業別採用率（%）の確率分布（KDE付き）</div>', unsafe_allow_html=True)
st.markdown("""
<p class="insight">
本グラフは、各企業における採用率（％）の分布を示したものであり、採用戦略の違いや人員拡大の度合いを比較・分析することを目的としている。分布の特徴を検討することで、各企業の成長傾向や変動の大きさ、さらには雇用構造上の差異を明らかにすることが可能である。
</p>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── Section 4: Scatter Plot ───────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-number">4</div>
  <div class="section-title">売上高 vs 従業員数</div>
</div>
""", unsafe_allow_html=True)

fig4 = px.scatter(
    filtered_df,
    x='revenue_billions_usd', y='employees_end',
    color='company', size='new_hires',
    hover_data=['year'],
    trendline='ols',
    color_discrete_sequence=COLOR_SEQ,
    labels={
        'revenue_billions_usd': '売上高（10億USD）',
        'employees_end':        '従業員数（人）',
        'company':              '企業',
        'new_hires':            '採用数',
    },
    size_max=32,
)
fig4.update_traces(marker=dict(opacity=0.8, line=dict(width=0)))
fig4 = apply_theme(fig4)
st.plotly_chart(fig4, use_container_width=True)
st.markdown('<div class="chart-caption">図4. 売上高と従業員数の関係（バブルサイズ ＝ 採用数、OLS回帰直線付き）</div>', unsafe_allow_html=True)
st.markdown("""
<p class="insight">
本散布図は、各テクノロジー企業の売上高（横軸）と従業員数（縦軸）の関係を示したものである。バブルの大きさは採用数を表しており、事業規模と人員規模の相関を視覚的に把握することができる。OLS回帰直線が示すとおり、売上高の増加に伴い従業員数も増加する傾向が全体的に確認されるが、企業ごとに傾きの異なる分布が見られることから、人的資本の活用効率や事業モデルの違いが反映されていると考えられる。バブルサイズの大きい点は積極的な採用期を示しており、成長戦略との連動性を読み取ることも可能である。
</p>
""", unsafe_allow_html=True)
