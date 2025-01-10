import pytest
from unittest.mock import MagicMock
import numpy as np
from PyQt5.QtWidgets import QApplication
from presenter.RectanglePresenter import RectanglePresenter

@pytest.fixture
def setup_rectangle_presenter():
    #Mock dla widoku
    view_mock = MagicMock()
    presenter_mock = MagicMock()
    #Mockowanie pixmap_item i jej metod
    view_mock.pixmap_item = MagicMock()
    view_mock.pixmap_item.pixmap.return_value.height.return_value = 500
    view_mock.pixmap_item.pixmap.return_value.width.return_value = 500
    view_mock.scene = MagicMock()
    #Utworzenie instancji RectanglePresenter
    rectangle_presenter = RectanglePresenter(view_mock, presenter_mock)
    return rectangle_presenter, view_mock, presenter_mock

#Utworzenie aplikacji PyQt5, aby uruchomić GUI (bez tego się wysypywało)
@pytest.fixture(scope="module", autouse=True)
def app():
    app = QApplication([])
    yield app
    app.quit()

#Testowanie funkcji rysującej prostokąt
def test_draw_rectangle(setup_rectangle_presenter):
    rectangle_presenter, view_mock, _ = setup_rectangle_presenter
    x1, y1, x2, y2 = 50, 50, 200, 200
    rectangle_presenter.draw_rectangle(x1, y1, x2, y2)
    #Sprawdzenie czy wszystko zostało poprawnie przypisane
    assert len(rectangle_presenter.points) == 4
    assert rectangle_presenter.points[0] == (50, 50)
    assert rectangle_presenter.points[2] == (200, 200)

#Test rysowania na scenie
def test_draw_item_on_scene(setup_rectangle_presenter):
    rectangle_presenter, view_mock, _ = setup_rectangle_presenter
    image = np.zeros((500, 500, 4), dtype=np.uint8)
    rectangle_presenter.draw_item_on_scene(image)
    view_mock.scene.addItem.assert_called_once()

#Test usuwania tymczasowego prostokąta
def test_delete_temp_rectangle(setup_rectangle_presenter):
    rectangle_presenter, view_mock, _ = setup_rectangle_presenter
    rectangle_presenter.temp_rectangle_item = MagicMock()
    rectangle_presenter.delete_temp_rectangle()
    #Sprawdzenie, czy temp_rectangle_item zostało ustawione na None po usunięciu
    assert rectangle_presenter.temp_rectangle_item is None

#Test aktualizacji punktu startowego
def test_update_start_point(setup_rectangle_presenter):
    rectangle_presenter, view_mock, _ = setup_rectangle_presenter
    rectangle_presenter.update_start_point(100, 100)
    assert rectangle_presenter.rectangle_start_point == (100, 100)

#Test anulowania rysowania prostokąta
def test_cancel_drawing_rectangle(setup_rectangle_presenter):
    rectangle_presenter, view_mock, presenter_mock = setup_rectangle_presenter
    rectangle_presenter.cancel_drawing_rectangle()
    #Test zmiany tekstu przycisku
    view_mock.set_draw_rectangle_button_text.assert_called_with("Rysuj prostokąt")
    #Test zmiany kursora
    view_mock.change_to_arrow_cursor.assert_called()
    #Sprawdzenie czy funkcja update_items została wywołana na presenterze
    presenter_mock.annotation_presenter.update_items.assert_called_once()

def test_update_color(setup_rectangle_presenter):
    rectangle_presenter, view_mock, _ = setup_rectangle_presenter
    rectangle_presenter.update_color((255, 0, 0))
    #Sprawdzenie czy kolor został zaktualizowany
    assert rectangle_presenter.color == (255, 0, 0)