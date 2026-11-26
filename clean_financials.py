import pandas as pd

# Load original dataset
df = pd.read_csv("Dataset/archive/Financials.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Financial columns
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

# Convert currency text into numeric values
for col in numeric_cols:
    s = df[col].astype(str).str.strip()
    s = s.str.replace("$", "", regex=False)
    s = s.str.replace(",", "", regex=False)
    s = s.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
    s = s.replace(["-", "", "nan"], pd.NA)
    df[col] = pd.to_numeric(s, errors="coerce")

# Convert dates (US format: MM/DD/YYYY)
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

# Save cleaned dataset
df.to_csv("Dataset/Financials_Cleaned.csv", index=False)

# Cleaning report
print("CLEANING COMPLETED!")
print("Dataset Shape:", df.shape)
print("\nDATA TYPES:")
print(df.dtypes)
print("\nMISSING VALUES:")
print(df.isnull().sum())
print("\nDUPLICATE ROWS:", df.duplicated().sum())
print("\nNEGATIVE PROFITS:", (df["Profit"] < 0).sum())
print("\nCLEANED FILE SAVED: Dataset/Financials_Cleaned.csv")
