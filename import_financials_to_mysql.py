
import pandas as pd
import mysql.connector
from getpass import getpass

# Read cleaned dataset
df = pd.read_csv("Dataset/Financials_Analysis_Ready.csv")

# Match CSV column names with MySQL table columns
df.rename(columns={
    "Discount Band": "Discount_Band",
    "Units Sold": "Units_Sold",
    "Manufacturing Price": "Manufacturing_Price",
    "Sale Price": "Sale_Price",
    "Gross Sales": "Gross_Sales",
    "Month Number": "Month_Number",
    "Month Name": "Month_Name"
}, inplace=True)

columns = [
    "Segment", "Country", "Product", "Discount_Band",
    "Units_Sold", "Manufacturing_Price", "Sale_Price",
    "Gross_Sales", "Discounts", "Sales", "COGS",
    "Profit", "Date", "Month_Number", "Month_Name", "Year"
]

df = df[columns]

# Convert dates
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert missing values to SQL NULL
def convert_value(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date()
    if hasattr(value, "item"):
        return value.item()
    return value

records = [
    tuple(convert_value(value) for value in row)
    for row in df.itertuples(index=False, name=None)
]

password = getpass("Enter MySQL root password: ")

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=password,
        database="financial_analysis"
    )

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM financial_data")
    existing_rows = cursor.fetchone()[0]

    if existing_rows > 0:
        print("Table already contains data:", existing_rows)
        print("Import stopped to avoid duplicate records.")

    else:
        query = """
        INSERT INTO financial_data (
            Segment, Country, Product, Discount_Band,
            Units_Sold, Manufacturing_Price, Sale_Price,
            Gross_Sales, Discounts, Sales, COGS,
            Profit, Date, Month_Number, Month_Name, Year
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        """

        cursor.executemany(query, records)
        connection.commit()

        print("SUCCESS! CSV data imported into MySQL.")
        print("Total rows imported:", cursor.rowcount)

except mysql.connector.Error as error:
    if connection and connection.is_connected():
        connection.rollback()
    print("Import failed:", error)

finally:
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
