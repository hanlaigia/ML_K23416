class TrainedModel:
    def __init__(
        self,
        estimator=None,
        columns_input=None,
        column_target=None,
        X_train=None,
        X_test=None,
        y_train=None,
        y_test=None,
    ):
        self.estimator = estimator
        self.columns_input = columns_input or []
        self.column_target = column_target
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def predict(self, X):
        return self.estimator.predict(X)
