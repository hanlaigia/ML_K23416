import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import ndcg_score

# 1 truy vấn, 5 tài liệu, 2 đặc trưng/tài liệu
X = np.array([[100,3],[200,5],[150,1],[300,7],[120,2]], dtype=float)
# Nhãn graded relevance (0–3). Dùng shape (1, n_docs) cho ndcg_score
y_true = np.array([[1, 2, 0, 3, 1]])

model = LinearRegression().fit(X, y_true.ravel())
scores = model.predict(X).reshape(1, -1)

print("Pointwise  NDCG@5:", ndcg_score(y_true, scores, k=5))
print("Thứ hạng (chỉ số tài liệu giảm dần):", np.argsort(-scores[0]))
