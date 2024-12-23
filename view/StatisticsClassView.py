from PyQt5 import QtCore, QtGui, QtWidgets


class StatisticsClassView(object):
    def setupUi(self, class_statistics_window, presenter):
        super().__init__()
        self.presenter = presenter

        class_statistics_window.setObjectName("class_statistics_window")
        class_statistics_window.setWindowModality(QtCore.Qt.NonModal)
        class_statistics_window.resize(629, 479)
        font = QtGui.QFont()
        font.setPointSize(9)
        class_statistics_window.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(class_statistics_window)
        self.gridLayout.setContentsMargins(12, 12, 12, 12)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.title_label = QtWidgets.QLabel(class_statistics_window)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.gridLayout.addWidget(self.title_label, 0, 1, 1, 1)
        self.class_tableView = QtWidgets.QTableView(class_statistics_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.class_tableView.setFont(font)
        self.class_tableView.setSortingEnabled(True)
        self.class_tableView.setObjectName("class_tableView")
        self.gridLayout.addWidget(self.class_tableView, 1, 1, 1, 1)

        self.retranslateUi(class_statistics_window)
        QtCore.QMetaObject.connectSlotsByName(class_statistics_window)

    def retranslateUi(self, annotation_statistics_window):
        _translate = QtCore.QCoreApplication.translate
        annotation_statistics_window.setWindowTitle(_translate("annotation_statistics_window", "Klasy"))
        self.title_label.setText(_translate("annotation_statistics_window", "Klasy"))
