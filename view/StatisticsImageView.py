from PyQt5 import QtCore, QtGui, QtWidgets


class StatisticsImageView(object):
    def setupUi(self, image_statistics_window, presenter):
        super().__init__()
        self.presenter = presenter

        image_statistics_window.setObjectName("image_statistics_window")
        image_statistics_window.setWindowModality(QtCore.Qt.NonModal)
        image_statistics_window.resize(629, 479)
        font = QtGui.QFont()
        font.setPointSize(9)
        image_statistics_window.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(image_statistics_window)
        self.verticalLayout.setContentsMargins(12, 12,12, 12)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(image_statistics_window)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.image_listWidget = QtWidgets.QListWidget(image_statistics_window)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.image_listWidget.setFont(font)
        self.image_listWidget.setObjectName("image_listWidget")
        self.verticalLayout.addWidget(self.image_listWidget)

        self.retranslateUi(image_statistics_window)
        QtCore.QMetaObject.connectSlotsByName(image_statistics_window)

    def retranslateUi(self, image_statistics_window):
        _translate = QtCore.QCoreApplication.translate
        image_statistics_window.setWindowTitle(_translate("image_statistics_window", "Obrazy"))
        self.title_label.setText(_translate("image_statistics_window", "Obrazy"))
