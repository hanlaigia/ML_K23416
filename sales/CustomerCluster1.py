from flask import Flask
from flaskext.mysql import MySQL
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
app = Flask(__name__)

def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        # MySQL configurations
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except mysql.connector.Error as e:
        print("Error = ", e)
        return None
def closeConnection(conn):
    if conn != None:
        conn.close()

def queryDataset(conn, sql):
    cursor = conn.cursor()

    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    return df

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

sql1 = "select * from customer"
df1 = queryDataset(conn, sql1)
print(df1)

sql2 = "select distinct customer.CustomerId, Age, Annual_Income, Spending_Score " \
       "from customer, customer_spend_score " \
       "where customer.CustomerId = customer_spend_score.CustomerID"

df2 = queryDataset(conn, sql2)
df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

print(df2)
print(df2.head())
print(df2.describe())

def showHistogram(df, columns):
    plt.figure(1, figsize=(7, 8))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        sns.distplot(df[column], bins=32)
        plt.title(f'Histogram of {column}')
    plt.show()

showHistogram(df2, df2.columns[1:])

def elbowMethod(df, colunmsForElbow):
    X = df.loc[:, colunmsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(n_clusters=n,
                       init='k-means++',
                       max_iter=500,
                       random_state=42)
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '--', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.show()

columns=['Age', 'Spending Score']
elbowMethod(df2, columns)