import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load data
df = pd.read_csv("Dataset/Financials_Analysis_Ready.csv")

# Create output folder
output = Path("Screenshorts")
output.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# Country performance
country = df.groupby("Country")[["Sales", "Profit"]].sum().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(data=country.sort_values("Sales", ascending=False),
            x="Sales", y="Country", ax=axes[0])
axes[0].set_title("Country-wise Sales")
axes[0].set_xlabel("Total Sales")

sns.barplot(data=country.sort_values("Profit", ascending=False),
            x="Profit", y="Country", ax=axes[1])
axes[1].set_title("Country-wise Profit")
axes[1].set_xlabel("Total Profit")

plt.tight_layout()
plt.savefig(output / "Country_Performance.png", dpi=300)
plt.close()

# Product performance
product = df.groupby("Product")[["Sales", "Profit"]].sum().reset_index()

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(data=product.sort_values("Sales", ascending=False),
            x="Sales", y="Product", ax=axes[0])
axes[0].set_title("Product-wise Sales")
axes[0].set_xlabel("Total Sales")

sns.barplot(data=product.sort_values("Profit", ascending=False),
            x="Profit", y="Product", ax=axes[1])
axes[1].set_title("Product-wise Profit")
axes[1].set_xlabel("Total Profit")

plt.tight_layout()
plt.savefig(output / "Product_Performance.png", dpi=300)
plt.close()

print("VISUALIZATION COMPLETED!")
print("Saved: Screenshorts/Country_Performance.png")
print("Saved: Screenshorts/Product_Performance.png")
