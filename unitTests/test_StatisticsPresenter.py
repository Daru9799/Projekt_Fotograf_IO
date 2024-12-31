import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget

# Dodanie głównego folderu projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from presenter.StatisticsPresenter import StatisticsPresenter

@pytest.fixture
def setup_statistics_presenter(qtbot):
    # Tworzenie aplikacji Qt
    app = QApplication.instance() or QApplication([])

    # Prawdziwy obiekt QWidget jako placeholder dla self.view
    view_widget = QWidget()

    # Mockowanie pozostałych zależności
    project_mock = MagicMock()
    presenter_mock = MagicMock()

    # Mockowanie danych projektu
    project_mock.get_images_list.return_value = [
        MagicMock(
            has_annotation=True,
            get_annotation_list=lambda: [MagicMock(class_id=1), MagicMock(class_id=2)],
            get_annotation_size=lambda: 2,
            width=1920,
            height=1080,
            filename="image1.jpg"
        ),
        MagicMock(
            has_annotation=False,
            get_annotation_list=lambda: [],
            get_annotation_size=lambda: 0,
            width=1280,
            height=720,
            filename="image2.png"
        ),
    ]
    project_mock.get_classes_list.return_value = [
        MagicMock(class_id=1, name="Class A"),
        MagicMock(class_id=2, name="Class B"),
    ]
    project_mock.get_list_of_images_size.return_value = 2

    # Tworzenie instancji klasy StatisticsPresenter
    stats_presenter = StatisticsPresenter(view_widget, project_mock, presenter_mock)
    return stats_presenter, project_mock

def test_count_all_adnotations(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    assert stats_presenter.count_all_adnotations() == 2  # Dwie adnotacje w obrazie

def test_count_img_with_annotations(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    assert stats_presenter.count_img_with_annotations() == 1  # Jeden obraz z adnotacjami

def test_count_img_without_annotation(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    assert stats_presenter.count_img_without_annotation() == 1  # Jeden obraz bez adnotacji

def test_count_img_with_mult_annotations(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    assert stats_presenter.count_img_with_mult_annotations() == 1  # Jeden obraz z wieloma adnotacjami

def test_determine_min_max_average_img_resolution(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    result = stats_presenter.determine_min_max_average_img_resolution()
    assert result[0] == (1280, 720)  # Najmniejsza rozdzielczość
    assert result[1] == (1920, 1080)  # Największa rozdzielczość
    assert result[2] == (1600, 900)  # Średnia rozdzielczość

def test_count_class_usage(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    class_usage = stats_presenter.count_class_usage()
    assert class_usage[1] == 1  # Klasa A użyta raz
    assert class_usage[2] == 1  # Klasa B użyta raz

def test_calcualte_class_procentage_usage(setup_statistics_presenter):
    stats_presenter, _ = setup_statistics_presenter
    class_percentage = stats_presenter.calcualte_class_procentage_usage()
    assert class_percentage[1] == 50.0  # Klasa A 50%
    assert class_percentage[2] == 50.0  # Klasa B 50%
