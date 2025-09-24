import sqlite3
import pandas as pd

def top_customers_by_spending(db_path, n):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        print('DB Init')

        query = """
        SELECT CustomerId, SUM(Total) AS TotalSpent
        FROM Invoice
        GROUP BY CustomerId
        ORDER BY TotalSpent DESC
        LIMIT ?;
        """
        cursor.execute(query, (n,))

        # Lấy dữ liệu
        rows = cursor.fetchall()

        # Lấy tên cột từ cursor.description
        col_names = [desc[0] for desc in cursor.description]

        # Đưa vào DataFrame
        df = pd.DataFrame(rows, columns=col_names)
        print(df)

        cursor.close()
        return df

    except sqlite3.Error as error:
        print('Error occurred - ', error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('sqlite connection closed')

db_path = '../databases/Chinook_Sqlite.sqlite'
n = int(input("Nhập số khách hàng top n: "))
result = top_customers_by_spending(db_path, n)
