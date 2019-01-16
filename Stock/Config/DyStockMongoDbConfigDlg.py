import json

from PyQt5.QtWidgets import QDialog, QLabel, QTabWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget

from DyCommon.DyCommon import DyCommon
from Stock.Common.DyStockCommon import DyStockCommon
from .DyStockConfig import DyStockConfig


class DyStockMongoDbConfigDlg(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._read()
        self._initUi()

    def _createCommonDaysTab(self, tabWidget):
        widget = QTabWidget()

        self._createJQDataTab(widget)
        self._createTuShareTab(widget)

        tabWidget.addTab(widget, "通用和日线数据")

    def _createJQDataTab(self, tabWidget):
        widget = QWidget()

        # common data
        labelStockCommonDb = QLabel('股票通用数据库')
        labelTradeDayTableName = QLabel('股票交易日数据库表')
        labelCodeTableName = QLabel('股票代码数据库表')

        self._lineEditStockCommonDbJQData = QLineEdit(self._data["CommonDays"]["JQData"]['stockCommonDb'])
        self._lineEditTradeDayTableNameJQData = QLineEdit(self._data["CommonDays"]["JQData"]['tradeDayTableName'])
        self._lineEditCodeTableNameJQData = QLineEdit(self._data["CommonDays"]["JQData"]['codeTableName'])

        # days data
        labelStockDaysDb = QLabel('股票历史日线数据库')
        self._lineEditStockDaysDbJQData = QLineEdit(self._data["CommonDays"]["JQData"]['stockDaysDb'])

        # 布局
        vbox = QVBoxLayout()
 
        vbox.addWidget(labelStockCommonDb)
        vbox.addWidget(self._lineEditStockCommonDbJQData)
        vbox.addWidget(labelTradeDayTableName)
        vbox.addWidget(self._lineEditTradeDayTableNameJQData)
        vbox.addWidget(labelCodeTableName)
        vbox.addWidget(self._lineEditCodeTableNameJQData)

        vbox.addWidget(QLabel('                                                                                             '))

        vbox.addWidget(labelStockDaysDb)
        vbox.addWidget(self._lineEditStockDaysDbJQData)
 
        widget.setLayout(vbox)

        tabWidget.addTab(widget, "JQData")

    def _createTuShareTab(self, tabWidget):
        widget = QWidget()

        # common data
        labelStockCommonDb = QLabel('股票通用数据库')
        labelTradeDayTableName = QLabel('股票交易日数据库表')
        labelCodeTableName = QLabel('股票代码数据库表')

        self._lineEditStockCommonDbTuShare = QLineEdit(self._data["CommonDays"]["TuShare"]['stockCommonDb'])
        self._lineEditTradeDayTableNameTuShare = QLineEdit(self._data["CommonDays"]["TuShare"]['tradeDayTableName'])
        self._lineEditCodeTableNameTuShare = QLineEdit(self._data["CommonDays"]["TuShare"]['codeTableName'])

        # days data
        labelStockDaysDb = QLabel('股票历史日线数据库')
        self._lineEditStockDaysDbTuShare = QLineEdit(self._data["CommonDays"]["TuShare"]['stockDaysDb'])

        # 布局
        vbox = QVBoxLayout()
 
        vbox.addWidget(labelStockCommonDb)
        vbox.addWidget(self._lineEditStockCommonDbTuShare)
        vbox.addWidget(labelTradeDayTableName)
        vbox.addWidget(self._lineEditTradeDayTableNameTuShare)
        vbox.addWidget(labelCodeTableName)
        vbox.addWidget(self._lineEditCodeTableNameTuShare)

        vbox.addWidget(QLabel('                                                                                             '))

        vbox.addWidget(labelStockDaysDb)
        vbox.addWidget(self._lineEditStockDaysDbTuShare)
 
        widget.setLayout(vbox)

        tabWidget.addTab(widget, "TuShare")

    def _createConnectionTab(self, tabWidget):
        widget = QWidget()

        labelHost = QLabel('主机')
        labelPort = QLabel('端口')

        self._lineEditHost = QLineEdit(self._data['Connection']["Host"])
        self._lineEditPort = QLineEdit(str(self._data['Connection']["Port"]))

        # 布局
        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(labelHost, 0, 0)
        grid.addWidget(self._lineEditHost, 0, 1)

        grid.addWidget(labelPort, 0, 2)
        grid.addWidget(self._lineEditPort, 0, 3)
 
        widget.setLayout(grid)

        tabWidget.addTab(widget, "连接")

    def _createTicksTab(self, tabWidget):
        widget = QWidget()

        labelStockTicksDb = QLabel('股票分笔数据库')
        self._lineEditStockTicksDb = QLineEdit(self._data["Ticks"]['db'])

        # 布局
        hbox = QHBoxLayout()
 
        hbox.addWidget(labelStockTicksDb)
        hbox.addWidget(self._lineEditStockTicksDb)
 
        widget.setLayout(hbox)

        tabWidget.addTab(widget, "分笔数据")

    def _initUi(self):
        self.setWindowTitle('配置-MongoDB')

        tabWidget = QTabWidget()
        self._createConnectionTab(tabWidget)
        self._createCommonDaysTab(tabWidget)
        self._createTicksTab(tabWidget)
        

        cancelPushButton = QPushButton('Cancel')
        okPushButton = QPushButton('OK')
        cancelPushButton.clicked.connect(self._cancel)
        okPushButton.clicked.connect(self._ok)

        # 布局
        grid = QGridLayout()
        grid.setSpacing(10)
 
        grid.addWidget(tabWidget, 0, 0, 2, 1)

        grid.addWidget(okPushButton, 0, 1)
        grid.addWidget(cancelPushButton, 1, 1)
 
        self.setLayout(grid)

    def _read(self):
        file = DyStockConfig.getStockMongoDbFileName()

        # open
        try:
            with open(file) as f:
                self._data = json.load(f)
        except:
            self._data = DyStockConfig.defaultMongoDb

    def _ok(self):
        # get data from UI
        data = {"Connection": {}, "CommonDays": {"JQData": {}, "TuShare": {}}, "Ticks": {}}

        # host & port
        data["Connection"]["Host"] = self._lineEditHost.text()
        data["Connection"]["Port"] = int(self._lineEditPort.text())

        # JQData
        data["CommonDays"]["JQData"]['stockCommonDb'] = self._lineEditStockCommonDbJQData.text()
        data["CommonDays"]["JQData"]['tradeDayTableName'] = self._lineEditTradeDayTableNameJQData.text()
        data["CommonDays"]["JQData"]['codeTableName'] = self._lineEditCodeTableNameJQData.text()
        data["CommonDays"]["JQData"]['stockDaysDb'] = self._lineEditStockDaysDbJQData.text()

        # TuShare
        data["CommonDays"]["TuShare"]['stockCommonDb'] = self._lineEditStockCommonDbTuShare.text()
        data["CommonDays"]["TuShare"]['tradeDayTableName'] = self._lineEditTradeDayTableNameTuShare.text()
        data["CommonDays"]["TuShare"]['codeTableName'] = self._lineEditCodeTableNameTuShare.text()
        data["CommonDays"]["TuShare"]['stockDaysDb'] = self._lineEditStockDaysDbTuShare.text()

        # ticks
        data["Ticks"]['db'] = self._lineEditStockTicksDb.text()

        # config to variables
        DyStockConfig.configStockMongoDb(data)

        # save config
        file = DyStockConfig.getStockMongoDbFileName()
        with open(file, 'w') as f:
            f.write(json.dumps(data, indent=4))

        self.accept()

    def _cancel(self):
        self.reject()