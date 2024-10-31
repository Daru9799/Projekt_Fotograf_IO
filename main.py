import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from view.mainView import MainView
from presenter.mainPresenter import Presenter
from qt_material import apply_stylesheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml') #pelna lista wraz z modyfikacjami https://github.com/UN-GCPDS/qt-material

    presenter = Presenter(None)  # Inicjalizacja prezentera bez widoku
    MainWindow = QtWidgets.QMainWindow()
    ui = MainView()
    ui.setupUi(MainWindow, presenter)
    presenter.view = ui  # Wstrzyknięcie widoku do prezentera
    MainWindow.show()
    sys.exit(app.exec_())