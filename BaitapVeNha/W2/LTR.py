import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
data = pd.DataFrame({
    "query": ["Q1"]*3 + ["Q2"]*3,
    "doc": ["D1","D2","D3","D1","D2","D3"],
    "feature1": [0.1,0.4,0.9,0.2,0.7,0.8],
    "feature2": [0.2,0.8,0.3,0.1,0.6,0.9],
    "label": [0,1,2,0,2,1]   # 0 = không liên quan, 2 = liên quan cao
})
# print(data)
# X, y = data[["feature1","feature2"]], data["label"]
# model_point = LinearRegression().fit(X,y)
# preds_point = model_point.predict(X)
# print("Predictions:", preds_point.round(2).tolist())
# print("MSE:", mean_squared_error(y,preds_point))

#
# import itertools, numpy as np
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
#
# pairs, labels = [], []
# for q in data["query"].unique():
#     docs = data[data["query"]==q]
#     for (_, di), (_, dj) in itertools.combinations(docs.iterrows(),2):
#         diff = di[["feature1","feature2"]].values - dj[["feature1","feature2"]].values
#         label = 1 if di["label"]>dj["label"] else 0
#         pairs.append(diff); labels.append(label)
#
# X_pairs, y_pairs = np.array(pairs), np.array(labels)
# model_pair = LogisticRegression().fit(X_pairs,y_pairs)
# preds_pair = model_pair.predict(X_pairs)
# print("True labels:", y_pairs.tolist())
# print("Predictions:", preds_pair.tolist())
# print("Accuracy:", accuracy_score(y_pairs,preds_pair))


import torch, torch.nn as nn, torch.optim as optim
groups=[]
for q in data["query"].unique():
    docs=data[data["query"]==q]
    Xg=torch.tensor(docs[["feature1","feature2"]].values,dtype=torch.float32)
    yg=torch.tensor(docs["label"].values,dtype=torch.float32)
    yg=yg/yg.sum()
    groups.append((Xg,yg))

model_list=nn.Linear(2,1)
criterion=nn.KLDivLoss(reduction="batchmean")
opt=optim.Adam(model_list.parameters(),lr=0.1)

for epoch in range(50):
    total_loss=0
    for Xg,yg in groups:
        opt.zero_grad()
        scores=model_list(Xg).squeeze()
        probs=torch.softmax(scores,dim=0)
        loss=criterion(torch.log(probs),yg)
        loss.backward(); opt.step()
        total_loss+=loss.item()
    if epoch%10==0:
        print(f"Epoch {epoch}, Loss {total_loss:.4f}")

with torch.no_grad():
    for i,(Xg,yg) in enumerate(groups):
        scores=model_list(Xg).squeeze()
        probs=torch.softmax(scores,dim=0)
        print(f"Query {i+1}: predicted {probs.numpy()}, true {yg.numpy()}")











# === Dataset ===
#   query doc  feature1  feature2  label
# 0    Q1  D1       0.1       0.2      0
# 1    Q1  D2       0.4       0.8      1
# 2    Q1  D3       0.9       0.3      2
# 3    Q2  D1       0.2       0.1      0
# 4    Q2  D2       0.7       0.6      2
# 5    Q2  D3       0.8       0.9      1
#
# === Pointwise ===
# Predictions: [0.02, 0.68, 1.95, 0.27, 1.43, 1.64]
# MSE: 0.15220638652169657
#
# === Pairwise ===
# True labels (pairwise): [0, 0, 0, 0, 0, 1]
# Predictions: [0, 0, 0, 0, 0, 0]
# Accuracy: 0.8333333333333334
# Epoch 0, Loss 0.4062
# Epoch 10, Loss 0.1415
# Epoch 20, Loss 0.1083
# Epoch 30, Loss 0.1049
# Epoch 40, Loss 0.1050
#
# === Listwise ===
# Query 1: predicted distribution [0.05913439 0.23652029 0.7043453 ], true distribution [0.         0.33333334 0.6666667 ]
# Query 2: predicted distribution [0.05189361 0.3483426  0.59976375], true distribution [0.         0.6666667  0.33333334]
#
# Process finished with exit code 0











# # ==============================
# # Learning to Rank: Pointwise, Pairwise, Listwise
# # ==============================
#
# import pandas as pd
# import itertools
# import numpy as np
# from sklearn.linear_model import LinearRegression, LogisticRegression
# from sklearn.metrics import mean_squared_error, accuracy_score
# import torch
# import torch.nn as nn
# import torch.optim as optim
#
# # ------------------------------
# # 1. Dataset giả lập
# # ------------------------------
# data = pd.DataFrame({
#     "query": ["Q1"]*3 + ["Q2"]*3,
#     "doc": ["D1","D2","D3","D1","D2","D3"],
#     "feature1": [0.1,0.4,0.9,0.2,0.7,0.8],
#     "feature2": [0.2,0.8,0.3,0.1,0.6,0.9],
#     "label": [0,1,2,0,2,1]   # mức độ liên quan: 0 = không, 1 = trung bình, 2 = cao
# })
#
# print("=== Dataset ===")
# print(data)
#
# # ------------------------------
# # 2. Pointwise Approach
# # ------------------------------
# X, y = data[["feature1","feature2"]], data["label"]
#
# model_point = LinearRegression().fit(X,y)
# preds_point = model_point.predict(X)
# mse_point = mean_squared_error(y,preds_point)
#
# print("\n=== Pointwise ===")
# print("Predictions:", preds_point.round(2).tolist())
# print("MSE:", mse_point)
#
# # ------------------------------
# # 3. Pairwise Approach
# # ------------------------------
# pairs, labels = [], []
# for q in data["query"].unique():
#     docs = data[data["query"]==q]
#     for (_, di), (_, dj) in itertools.combinations(docs.iterrows(),2):
#         diff = di[["feature1","feature2"]].values - dj[["feature1","feature2"]].values
#         label = 1 if di["label"]>dj["label"] else 0
#         pairs.append(diff); labels.append(label)
#
# X_pairs, y_pairs = np.array(pairs), np.array(labels)
#
# model_pair = LogisticRegression().fit(X_pairs,y_pairs)
# preds_pair = model_pair.predict(X_pairs)
# acc_pair = accuracy_score(y_pairs,preds_pair)
#
# print("\n=== Pairwise ===")
# print("True labels (pairwise):", y_pairs.tolist())
# print("Predictions:", preds_pair.tolist())
# print("Accuracy:", acc_pair)
#
# # ------------------------------
# # 4. Listwise Approach (ListNet demo)
# # ------------------------------
# groups=[]
# for q in data["query"].unique():
#     docs=data[data["query"]==q]
#     Xg=torch.tensor(docs[["feature1","feature2"]].values,dtype=torch.float32)
#     yg=torch.tensor(docs["label"].values,dtype=torch.float32)
#     yg=yg/yg.sum()   # normalize thành phân phối
#     groups.append((Xg,yg))
#
# model_list=nn.Linear(2,1)
# criterion=nn.KLDivLoss(reduction="batchmean")
# opt=optim.Adam(model_list.parameters(),lr=0.1)
#
# for epoch in range(50):
#     total_loss=0
#     for Xg,yg in groups:
#         opt.zero_grad()
#         scores=model_list(Xg).squeeze()
#         probs=torch.softmax(scores,dim=0)
#         loss=criterion(torch.log(probs),yg)
#         loss.backward(); opt.step()
#         total_loss+=loss.item()
#     if epoch%10==0:
#         print(f"Epoch {epoch}, Loss {total_loss:.4f}")
#
# print("\n=== Listwise ===")
# with torch.no_grad():
#     for i,(Xg,yg) in enumerate(groups):
#         scores=model_list(Xg).squeeze()
#         probs=torch.softmax(scores,dim=0)
#         print(f"Query {i+1}: predicted distribution {probs.numpy()}, true distribution {yg.numpy()}")
