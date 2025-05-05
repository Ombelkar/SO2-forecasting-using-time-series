import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
file_path = "C:/Users/BAPS/Desktop/combined AQI.csv"
df = pd.read_csv(file_path)
df['Year'] = df['Year'].astype(str)

# --- HEATMAP ---
plt.figure(figsize=(12, 8))
heatmap_data = df.pivot(index="State", columns="Year", values="SO2")
sns.heatmap(heatmap_data, cmap="Reds", annot=True, fmt=".1f", linewidths=0.5,
            cbar_kws={'label': 'SO₂ Levels'})
plt.title("SO₂ Levels Heatmap (State vs Year)")
plt.xlabel("Year")
plt.ylabel("State")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# --- HORIZONTAL LINE PLOT (States on Y-axis) ---
pivot_df = df.pivot(index="State", columns="Year", values="SO2")

# Plot horizontal lines for each state
plt.figure(figsize=(14, 8))
for state in pivot_df.index:
    plt.plot(pivot_df.columns, pivot_df.loc[state], marker='o', label=state)

plt.title("SO₂ Trend per State")
plt.xlabel("Year")
plt.ylabel("State")
plt.yticks(ticks=range(len(pivot_df.index)), labels=pivot_df.index)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()