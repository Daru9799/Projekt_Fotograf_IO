import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from view.mainView import MainView
from presenter.mainPresenter import Presenter
from qt_material import apply_stylesheet
from css import viewCSS

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml', extra=viewCSS.extra) #pelna lista wraz z modyfikacjami https://github.com/UN-GCPDS/qt-material

    presenter = Presenter(None)  # Inicjalizacja prezentera bez widoku
    MainWindow = QtWidgets.QMainWindow()
    ui = MainView()
    ui.setupUi(MainWindow, presenter)
    presenter.update_view(ui) #Wstrzyknięcie widoku do prezentera (wlasciwie to jego aktualizacja)
    MainWindow.show()
    sys.exit(app.exec_())