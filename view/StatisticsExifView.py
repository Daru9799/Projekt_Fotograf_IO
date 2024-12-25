from PyQt5 import QtCore, QtGui, QtWidgets


class StatisticsExifView(object):
    def setupUi(self, exif_statistics_window, presenter):
        super().__init__()
        self.presenter = presenter

        exif_statistics_window.setObjectName("exif_statistics_window")

        #exif_statistics_window.resize(629, 479)
        exif_statistics_window.setFixedSize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(9)
        exif_statistics_window.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(exif_statistics_window)
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")

        self.title_label = QtWidgets.QLabel(exif_statistics_window)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)

        # Obszar przewijania
        self.scrollArea = QtWidgets.QScrollArea(exif_statistics_window)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # Widget zawierający wykresy
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(12, 12, 12, 12)
        self.scrollLayout.setSpacing(6)

        self.scrollArea.setWidget(self.scrollWidget)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(exif_statistics_window)
        QtCore.QMetaObject.connectSlotsByName(exif_statistics_window)

    def retranslateUi(self, exif_statistics_window):
        _translate = QtCore.QCoreApplication.translate
        exif_statistics_window.setWindowTitle(_translate("exif_statistics_window", "Metadane"))
        self.title_label.setText(_translate("exif_statistics_window", "Metadane"))
