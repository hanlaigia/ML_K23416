import pandas as pd

def top_3_products_by_sales(df):
    df['SalesValue'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    product_totals = df.groupby('ProductID')['SalesValue'].sum()

    top_products = product_totals.sort_values(ascending=False).head(3)

    return top_products.to_dict()

df = pd.read_csv('../datasets/SalesTransactions/SalesTransactions.csv')

result = top_3_products_by_sales(df)
print("Top 3 sản phẩm bán chạy nhất là:")
for product, value in result.items():
    print(f" - Sản phẩm {product}: {value:.2f}")
