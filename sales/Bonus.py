from flask import Flask, render_template_string, request
from flaskext.mysql import MySQL
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import io, base64

app = Flask(__name__)

# ==============================
# KẾT NỐI DATABASE SAKILA
# ==============================
def getConnect():
    try:
        mysql = MySQL()
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        app.config['MYSQL_DATABASE_PORT'] = 3306
        app.config['MYSQL_DATABASE_DB'] = 'sakila'
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = '@Obama123'
        mysql.init_app(app)
        conn = mysql.connect()
        return conn
    except Exception as e:
        print("Lỗi kết nối:", e)
        return None


def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    return df


conn = getConnect()

# =====================================================================
# (1) KHÁCH HÀNG THEO TỪNG PHIM
# =====================================================================
def customers_by_film(conn):
    sql = """
        SELECT 
            f.film_id,
            f.title AS film_title,
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        ORDER BY f.title, customer_name;
    """
    df = queryDataset(conn, sql)
    return df


# =====================================================================
# (2) KHÁCH HÀNG THEO CATEGORY (CẬP NHẬT CHUẨN)
# =====================================================================
def customers_by_category(conn):
    sql = """
        SELECT DISTINCT
            cat.category_id,
            cat.name AS category_name,
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email
        FROM category cat
        JOIN film_category fc ON fc.category_id = cat.category_id
        JOIN film f ON f.film_id = fc.film_id
        JOIN inventory i ON i.film_id = f.film_id
        JOIN rental r ON r.inventory_id = i.inventory_id
        JOIN customer c ON c.customer_id = r.customer_id
        ORDER BY cat.category_id, c.customer_id;
    """
    df = queryDataset(conn, sql)
    return df


# =====================================================================
# (3) GOM CỤM KHÁCH HÀNG K-MEANS
# =====================================================================
def customer_interest_clusters(conn, k=4):
    sql = """
        SELECT 
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
            COUNT(r.rental_id) AS total_rentals,
            COUNT(DISTINCT i.film_id) AS unique_films,
            COUNT(DISTINCT r.inventory_id) AS unique_inventory_cnt
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        GROUP BY c.customer_id, c.first_name, c.last_name;
    """
    df = queryDataset(conn, sql)

    X = df[['total_rentals', 'unique_films', 'unique_inventory_cnt']]
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['cluster'] = model.fit_predict(X)

    plt.figure(figsize=(5, 4))
    plt.scatter(df['total_rentals'], df['unique_films'], c=df['cluster'])
    plt.xlabel("Total Rentals")
    plt.ylabel("Unique Films")
    plt.title("Customer Clustering (K-Means)")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return df, img_base64


# =====================================================================
# GIAO DIỆN WEB
# =====================================================================
@app.route("/", methods=["GET", "POST"])
def index():
    html = """
    <html>
    <head>
        <title>Phân tích khách hàng Sakila</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <h2 class="text-center mb-4 fw-bold">Phân tích khách hàng (CSDL Sakila)</h2>

        <form method="post" class="text-center mb-4">
            <label class="mx-2 fw-semibold">Chọn chức năng:</label>
            <select name="task" class="form-select d-inline-block w-auto">
                <option value="1" {% if task == '1' %}selected{% endif %}>Khách hàng theo từng phim (bài 1)</option>
                <option value="2" {% if task == '2' %}selected{% endif %}>Khách hàng theo từng category (bài 2)</option>
                <option value="3" {% if task == '3' %}selected{% endif %}>Gom cụm K-Means mức độ quan tâm (bài 3)</option>
            </select>

            <label class="mx-2 fw-semibold">K (cho bài 3):</label>
            <input class="form-control d-inline-block w-auto" type="number" name="k" value="{{ k_val }}" min="2" max="10"/>

            <button type="submit" class="btn btn-primary mx-2">Thực hiện</button>
        </form>

        {% if task == '3' and clusters %}
            <div class="text-center mb-3">
                <h5 class="fw-bold text-success mb-3">Chọn cụm để xem chi tiết:</h5>
                {% for c_id in clusters.keys() %}
                    <form method="post" class="d-inline">
                        <input type="hidden" name="task" value="3">
                        <input type="hidden" name="k" value="{{ k_val }}">
                        <input type="hidden" name="filter_cluster" value="{{ c_id }}">
                        <button type="submit" class="btn btn-outline-primary btn-sm mx-1">Cụm {{ c_id }}</button>
                    </form>
                {% endfor %}
            </div>
        {% endif %}

        {% if img %}
            <div class="text-center mt-4">
                <img src="data:image/png;base64,{{ img }}" class="img-fluid border rounded mb-4">
            </div>
        {% endif %}

        {% if table %}
            <div class="container mt-4">
                {{ table|safe }}
            </div>
        {% endif %}
    </body>
    </html>
    """

    k_val = 4
    task = None
    table_html = None
    img64 = None
    clusters = None

    if request.method == "POST":
        task = request.form.get("task")
        k_val = int(request.form.get("k", 4))

        if task == "1":
            df = customers_by_film(conn)
            table_html = df.head(100).to_html(classes="table table-bordered table-sm", index=False)

        elif task == "2":
            df = customers_by_category(conn)
            table_html = df.to_html(classes="table table-bordered table-sm", index=False)

        elif task == "3":
            df, img64 = customer_interest_clusters(conn, k_val)
            clusters = {cid: grp for cid, grp in df.groupby("cluster")}
            filter_cluster = request.form.get("filter_cluster")
            if filter_cluster is not None and int(filter_cluster) in clusters:
                df_show = clusters[int(filter_cluster)]
            else:
                df_show = df
            table_html = df_show.head(100).to_html(classes="table table-bordered table-sm", index=False)

    return render_template_string(html, table=table_html, img=img64, task=task, clusters=clusters, k_val=k_val)


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("===============================================")
    print("PHÂN TÍCH KHÁCH HÀNG TỪ CSDL SAKILA")
    print("Thực hiện 3 yêu cầu trong đề bài:")
    print(" (1) Liệt kê khách hàng theo từng phim họ đã thuê")
    print(" (2) Liệt kê khách hàng theo từng category (cập nhật có email, DISTINCT)")
    print(" (3) Gom cụm khách hàng bằng K-Means theo mức độ quan tâm, có nút lọc cụm")
    print("===============================================\n")
    app.run()
