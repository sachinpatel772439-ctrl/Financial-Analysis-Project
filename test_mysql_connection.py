
import mysql.connector
from getpass import getpass

password = getpass("Enter MySQL root password: ")

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=password,
        database="financial_analysis"
    )

    if connection.is_connected():
        print("SUCCESS! Python connected to MySQL.")

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        print("Database details:", cursor.fetchone())

        cursor.close()
        connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)
