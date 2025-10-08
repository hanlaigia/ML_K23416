import traceback

import mysql.connector

from retail_project.models.customer import Customer

server="localhost"
port=3306
database="k23416_retail"
username="root"
password="@Obama123"

try:
    conn = mysql.connector.connect(
                    host=server,
                    port=port,
                    database=database,
                    user=username,
                    password=password)
except:
    traceback.print_exc()

def login_customer(email,pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM customer "\
           "where Email='"+email+"' and Password='"+pwd +"'"
    cust=None
    cursor.execute(sql)
    dataset = cursor.fetchone()
    if dataset!=None:
        cust=Customer(dataset[0],dataset[1],dataset[2],dataset[3],dataset[4], dataset[5])
        # print("ID==", dataset[0])
        # cust.ID, cust.Name, cust.Phone, cust.Email, cust.Password, cust.IsDeleted=dataset
    return cust
    cursor.close()
cust =login_customer("daodao@gmail.com","123")
if cust==None:
    print('Login Failed')
else:
    print('Login Succeeded')
    print(cust)

