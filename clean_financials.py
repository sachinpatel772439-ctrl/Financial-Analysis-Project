import pandas as pd

df = pd.read_csv("Dataset/archive/Financials.csv")

df.columns = df.columns.str.strip()

numeric_cols = [
    "Units Sold",
    "Manufacturing Price",
    "Sale Price",
    "Gross Sales",
    "Discounts",
    "Sales",
    "COGS",
    "Profit"
]

for col in numeric_cols:
    s = df[col].astype(str).str.strip()
    s = s.str.replace("$", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    s = s.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    s = s.replace(["-", "", "nan"], pd.NA)
    df[col] = pd.to_numeric(s, errors="coerce")

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

df.to_csv("Dataset/Financials_Cleaned.csv", index=False)

print("CLEANING COMPLETED!")
print("Dataset Shape:", df.shape)
print("\nDATA TYPES:")
print(df.dtypes)
print("\nMISSING VALUES:")
print(df.isnull().sum())
print("\nDUPLICATE ROWS:", df.duplicated().sum())
print("\nNEGATIVE PROFITS:", (df["Profit"] < 0).sum())
print("\nCLEANED FILE SAVED: Dataset/Financials_Cleaned.csv")
