import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Tech Workforce Dashboard", layout="wide")
st.title("📊 Tech Hiring & Layoffs Analysis (2000–2025)")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("tech_employment_2000_2025.csv")

df = load_data()

# -----------------------------
# Sidebar Filter
# -----------------------------
st.sidebar.header("Filter")

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, 2025)
)

filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# -----------------------------
# KPI Section
# -----------------------------
total_emp = int(filtered_df["Employment"].sum())
total_layoff = int(filtered_df["Layoffs"].sum())
peak_year = filtered_df.loc[filtered_df["Layoffs"].idxmax()]["Year"]

col1, col2, col3 = st.columns(3)
col1.metric("Total Employment", f"{total_emp:,}")
col2.metric("Total Layoffs", f"{total_layoff:,}")
col3.metric("Peak Layoff Year", int(peak_year))

st.divider()

# -----------------------------
# Line Chart
# -----------------------------
st.subheader("Employment & Layoffs Trend")

fig, ax = plt.subplots()
ax.plot(filtered_df["Year"], filtered_df["Employment"])
ax.plot(filtered_df["Year"], filtered_df["Layoffs"])
ax.set_xlabel("Year")
ax.set_ylabel("Number")
ax.legend(["Employment", "Layoffs"])

st.pyplot(fig)

st.divider()

# -----------------------------
# Moving Average
# -----------------------------
st.subheader("3-Year Moving Average")

filtered_df["Emp_MA"] = filtered_df["Employment"].rolling(3).mean()
filtered_df["Layoff_MA"] = filtered_df["Layoffs"].rolling(3).mean()

fig2, ax2 = plt.subplots()
ax2.plot(filtered_df["Year"], filtered_df["Emp_MA"])
ax2.plot(filtered_df["Year"], filtered_df["Layoff_MA"])
ax2.set_xlabel("Year")
ax2.set_ylabel("Moving Average")
ax2.legend(["Employment MA", "Layoffs MA"])

st.pyplot(fig2)

st.divider()

# -----------------------------
# Correlation
# -----------------------------
st.subheader("Correlation Analysis")

correlation = filtered_df["Employment"].corr(filtered_df["Layoffs"])
st.write(f"Correlation Coefficient: {correlation:.3f}")

if correlation > 0:
    st.write("Employment and layoffs tend to move in the same direction.")
else:
    st.write("Employment and layoffs tend to move in opposite directions.")

st.divider()

# -----------------------------
# Download Button
# -----------------------------
st.download_button(
    "Download Filtered Data",
    filtered_df.to_csv(index=False),
    "filtered_data.csv",
    "text/csv"
)