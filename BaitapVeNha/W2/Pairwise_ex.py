import numpy as np
from itertools import combinations
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ndcg_score

X = np.array([[100,3],[200,5],[150,1],[300,7],[120,2]], dtype=float)
y = np.array([1, 2, 0, 3, 1])  # graded relevance 1D

# Tạo cặp (i, j); label=1 nếu y[i] > y[j], ngược lại 0
X_pair, y_pair = [], []
for i, j in combinations(range(len(X)), 2):
    X_pair.append(X[i] - X[j])              # đặc trưng hiệu
    y_pair.append(1 if y[i] > y[j] else 0)  # ai "đáng" cao hơn

clf = LogisticRegression().fit(np.vstack(X_pair), np.array(y_pair))
# Suy diễn điểm đơn lẻ: s(d) ≈ w^T x với w là trọng số của logistic
w = clf.coef_.ravel()
scores = (X @ w).reshape(1, -1)

print("Pairwise   NDCG@5:", ndcg_score(y.reshape(1,-1), scores, k=5))
print("Thứ hạng (chỉ số tài liệu giảm dần):", np.argsort(-scores[0]))
