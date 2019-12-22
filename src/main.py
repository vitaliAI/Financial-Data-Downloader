from datetime import datetime
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from yahoo_downloader.data import (
    downloand_ticker_price_data,
    downloand_ticker_option_data,
    downloand_ticker_fundamentals_data,
)
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.data_download_button()
        self.handle_sidebar()
        self.handle_browse()
        self.init_ui()
        # self._change_theme()

    def init_ui(self):
        self.tabWidget.setCurrentIndex(0)
        self.end_date.setDate(datetime.now())

    def handle_browse(self):
        self.browse.clicked.connect(self._browse)
        self.browse_4.clicked.connect(self._browse_4)
        self.browse_3.clicked.connect(self._browse_3)

    def handle_sidebar(self):
        self.priceData.clicked.connect(self._price_data_tab)
        self.priceData_2.clicked.connect(self._fundamental_data_tab)
        self.priceData_3.clicked.connect(self._options_data_tab)

    def _change_theme(self):
        style = open('themes/qdark.qss', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def _price_data_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def _fundamental_data_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def _options_data_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def _browse(self):
        save_location, _ = QFileDialog.getSaveFileName(self, caption='Save as', dir='.', filter="*.csv")
        self.save_as.setText(save_location)

    def _browse_4(self):
        save_location, _ = QFileDialog.getSaveFileName(self, caption='Save as', dir='.', filter="*.csv")
        self.save_as_4.setText(save_location)

    def _browse_3(self):
        save_location, _ = QFileDialog.getSaveFileName(self, caption='Save as', dir='.', filter="*.csv")
        self.save_as_3.setText(save_location)

    def data_download_button(self):
        self.pushButton_2.clicked.connect(self._download_pricing_data)
        self.pushButton_7.clicked.connect(self._download_option_data)
        self.pushButton_3.clicked.connect(self._download_fundamental_data)

    def _download_fundamental_data(self):
        ticker = self.ticker_2.text()
        location = self.save_as_3.text()
        combobox = self.comboBox.currentText()
        if ticker and location:
            data = self._fetch_data_by_combobox(key=combobox, ticker=ticker)
            data.to_csv(location)
            self.progressBar_2.setValue(100)

    def _fetch_data_by_combobox(self, key, ticker):
        inst = downloand_ticker_fundamentals_data(ticker=ticker)
        return {'Calendar': inst.calendar.T,
                'Sustainability': inst.sustainability,
                'Recommendations': inst.recommendations,
                'Annual Cashflow': inst.cashflow.T,
                'Quarterly Cashflow': inst.quarterly_cashflow.T,
                'Annual Balance sheet': inst.balance_sheet.T,
                'Quarterly Balance sheet': inst.quarterly_balance_sheet.T,
                'Annual Earnings': inst.earnings,
                'Quarterly Earnings': inst.quarterly_earnings,
                'Annual Financials': inst.financials.T,
                'Quarterly Financials': inst.quarterly_financials.T}[key]

    def _download_option_data(self):
        ticker = self.ticker_6.text()
        location = self.save_as_4.text()
        if ticker:
            options = downloand_ticker_option_data(ticker=ticker)
            if location:
                options.calls.to_csv(f'{location[:-4]}_calls.csv')
                options.puts.to_csv(f'{location[:-4]}_puts.csv')
                self.progressBar_6.setValue(100)

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
