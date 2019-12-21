from datetime import datetime
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from yahoo_downloader.data import (
    downloand_ticker_price_data,
)
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pricing_data_download_button()
        self.handle_sidebar()
        self.handle_browse()
        self.init_ui()

    def init_ui(self):
        self.end_date.setDate(datetime.now())
        # style = open('themes/qdark.qss', 'r')
        # style = style.read()
        # self.setStyleSheet(style)

    def handle_browse(self):
        self.browse.clicked.connect(self._browse)

    def handle_sidebar(self):
        self.priceData.clicked.connect(self._price_data_tab)
        self.priceData_2.clicked.connect(self._fundamental_data_tab)
        self.priceData_3.clicked.connect(self._options_data_tab)

    def _price_data_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def _fundamental_data_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def _options_data_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def _browse(self):
        save_location, _ = QFileDialog.getSaveFileName(self, caption='Save as', dir='.', filter="*.csv")
        self.save_as.setText(save_location)

    def pricing_data_download_button(self):
        self.pushButton_2.clicked.connect(self._download_pricing_data)

    def _download_pricing_data(self):
        ticker = self.ticker.text()
        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()
        location = self.save_as.text()
        if ticker:
            price_data = downloand_ticker_price_data(ticker=ticker, start=str(start), end=str(end), actions=True)
            if location:
                price_data.to_csv(location)
                self.progressBar.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
