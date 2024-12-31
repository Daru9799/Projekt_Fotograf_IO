import pytest
from unittest.mock import MagicMock

import sys
import os

# Dodanie głównego folderu projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from presenter.ScenePreseter import ScenePresenter

@pytest.fixture
def setup_scene_presenter():
    # Mockowanie zależności
    view_mock = MagicMock()
    presenter_mock = MagicMock()
    project_mock = MagicMock()

    # Mockowanie elementów widoku
    view_mock.pixmap_item.pixmap().height.return_value = 500
    view_mock.pixmap_item.pixmap().width.return_value = 500
    view_mock.scene = MagicMock()

    # Tworzenie instancji klasy ScenePresenter
    scene_presenter = ScenePresenter(view_mock, presenter_mock, project_mock)
    return scene_presenter, view_mock, presenter_mock, project_mock

def test_get_annotations_from_project(setup_scene_presenter):
    scene_presenter, view_mock, presenter_mock, project_mock = setup_scene_presenter

    # Przygotowanie danych wejściowych
    image_mock = MagicMock()
    presenter_mock.image_item.text.return_value = "image.jpg"
    project_mock.get_img_by_filename.return_value.get_annotation_list.return_value = [
        MagicMock(class_id=1, get_segmentation=lambda: [(0, 0), (1, 1), (2, 2)]),
    ]
    presenter_mock.classManagerPresenter.getHiddenClass.return_value = []

    # Wywołanie metody
    scene_presenter.get_annotations_from_project()

    # Assercje
    assert len(scene_presenter.polygons) == 1
    assert scene_presenter.polygons[0][0] == [(0, 0), (1, 1), (2, 2)]

def test_check_inclusion_point_inside_polygon(setup_scene_presenter):
    scene_presenter, _, _, _ = setup_scene_presenter

    polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
    x, y = 5, 5  # Punkt wewnątrz poligona

    assert scene_presenter.check_inclusion(polygon, x, y) is True

def test_check_inclusion_point_outside_polygon(setup_scene_presenter):
    scene_presenter, _, _, _ = setup_scene_presenter

    polygon = [(0, 0), (100, 0), (100, 100), (0, 100)]
    x, y = 105, 55  # Punkt poza poligonem

    assert scene_presenter.check_inclusion(polygon, x, y) is False

def test_handle_select_polygon(setup_scene_presenter):
    scene_presenter, _, _, _ = setup_scene_presenter

    # Przygotowanie danych
    scene_presenter.polygons = [
        [[(0, 0), (10, 0), (10, 10), (0, 10)], (255, 0, 0)],
        [[(20, 20), (30, 20), (30, 30), (20, 30)], (0, 255, 0)],
    ]

    # Wywołanie metody
    scene_presenter.handle_select_polygon(5, 5)  # Punkt wewnątrz pierwszego poligona

    # Assercje
    assert scene_presenter.selected_polygon == scene_presenter.polygons[0]
