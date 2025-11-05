import random
from random import random
import plotly.graph_objects as go

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QDialog, QComboBox, QPushButton, QCheckBox, \
    QListWidgetItem, QFileDialog
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from MLBAProject.Connectors.Connector import Connector
from MLBAProject.Models.PurchaseLinearRegression import PurchaseLinearRegression
from MLBAProject.Models.PurchaseStatistic import PurchaseStatistic
from MLBAProject.UI.ChartHandle import ChartHandle
from MLBAProject.UI.DatabaseConnectEx import DatabaseConnectEx
from MLBAProject.UI.MainWindow import Ui_MainWindow
import traceback

import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random


class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.purchaseLinearRegression = PurchaseLinearRegression()
        self.databaseConnectEx = DatabaseConnectEx()
        self.databaseConnectEx.parent = self
        self.chartHandle = ChartHandle()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.MainWindow = MainWindow


        self.vboxFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setupPlot()

        self.actionConnection.triggered.connect(self.openDatabaseConnectUI)

        self.pushButtonPurchaseRatesByGender.clicked.connect(self.showPurchaseRatesByGender)
        self.pushButtonSalesFlucuationsByYearAndMonth.clicked.connect(self.showSalesFlucuationsByYearAndMonth)
        self.pushButtonPurchaseCountingByCategory.clicked.connect(self.showPurchaseCountingByCategory)
        self.pushButtonPurchaseRatesByAgeGroup.clicked.connect(self.showPurchaseRatesByAgeGroup)
        self.pushButtonPurchaseCountingByCategory.clicked.connect(self.showPurchaseCountingByCategory)
        self.pushButtonPurchaseValueByCategory.clicked.connect(self.showPurchaseValueByCategory)
        self.pushButtonPurchaseByCategoryAndGender.clicked.connect(self.showPurchaseByCategoryAndGender)
        self.pushButtonPaymentMethod.clicked.connect(self.showPaymentMethod)
        self.pushButtonPurchaseRatesByShoppingMall.clicked.connect(self.showPurchaseRatesByShoppingMall)
        self.pushButtonProductSpendingByGender.clicked.connect(self.showProductSpendingByGender)
        self.pushButtonPurchaseFrequenceByAge.clicked.connect(self.showShowPurchaseFrequenceByAge)
        self.pushButtonSalesFluctuationsByMonth.clicked.connect(self.showpushButtonSalesFluctuationsByMonth)
        self.checkEnableWidget(False)

        self.pushButtonTrainModel.clicked.connect(self.processTrainModel)
        self.pushButtonEvaluate.clicked.connect(self.processEvaluateTrainedModel)
        self.pushButtonSavePath.clicked.connect(self.processPickSavePath)
        self.pushButtonSaveModel.clicked.connect(self.processSaveTrainedModel)
        self.pushButtonLoadModel.clicked.connect(self.processLoadTrainedModel)
        self.pushButtonPredict.clicked.connect(self.processPrediction)

    def show(self):
        self.MainWindow.show()

    def checkEnableWidget(self, flag=True):
        self.pushButtonPurchaseRatesByGender.setEnabled(flag)
        self.pushButtonPurchaseRatesByAgeGroup.setEnabled(flag)
        self.pushButtonPurchaseCountingByCategory.setEnabled(flag)
        self.pushButtonPurchaseValueByCategory.setEnabled(flag)
        self.pushButtonPurchaseByCategoryAndGender.setEnabled(flag)
        self.pushButtonPaymentMethod.setEnabled(flag)
        self.pushButtonPurchaseRatesByShoppingMall.setEnabled(flag)
        self.pushButtonProductSpendingByGender.setEnabled(flag)
        self.pushButtonPurchaseFrequenceByAge.setEnabled(flag)
        self.pushButtonSalesFluctuationsByMonth.setEnabled(flag)
        self.pushButtonSalesFlucuationsByYearAndMonth.setEnabled(flag)

    def setupPlot(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)
        self.verticalLayout_3.addWidget(self.toolbar)
        self.verticalLayout_3.addWidget(self.canvas)

    def openDatabaseConnectUI(self):
        dbwindow = QMainWindow()
        self.databaseConnectEx.setupUi(dbwindow)
        self.databaseConnectEx.show()

    def showDataIntoTableWidget(self, df):
        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setColumnCount(len(df.columns))
        for i in range(len(df.columns)):
            columnHeader = df.columns[i]
            self.tableWidgetStatistic.setHorizontalHeaderItem(i, QTableWidgetItem(columnHeader))
        row = 0
        for item in df.iloc:
            arr = item.values.tolist()
            self.tableWidgetStatistic.insertRow(row)
            j = 0
            for data in arr:
                self.tableWidgetStatistic.setItem(row, j, QTableWidgetItem(str(data)))
                j = j + 1
            row = row + 1

    def showPurchaseCountingByCategory(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        df = self.purchaseLinearRegression.processCategoryDistribution()
        self.showDataIntoTableWidget(df)
        columnLabel = "category"
        columnStatistic = "count"
        title = "Categories Distribution"
        hue = None
        self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, df, columnLabel, columnStatistic, title, hue)

    def showPurchaseRatesByGender(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        self.purchaseLinearRegression.execPurchaseHistory()
        self.purchaseLinearRegression.processGenderDistribution()
        df = self.purchaseLinearRegression.dfGender
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizePieChart(self.figure, self.canvas, df, "gender", "count", "Gender Distribution", True)

    def showSalesFlucuationsByYearAndMonth(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        self.purchaseLinearRegression.execPurchaseHistory()
        self.purchaseLinearRegression.processMonthlyAndYearSalesAmount()
        df = self.purchaseLinearRegression.dfMonthlyAndYearSalesAmount
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, df, "month", "sales_amount",
                                                "Monthly Variation in Sales Amount Over Years", "year", True)

    def showPurchaseRatesByAgeGroup(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        self.purchaseLinearRegression.execPurchaseHistory()
        fromAge = int(self.lineEditFromAge.text())
        toAge = int(self.lineEditToAge.text())
        self.purchaseLinearRegression.processAgeDistribution(fromAge, toAge)
        df = self.purchaseLinearRegression.dfAges
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, df, "age", "count",
                                                f"Age Distribution {fromAge}~{toAge}", None)

    def showPurchaseValueByCategory(self):
        df = self.purchaseLinearRegression.processCategorySpending()
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizeBarChart(self.figure, self.canvas, df, "category", "price",
                                           "Distribution category and Spending")

    def showPurchaseByCategoryAndGender(self):
        df = self.purchaseLinearRegression.processGenderAndCategoryCounter()
        self.showDataIntoTableWidget(df)
        df = self.purchaseLinearRegression.df
        self.chartHandle.visualizeMultiBarChart(self.figure, self.canvas, df, "category", "count", "gender",
                                                "Distribution gender and category")

    def showPaymentMethod(self):
        df = self.purchaseLinearRegression.processPaymentMethod()
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizePieChart(self.figure, self.canvas, df, "payment_method", "count",
                                           "Payment Distribution", False)

    def showPurchaseRatesByShoppingMall(self):
        df = self.purchaseLinearRegression.processShoppingMall()
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizePieChart(self.figure, self.canvas, df, "shopping_mall", "count",
                                           "Shopping Mall Distribution", False)

    def showProductSpendingByGender(self):
        df = self.purchaseLinearRegression.processGenderCategorySpending()
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizeBarPlot(self.figure, self.canvas, df, "category", "price", "gender",
                                          "Male and Female category Total Price Spend")

    def showShowPurchaseFrequenceByAge(self):
        df = self.purchaseLinearRegression.processAgeOrderFrequence()
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizeScatterPlot(self.figure, self.canvas, df, "age", "count",
                                              "Age VS Order Frequence")

    def showpushButtonSalesFluctuationsByMonth(self):
        df = self.purchaseLinearRegression.processMonthlySalesAmount()
        self.showDataIntoTableWidget(df)
        self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, df, "month", "sales_amount",
                                                "Monthly Variation in Sales Amount", None)

    def processTrainModel(self):
        columns_input = ["gender", "age"]
        column_target = "price"
        if self.radioButtonGenderAgePayment.isChecked():
            columns_input = ["gender", "age", "payment_method"]
        test_size = float(self.lineEditTestSize.text()) / 100
        random_state = int(self.lineEditRandomState.text())
        self.purchaseLinearRegression = PurchaseLinearRegression()
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        self.purchaseLinearRegression.processTrain(columns_input, column_target, test_size, random_state)
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Info")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText("Train machine learning model successful!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        dlg.exec()

    def processEvaluateTrainedModel(self):
        result = self.purchaseLinearRegression.evaluate()
        self.lineEditMAE.setText(str(result.MAE))
        self.lineEditMSE.setText(str(result.MSE))
        self.lineEditRMSE.setText(str(result.RMSE))
        self.lineEditR2SCore.setText(str(result.R2_SCORE))

    def processPickSavePath(self):
        filters = "trained model file (*.zip);;All files(*)"
        filename, selected_filter = QFileDialog.getSaveFileName(self.MainWindow, filter=filters)
        self.lineEditPath.setText(filename)

    def processSaveTrainedModel(self):
        trainedModelPath = self.lineEditPath.text()
        if trainedModelPath == "":
            return
        self.purchaseLinearRegression.saveModel(trainedModelPath)
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Info")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText(f"Saved Trained machine learning model successful at [{trainedModelPath}]!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        dlg.exec()

    def processLoadTrainedModel(self):
        filters = "trained model file (*.zip);;All files(*)"
        filename, selected_filter = QFileDialog.getOpenFileName(self.MainWindow, filter=filters)
        if filename == "":
            return
        self.lineEditLocationLoadTrainedModel.setText(filename)
        self.purchaseLinearRegression.loadModel(filename)
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Info")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText(f"Load Trained machine learning model successful from [{filename}]!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes)
        dlg.exec()

    def processPrediction(self):
        gender = self.lineEditGender.text()
        age = int(self.lineEditAge.text())
        payment = self.lineEditPaymentMethod.text()
        if len(self.purchaseLinearRegression.trainedmodel.columns_input) == 3:
            predicted_price = self.purchaseLinearRegression.predictPriceFromGenderAndAgeAndPayment(gender, age, payment)
        else:
            predicted_price = self.purchaseLinearRegression.predictPriceFromGenderAndAge(gender, age)
        self.lineEditPredictedPrice.setText(str(predicted_price[0]))
