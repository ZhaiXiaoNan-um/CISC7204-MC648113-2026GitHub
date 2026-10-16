import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.makedirs("visualizations", exist_ok=True)

df_raw = pd.read_csv("export.csv")

target_measures = [
    "Housing insecurity in the past 12 months among adults",
    "Depression among adults"
]

df_filter = df_raw[df_raw["Measure"].isin(target_measures)].copy()

df_pivot = df_filter.pivot_table(
    index=["StateDesc", "LocationName"],
    columns="Measure",
    values="Data_Value",
    aggfunc="first"
).reset_index()

print("Pivot后的所有列名：")
print(df_pivot.columns.tolist())

df_pivot.columns = ["StateName", "CountyName", "HousingInsecurity", "Depression"]
df_clean = df_pivot.dropna()

print(f"\n清洗后有效县记录数量：{len(df_clean)}")
corr_val = df_clean["HousingInsecurity"].corr(df_clean["Depression"])
print(f"住房不安全率 和 抑郁患病率 相关系数：{corr_val:.3f}")

# ========== 图1：相关性热力图 ==========
plt.figure(figsize=(6,5))
corr_matrix = df_clean[["HousingInsecurity", "Depression"]].corr()
sns.heatmap(corr_matrix, annot=True, cmap="RdYlBu_r", fmt=".2f")
plt.title("Correlation: Housing Insecurity vs Adult Depression")
plt.tight_layout()
plt.savefig("visualizations/correlation_heatmap.png", dpi=300)
plt.close()

# ========== 图2：Top10州 抑郁患病率柱状图 ==========
state_data = df_clean.groupby("StateName")["Depression"].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,5))
state_data.plot(kind="bar", color="#c84248")
plt.title("Top 10 US States: Average Adult Depression Prevalence")
plt.ylabel("Prevalence (%)")
plt.xlabel("State")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("visualizations/state_bar.png", dpi=300)
plt.close()

print("\n✅ 两张图成功保存至 visualizations 文件夹！")
