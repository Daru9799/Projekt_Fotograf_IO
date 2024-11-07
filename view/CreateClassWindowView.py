from PyQt5 import QtCore, QtGui, QtWidgets

#from presenter.ClassManagerPresenter import ClassManagerPresenter

class CreateClassWindowView(object):
    def setupUi(self, Add_new_class_window, presenter):
        super().__init__()
        self.presenter = presenter

        Add_new_class_window.setObjectName("Add_new_class_window")
        Add_new_class_window.setFixedSize(480, 175)
        font = QtGui.QFont()
        font.setPointSize(9)
        Add_new_class_window.setFont(font)
        self.Save_class = QtWidgets.QPushButton(Add_new_class_window)
        self.Save_class.setGeometry(QtCore.QRect(170, 130, 141, 23))
        self.Save_class.setObjectName("Save_class")
        self.Class_name_line_edit = QtWidgets.QLineEdit(Add_new_class_window)
        self.Class_name_line_edit.setGeometry(QtCore.QRect(70, 60, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Class_name_line_edit.setFont(font)
        self.Class_name_line_edit.setAutoFillBackground(False)
        self.Class_name_line_edit.setObjectName("Class_name_line_edit")

        self.retranslateUi(Add_new_class_window)
        QtCore.QMetaObject.connectSlotsByName(Add_new_class_window)

    def retranslateUi(self, Add_new_class_window):
        _translate = QtCore.QCoreApplication.translate
        Add_new_class_window.setWindowTitle(_translate("Add_new_class_window", "New Class"))
        self.Save_class.setText(_translate("Add_new_class_window", "Zapisz"))
        self.Class_name_line_edit.setText(_translate("Add_new_class_window", ""))


    # Podpięcia pod akcje
        self.Save_class.clicked.connect(self.presenter.saveClass)   #Zapis klasy