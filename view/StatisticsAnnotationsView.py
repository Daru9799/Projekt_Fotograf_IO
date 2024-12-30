from PyQt5 import QtCore, QtGui, QtWidgets


class StatisticsAnnotationsView(object):
    def setupUi(self, annotation_statistics_window, presenter):
        super().__init__()
        self.presenter = presenter

        annotation_statistics_window.setObjectName("annotation_statistics_window")
        #annotation_statistics_window.resize(622, 479)
        annotation_statistics_window.setFixedSize(600, 455)
        font = QtGui.QFont()
        font.setPointSize(9)
        annotation_statistics_window.setFont(font)
        self.annotation_listWidget = QtWidgets.QListWidget(annotation_statistics_window)
        self.annotation_listWidget.setGeometry(QtCore.QRect(20, 60, 561, 381))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.annotation_listWidget.setFont(font)
        self.annotation_listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.annotation_listWidget.setObjectName("annotation_listWidget")
        self.title_label = QtWidgets.QLabel(annotation_statistics_window)
        self.title_label.setGeometry(QtCore.QRect(30, 10, 311, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.title_label.setFont(font)
        self.title_label.setObjectName("title_label")

        self.retranslateUi(annotation_statistics_window)
        QtCore.QMetaObject.connectSlotsByName(annotation_statistics_window)

    def retranslateUi(self, annotation_statistics_window):
        _translate = QtCore.QCoreApplication.translate
        annotation_statistics_window.setWindowTitle(_translate("annotation_statistics_window", "Adnotacje"))
        self.title_label.setText(_translate("annotation_statistics_window", "Adnotacje"))