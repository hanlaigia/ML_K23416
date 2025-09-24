from numpy import nan as NA
import pandas as pd

data = pd.DataFrame([
    [1., 6.5, 3.],
    [1., NA, NA],
    [NA, NA, NA],
    [NA, 6.5, 3.]
])

print(data)
print("-" * 10)
cleaned = data.dropna()   #chứa ít nhất một giá trị NaN
print(cleaned)
print("-" * 10)
cleaned2 = data.dropna(how='all')       #tất cả giá trị đều NaN
print(cleaned2)


#bài tập: loại bỏ dl số âm khỏi datasets

