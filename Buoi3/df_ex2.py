import pandas as pd

def find_orders_within_range(df, minValue, maxValue, SortType=True):
    # tổng giá trị từng đơn hàng
    order_totals = df.groupby('OrderID').apply(lambda x: (x['UnitPrice'] * x['Quantity'] * (1 - x['Discount'])).sum())

    # lọc đơn hàng trong range
    orders_within_range = order_totals[(order_totals >= minValue) & (order_totals <= maxValue)]

    # sắp xếp theo SortType
    orders_sorted = orders_within_range.sort_values(ascending=SortType)

    # trả về danh sách OrderID + Tổng giá trị
    result = list(zip(orders_sorted.index.tolist(), orders_sorted.values.tolist()))
    return result

df = pd.read_csv('../datasets/SalesTransactions/SalesTransactions.csv')

minValue = float(input("Nhập giá trị min: "))
maxValue = float(input("Nhập giá trị max: "))
sortType = input("Sắp xếp tăng dần? (y/n): ").lower() == 'y'

result = find_orders_within_range(df, minValue, maxValue, SortType=sortType)
print('Danh sách các hóa đơn trong phạm vi giá trị từ', minValue, 'đến', maxValue, 'là', result)
