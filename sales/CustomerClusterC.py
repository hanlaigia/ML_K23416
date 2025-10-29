from flask import Flask, request, render_template_string
from flaskext.mysql import MySQL
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import sys, time

app = Flask(__name__)

# ==============================
# KẾT NỐI MYSQL
# ==============================
def getConnect(server, port, database, username, password):
    try:
        mysql = MySQL()
        app.config['MYSQL_DATABASE_HOST'] = server
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = database
        app.config['MYSQL_DATABASE_USER'] = username
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except Exception as e:
        print("Error =", e)
        return None

# LẤY CẢ TÊN CỘT TỪ MYSQL
def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    return df

conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

# ==============================
# LẤY DỮ LIỆU BAN ĐẦU
# ==============================
sql2 = """SELECT DISTINCT customer.CustomerId, Age, Annual_Income, Spending_Score
          FROM customer, customer_spend_score
          WHERE customer.CustomerId = customer_spend_score.CustomerID"""
df2 = queryDataset(conn, sql2)
df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

# ==============================
# HÀM HỖ TRỢ CLUSTER
# ==============================
def runKMeans(df, columns, cluster):
    X = df.loc[:, columns].values
    model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
    model.fit(X)
    df["cluster"] = model.labels_
    return df, model.cluster_centers_

# ==============================
# HIỂN THỊ KHÁCH HÀNG TRÊN CONSOLE
# ==============================
def showCustomersByClusterConsole(conn, df2, clusterCount):
    print(f"\n===================== K = {clusterCount} =====================")
    for c in range(clusterCount):
        print(f"\n===== CLUSTER {c} =====")
        customer_ids = df2[df2["cluster"] == c]["CustomerId"].tolist()
        if not customer_ids:
            print("Không có khách hàng trong cụm này.")
            continue
        id_list = ",".join(map(str, customer_ids))
        sql = f"SELECT * FROM customer WHERE CustomerId IN ({id_list});"
        df = queryDataset(conn, sql)
        print(df.to_string(index=False))
        sys.stdout.flush()
        time.sleep(0.2)

# ==============================
# CHẠY CLUSTER TRÊN CONSOLE KHI KHỞI ĐỘNG
# ==============================
def showAllClustersAtStartup():
    columns = ['Age', 'Annual Income', 'Spending Score']
    for k in [4, 5, 6]:
        df_clustered, _ = runKMeans(df2.copy(), columns, k)
        showCustomersByClusterConsole(conn, df_clustered, k)
        print("\n-------------------------------------------------------------")
        time.sleep(1)

# ==============================
# GIAO DIỆN WEB FLASK
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():
    html_form = """
    <html>
    <head>
        <title>Customer Clustering</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <h2 class="mb-4 text-center text-primary fw-bold">
            Phân cụm khách hàng (K-Means)
        </h2>

        <form method="post" class="text-center mb-4">
            <label for="k" class="fw-semibold">Chọn số cụm (K):</label>
            <select name="k" class="form-select d-inline-block w-auto mx-2 text-center">
                <option value="4" {% if k == 4 %}selected{% endif %}>4</option>
                <option value="5" {% if k == 5 %}selected{% endif %}>5</option>
                <option value="6" {% if k == 6 %}selected{% endif %}>6</option>
            </select>
            <button type="submit" class="btn btn-primary">Gom cụm</button>
        </form>

        {% if clusters %}
            <hr/>
            <h4 class="text-center text-success">K = {{k}} - Danh sách cụm khách hàng</h4>
            {% for i, table in clusters.items() %}
                <h5 class="mt-4 text-primary">Cụm {{i}}</h5>
                <div class="table-responsive">{{table|safe}}</div>
            {% endfor %}
        {% endif %}
    </body>
    </html>
    """

    if request.method == "POST":
        k = int(request.form.get("k"))
        print(f"\n>>> GOM CỤM K = {k}")
        columns = ['Age', 'Annual Income', 'Spending Score']
        df_clustered, _ = runKMeans(df2.copy(), columns, k)

        clusters_html = {}
        for i in range(k):
            ids = df_clustered[df_clustered["cluster"] == i]["CustomerId"].tolist()
            if not ids:
                clusters_html[i] = "<p>Không có khách hàng nào trong cụm này.</p>"
                continue
            id_list = ",".join(map(str, ids))
            sql = f"SELECT * FROM customer WHERE CustomerId IN ({id_list});"
            df_cluster = queryDataset(conn, sql)
            clusters_html[i] = df_cluster.to_html(
                classes="table table-striped table-sm table-bordered align-middle text-center",
                index=False
            )

        return render_template_string(html_form, clusters=clusters_html, k=k)
    else:
        return render_template_string(html_form, clusters=None, k=None)

# ==============================
# CHẠY SERVER
# ==============================
if __name__ == "__main__":
    showAllClustersAtStartup()
    app.run()

