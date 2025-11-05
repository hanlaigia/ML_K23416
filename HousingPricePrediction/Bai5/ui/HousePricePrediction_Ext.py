from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from ui.HousePricePrediction import Ui_MainWindow
from FileUtil import FileUtil
import os


class HousePricePredictionExt(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = None
        self.setWindowTitle("House Price Prediction")

        # Gán sự kiện
        self.pushButtonLoadModel.clicked.connect(self.load_model)
        self.pushButtonPredict.clicked.connect(self.predict_price)
        self.pushButtonClear.clicked.connect(self.clear_fields)
        self.pushButtonExit.clicked.connect(self.close)

    def load_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Model File", "", "Model Files (*.zip *.pkl)"
        )
        if file_path:
            try:
                self.model = FileUtil.loadmodel(file_path)
                QMessageBox.information(
                    self, "Success",
                    f"Model loaded successfully:\n{os.path.basename(file_path)}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Warning", "No model selected!")

    def predict_price(self):
        if self.model is None:
            QMessageBox.warning(self, "Warning", "Please load model first!")
            return

        try:
            X = [[
                float(self.lineEditIncome.text()),
                float(self.lineEditHouseAge.text()),
                float(self.lineEditRooms.text()),
                float(self.lineEditBedroom.text()),
                float(self.lineEditPopulation.text())
            ]]

            y_pred = self.model.predict(X)[0]
            self.lineEditPrice.setText(f"{y_pred:,.2f}")

        except ValueError:
            QMessageBox.warning(self, "Input Error",
                                "Please enter valid numeric values for all fields.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_fields(self):
        self.lineEditIncome.clear()
        self.lineEditHouseAge.clear()
        self.lineEditRooms.clear()
        self.lineEditBedroom.clear()
        self.lineEditPopulation.clear()
        self.lineEditPrice.clear()
