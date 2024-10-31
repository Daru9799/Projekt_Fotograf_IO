import sys
from PyQt5.QtWidgets import QApplication
from view.mainView import MainView
from presenter.mainPresenter import Presenter

if __name__ == '__main__':
    app = QApplication(sys.argv)

    presenter = Presenter(None)  # Inicjalizacja prezentera bez widoku
    view = MainView(presenter)  # Teraz przekazujemy prezentera do widoku
    presenter.view = view  # Wstrzyknięcie widoku do prezentera

    view.show()
    sys.exit(app.exec_())