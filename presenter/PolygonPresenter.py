from PyQt5.QtCore import QObject
import cv2
import numpy as np
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap


class PolygonPresenter(QObject):

    def __init__(self, view, presenter):
        super().__init__()
        self.view = view
        self.presenter = presenter


        self.current_polygon_points = []
        self.polygon_closed = False
        self.point_radius = 5  # Promień kółek dla wierzchołków
        self.close_distance_multiplier = 2
        self.temp_polygon_item = None  # referencja to rysowanego polygona
        self.cursor_pos = [0,0]
        self.color = (0, 0, 0, 255)  # RGB

        # self.allow_drawing = False

    def is_near_starting_point(self, x, y):
        """Sprawdza, czy punkt (x, y) jest blisko pierwszego punktu bieżącego wielokąta."""
        if not self.current_polygon_points:
            return False
        start_point = self.current_polygon_points[0]
        distance = np.linalg.norm(np.array([x, y]) - np.array(start_point))
        return distance < self.point_radius * self.close_distance_multiplier  # Zwiększony obszar dla łatwiejszego zamknięcia

    # Funkcja odpowiedzialna za narysowanie wszystkich wirzchołków polygona na nowej powierzchni rysunkowej
    def drawing_polygon(self):
        #print("--- Lista aktualnych punktów polygona: ---")
        #print( self.current_polygon_points)
        drawing_surface = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4),dtype=np.uint8)
        #drawing_surface[:, :, 3] = 255
        #border_color = (abs(self.color[0] - 50), abs(self.color[1] - 50), abs(self.color[2] - 50))
        if len(self.current_polygon_points) != 0:

            # konwersja listy punktów((x,y)) -> np.array, dla poprawnego rysowania cv2
            np_points = np.array(self.current_polygon_points, dtype=np.int32)
            np_points = np_points.reshape((-1, 1, 2))

            if len(np_points) > 1: # rysowanie całego polygona
                cv2.polylines(drawing_surface, [np_points], isClosed=False, thickness=2, color=self.color )
                for point in np_points:
                    cv2.circle(drawing_surface, tuple(point[0]), self.point_radius, self.color, -1)

            else: # rysowanie pierszego wierzchołka
                cv2.circle(drawing_surface, tuple(np_points[0][0]), self.point_radius, self.color, -1)

            # if self.polygon_closed:
            #     fill_color = (self.color[0], self.color[1], self.color[2], 120)
            #     cv2.fillPoly(drawing_surface, [np_points], color=fill_color)

            # Rysowanie lini podążającej za kursorem:
            if len(np_points) > 0 and not self.polygon_closed:
                last_point = np_points[-1][0]  # Ostatni punkt
                cv2.line(drawing_surface, tuple(last_point), (self.cursor_pos[0], self.cursor_pos[1]), self.color, 2)

        self.draw_item_on_scene(drawing_surface)

    def draw_item_on_scene(self, drawing_surface):
        # Utwórz QImage z obrazu numpy (z zachowaniem przezroczystości)
        height, width, channel = drawing_surface.shape
        bytes_per_line = 4 * width
        # Tworzymy QImage z formatem BGRA
        qimage = QImage(drawing_surface.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        # Utwórz QPixmap z QImage
        pixmap = QPixmap.fromImage(qimage)
        # Dodanie nowego prostokąta do sceny
        self.view.scene.removeItem(self.temp_polygon_item)
        self.temp_polygon_item = QGraphicsPixmapItem(pixmap)

        self.view.scene.addItem(self.temp_polygon_item)

    def set_cursor_pos(self,x,y):
        self.cursor_pos = [x,y]
        if len(self.current_polygon_points) != 0: # Nie chcemy rysować jeśli polygon nie ma wierzchołków
            self.drawing_polygon()

    # Sprawdza czy punkt (x,y) znajduje się w polu polygona
    def check_inclusion(self,x,y):
        np_points = np.array(self.current_polygon_points, dtype=np.int32)
        #np_points = np_points.reshape((-1, 1, 2))
        result = cv2.pointPolygonTest(np_points, (x,y), False)
        return result

    def cancel_drawing_polygon(self):
        self.view.scene.removeItem(self.temp_polygon_item)
        self.temp_polygon_item = None
        self.polygon_closed = False
        self.current_polygon_points.clear()
        self.view.set_draw_polygon_button_text("Rysuj poligon")

        #Wczytanie na nowo adnotacji żeby żadna adnotacja nie była zaznaczona po wyjściu z rysowania
        self.presenter.annotation_presenter.updateItems()

    def update_color(self, color):
        self.color = (color[0],color[1],color[2],255)