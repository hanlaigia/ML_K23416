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


# Hàm hỗ trợ query
def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    return df


conn = getConnect()

# =====================================================================
# (1) PHÂN LOẠI KHÁCH HÀNG THEO TÊN PHIM
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

    print("\n================= (1) KHÁCH HÀNG THEO TỪNG PHIM =================")
    for film_title, group in df.groupby("film_title"):
        print(f"\n--- PHIM: {film_title} ---")
        for _, row in group.iterrows():
            print(f"CustomerID {row['customer_id']} - {row['customer_name']}")

    return df


# =====================================================================
# (2) PHÂN LOẠI KHÁCH HÀNG THEO CATEGORY
# =====================================================================
def customers_by_category(conn):
    sql = """
        SELECT DISTINCT
            cat.category_id,
            cat.name AS category_name,
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name
        FROM customer c
        JOIN rental r ON c.customer_id = r.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        ORDER BY cat.name, customer_name;
    """
    df = queryDataset(conn, sql)

    print("\n================= (2) KHÁCH HÀNG THEO TỪNG CATEGORY =================")
    for category_name, group in df.groupby("category_name"):
        print(f"\n--- CATEGORY: {category_name} ---")
        for _, row in group.iterrows():
            print(f"CustomerID {row['customer_id']} - {row['customer_name']}")

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
    model = KMeans(n_clusters=k, random_state=42)
    df['cluster'] = model.fit_predict(X)

    print("\n================= (3) K-MEANS CLUSTERING KHÁCH HÀNG =================")
    print(f"Số cụm k = {k}")
    for c_id, group in df.groupby("cluster"):
        print(f"\n--- CỤM {c_id} ---")
        for _, row in group.iterrows():
            print(
                f"{row['customer_id']:>3} | {row['customer_name']:<20} | "
                f"rentals={row['total_rentals']}, films={row['unique_films']}, invs={row['unique_inventory_cnt']}"
            )

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
                <option value="1">Khách hàng theo từng phim (bài 1)</option>
                <option value="2">Khách hàng theo từng category (bài 2)</option>
                <option value="3">Gom cụm K-Means mức độ quan tâm (bài 3)</option>
            </select>

            <label class="mx-2 fw-semibold">K (cho bài 3):</label>
            <input class="form-control d-inline-block w-auto" type="number" name="k" value="4" min="2" max="10"/>

            <button type="submit" class="btn btn-primary mx-2">Thực hiện</button>
        </form>

        {% if table %}
            <div class="container mt-4">
                {{ table|safe }}
            </div>
        {% endif %}

        {% if img %}
            <div class="text-center mt-4">
                <img src="data:image/png;base64,{{ img }}" class="img-fluid border rounded">
            </div>
        {% endif %}
    </body>
    </html>
    """

    if request.method == "POST":
        task = request.form.get("task")

        if task == "1":
            df = customers_by_film(conn)
            table_html = df.head(100).to_html(classes="table table-bordered table-sm", index=False)
            return render_template_string(html, table=table_html)

        elif task == "2":
            df = customers_by_category(conn)
            table_html = df.head(100).to_html(classes="table table-bordered table-sm", index=False)
            return render_template_string(html, table=table_html)

        elif task == "3":
            k_raw = request.form.get("k")
            try:
                k_val = int(k_raw)
            except:
                k_val = 4
            df, img64 = customer_interest_clusters(conn, k=k_val)
            table_html = df.head(100).to_html(classes="table table-bordered table-sm", index=False)
            return render_template_string(html, table=table_html, img=img64)

    return render_template_string(html)


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("===============================================")
    print("PHÂN TÍCH KHÁCH HÀNG TỪ CSDL SAKILA")
    print("Thực hiện 3 yêu cầu trong đề bài:")
    print(" (1) Liệt kê khách hàng theo từng phim họ đã thuê")
    print(" (2) Liệt kê khách hàng theo từng category, bỏ trùng lặp")
    print(" (3) Gom cụm khách hàng bằng K-Means theo mức độ quan tâm")
    print("===============================================\n")

    # Hiển thị kết quả trên console trước
    df_film = customers_by_film(conn)
    df_cat = customers_by_category(conn)
    df_clustered, _img = customer_interest_clusters(conn, k=4)

    # Sau đó mở web để xem lại kết quả
    app.run()
