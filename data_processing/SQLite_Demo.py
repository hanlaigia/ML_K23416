# import sqlite3
# import pandas as pd
# try:
#     sqliteConnection = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
#     cursor = sqliteConnection.cursor()
#     print('DB Init')
#
#     query='SELECT * FROM InvoiceLine LIMIT 5;'
#     cursor.execute(query)
#
#     df=pd.DataFrame(cursor.fetchall())
#     print(df)
#
#     cursor.close()
#
# except sqlite3.Error as error:
#     print('Eror occured - ', error)
# finally:
#     if sqliteConnection:
#         sqliteConnection.close()
#         print('sqlite connection closed')

import sqlite3
import pandas as pd

try:
    sqliteConnection = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print('DB Init')

    query = 'SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute(query)

    # Lấy dữ liệu
    rows = cursor.fetchall()

    # Lấy tên cột từ cursor.description
    col_names = [desc[0] for desc in cursor.description]

    # Đưa vào DataFrame với cột
    df = pd.DataFrame(rows, columns=col_names)
    print(df)

    cursor.close()

except sqlite3.Error as error:
    print('Error occurred - ', error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('sqlite connection closed')
