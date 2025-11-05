import sys
from PyQt6.QtWidgets import QApplication
from ui.HousePricePrediction_Ext import HousePricePredictionExt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HousePricePredictionExt()
    window.show()
    sys.exit(app.exec())
