import numpy as np
from sklearn.metrics import ndcg_score
import lightgbm as lgb 

X = np.array([[100,3],[200,5],[150,1],[300,7],[120,2]], dtype=float)
y = np.array([1, 2, 0, 3, 1])  # graded relevance

dtrain = lgb.Dataset(X, label=y, group=[len(y)])
params = {
    "objective": "lambdarank",
    "metric": "ndcg",
    "ndcg_eval_at": [5],
    "learning_rate": 0.1,
    "num_leaves": 15,
    "min_data_in_leaf": 1,
    "verbose": -1,
}
model = lgb.train(params, dtrain, num_boost_round=60)

scores = model.predict(X).reshape(1, -1)
print("Listwise   NDCG@5:", ndcg_score(y.reshape(1,-1), scores, k=5))
print("Thứ hạng (chỉ số tài liệu giảm dần):", np.argsort(-scores[0]))