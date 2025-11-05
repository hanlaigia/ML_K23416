import pandas as pd
from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

from MLBAProject.Models.MetricsResult import MetricsResult
from MLBAProject.Models.PurchaseMLModel import PurchaseMLModel
from MLBAProject.Models.TrainedModel import TrainedModel
from MLBAProject.Utils.FileUtils import FileUtil

import numpy as np
from types import SimpleNamespace
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

class PurchaseLinearRegression(PurchaseMLModel):
    def __init__(self, connector=None):
        super().__init__(connector)
        self.le = LabelEncoder()
        self.sc_std = StandardScaler()

    def processTrain(self, columns_input, column_target, test_size, random_state):
        self.execPurchaseHistory()
        self.processTransform()
        print(self.dfTransform.columns)
        print(self.dfTransform.iloc[0])

        y = self.dfTransform[column_target]
        X = self.dfTransform[columns_input]
        print("X=", X)
        print("y=", y)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        self.trainedmodel = TrainedModel()
        self.trainedmodel.X_train = self.X_train
        self.trainedmodel.X_test = self.X_test
        self.trainedmodel.y_train = self.y_train
        self.trainedmodel.y_test = self.y_test
        self.trainedmodel.columns_input = columns_input
        self.trainedmodel.column_target = column_target

        self.X_train = self.sc_std.fit_transform(self.X_train)
        self.X_test = self.sc_std.transform(self.X_test)

        self.lr = LinearRegression()
        self.model = self.lr.fit(self.X_train, self.y_train)

        # giữ lại code cũ
        self.trainedmodel.model = self.model

        # dùng estimator thống nhất (không dùng lambda để tránh lỗi pickle)
        self.trainedmodel.estimator = self.model

    def visualizeActualAndPredictResult(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.lr.predict(self.X_train), self.y_train)
        plt.xlabel('Predicted value of Y')
        plt.ylabel('Real value of Y')
        plt.show()

    def evaluate(self):
        pred = self.trainedmodel.predict(self.X_test)

        mae = mean_absolute_error(self.y_test, pred)
        mse = mean_squared_error(self.y_test, pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, pred)

        return SimpleNamespace(MAE=mae, MSE=mse, RMSE=rmse, R2_SCORE=r2)

    def predictPriceFromGenderAndAge(self, gender, age):
        data_gender = {'gender': ["Male", "Female"]}
        df_gender = pd.DataFrame(data=data_gender)
        df_gender_transform = self.le.fit_transform(df_gender)

        col_gender = 0 if gender == 'Male' else 1
        data = [[df_gender_transform[col_gender], age]]

        input_transform = self.sc_std.transform(data)
        pred = self.predict(input_transform)
        return pred

    def predictPriceFromGenderAndAgeAndPayment(self, gender, age, payment_method):
        data_gender = {'gender': ["Male", "Female"]}
        df_gender = pd.DataFrame(data=data_gender)
        df_gender_transform = self.le.fit_transform(df_gender)

        data_payment_method = {"payment_method": ["Credit Card", "Debit Card", "Cash"]}
        df_payment_method = pd.DataFrame(data=data_payment_method)
        df_payment_method_transform = self.le.fit_transform(df_payment_method)

        col_gender = 0 if gender == 'Male' else 1

        if payment_method == "Credit Card":
            col_payment = 0
        elif payment_method == "Debit Card":
            col_payment = 1
        else:
            col_payment = 2

        data = [[df_gender_transform[col_gender], age, df_payment_method_transform[col_payment]]]

        input_transform = self.sc_std.transform(data)
        pred = self.predict(input_transform)
        return pred

    def predict(self, columns_input):
        if hasattr(self, "trainedmodel") and self.trainedmodel is not None:
            if hasattr(self.trainedmodel, "predict"):
                return self.trainedmodel.predict(columns_input)
            if hasattr(self.trainedmodel, "estimator"):
                return self.trainedmodel.estimator.predict(columns_input)
        pred = self.model.predict(columns_input)
        return pred

    def saveModel(self, fileName):
        ret = FileUtil.saveModel(self.trainedmodel, fileName)
        return ret

    def loadModel(self, fileName):
        self.trainedmodel = FileUtil.loadModel(fileName)
        if self.trainedmodel is None:
            return None

        if hasattr(self.trainedmodel, "X_train") and self.trainedmodel.X_train is not None:
            self.sc_std.fit_transform(self.trainedmodel.X_train)

        self.model = getattr(self.trainedmodel, "estimator", None) or getattr(self.trainedmodel, "model", None)
        if self.model is not None and not hasattr(self.trainedmodel, "estimator"):
            self.trainedmodel.estimator = self.model
        return self.model
