import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# Streamlit Page Setup
# ======================================================
st.set_page_config(page_title="FIFA 23 Intelligence Dashboard", layout="wide")

st.title("⚽ FIFA 23 Intelligence Dashboard")
st.write("An interactive dashboard exploring clubs, nations, and player performance metrics.")

# ======================================================
# Load Data Directly
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_csv("fifa23.csv")
    return df

df = load_data()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# ======================================================
# Data Preparation
# ======================================================
# Create attacking prowess
df["Attacking Prowess"] = df[["Finishing", "Shot Power", "Positioning"]].mean(axis=1)

# Ensure numeric wage column
df["Wage(in Euro)"] = pd.to_numeric(df["Wage(in Euro)"], errors="coerce")

# ======================================================
# Popularity by Club Name
# ======================================================
st.subheader("🌍 Club Popularity (Avg International Reputation)")
club_popularity = (
    df.groupby("Club Name")["International Reputation"]
    .mean()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(10, 6))
club_popularity.head(10).plot(kind="barh", color="#1f77b4", ax=ax1)
ax1.set_xlabel("Average International Reputation")
ax1.set_ylabel("Club Name")
ax1.set_title("Top 10 Most Popular Clubs")
st.pyplot(fig1)

# ======================================================
# Top Players by Attacking Prowess
# ======================================================
st.subheader("⚡ Top 10 Players by Attacking Prowess")
top_attackers = (
    df.sort_values("Attacking Prowess", ascending=False)[
        ["Full Name", "Club Name", "Nationality", "Attacking Prowess", "Overall"]
    ]
    .head(10)
)
st.dataframe(top_attackers)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.barh(top_attackers["Full Name"], top_attackers["Attacking Prowess"], color="#ff7f0e")
ax2.set_xlabel("Attacking Prowess")
ax2.set_ylabel("Player Name")
ax2.set_title("Top 10 Attackers in FIFA 23")
st.pyplot(fig2)

# ======================================================
# Top Nations by Attacking Prowess
# ======================================================
st.subheader("🏴‍☠️ Top Nations by Average Attacking Prowess")
nation_attack = (
    df.groupby("Nationality")["Attacking Prowess"]
    .mean()
    .sort_values(ascending=False)
)

fig3, ax3 = plt.subplots(figsize=(10, 6))
nation_attack.head(10).plot(kind="barh", color="#2ca02c", ax=ax3)
ax3.set_xlabel("Average Attacking Prowess")
ax3.set_ylabel("Nationality")
ax3.set_title("Top 10 Nations by Attacking Strength")
st.pyplot(fig3)

# ======================================================
# Top Clubs by Total Wage
# ======================================================
st.subheader("💰 Top Clubs by Total Wage (in Euro)")
club_wages = df.groupby("Club Name")["Wage(in Euro)"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(10, 6))
club_wages.head(10).plot(kind="barh", color="#9467bd", ax=ax4)
ax4.set_xlabel("Total Wage (€)")
ax4.set_ylabel("Club Name")
ax4.set_title("Top 10 Clubs by Total Wage")
st.pyplot(fig4)

# ======================================================
# Count Top Clubs Whose Skill Moves = 5
# ======================================================
st.subheader("🎯 Clubs with Players Having 5-Star Skill Moves")
five_star = df[df["Skill Moves"] == 5]
club_skill_counts = five_star["Club Name"].value_counts()

st.write(f"Total clubs with at least one 5-star skill player: **{club_skill_counts.count()}**")

fig5, ax5 = plt.subplots(figsize=(10, 6))
club_skill_counts.head(10).plot(kind="barh", color="#d62728", ax=ax5)
ax5.set_xlabel("Number of 5★ Players")
ax5.set_ylabel("Club Name")
ax5.set_title("Top 10 Clubs with 5-Star Skill Players")
st.pyplot(fig5)

# ======================================================
# Footer
# ======================================================
st.markdown("---")
