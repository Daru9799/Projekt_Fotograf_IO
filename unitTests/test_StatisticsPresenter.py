#from presenter.StatisticsPresenter import StatisticsPresenter
import pytest

import sys
import os

# Dodanie głównego folderu projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from view.mainView import MainView
from presenter.mainPresenter import Presenter
from PyQt5 import QtWidgets

# @pytest.fixture
# def get_main_presenter():
#     presenter = Presenter(None)  # Inicjalizacja prezentera bez widoku
#     MainWindow = QtWidgets.QMainWindow()
#     ui = MainView()
#     ui.setupUi(MainWindow, presenter)
#     presenter.update_view(ui)  # Wstrzyknięcie widoku do prezentera (wlasciwie to jego aktualizacja)
#     presenter.create_new_project()
#     return presenter
#
# def test_Stat_Annot(get_main_presenter):
#     presenter = get_main_presenter
#
#     # Testowanie wyświetlania statystyk przy braku klas
#     presenter.new_project.list_of_classes_model = []
#     assert presenter.new_project.get_list_of_images_size() == 0


def test_start():
    assert 1 == 1
