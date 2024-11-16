from PyQt5.QtCore import QObject
import cv2
import numpy as np
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap

class RectanglePresenter(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.points = [] #w tym przypadku zwróci 4 punkty (wierzchołki prostokąta w liście)
        self.temp_rectangle_item = None #referencja to rysowanego rectangle

    def draw_rectangle(self, x1, y1, x2, y2):
        # Utworzenie obrazu z przezroczystym tłem w OpenCV (BGRA) (Najpierw jest height potem width, muszą być to wymiary aktualnei wyswietlanego obrazka)
        image = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4), dtype=np.uint8)

        # Konwersja współrzędnych na typ int
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        #Parametry obramówki
        border_color = (200, 0, 0, 255)
        fill_color = (255, 0, 0, 80)  #Dla A im mniejsza wartość, tym bardziej przezroczysty
        border_thickness = 2

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        #obramówka
        cv2.rectangle(image, (x1, y1), (x2, y2), border_color, thickness=border_thickness)

        #środek
        cv2.rectangle(image, (x1 + border_thickness, y1 + border_thickness),
                     (x2 - border_thickness, y2 - border_thickness), fill_color, thickness=-1)

        self.draw_item_on_scene(image)
        #Od lewego górnego do lewego dolnego zgodnie ze wskazówkami zegara
        self.points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    #Funkcja ogólna, która obrabia to co chcemy narysowac i umieszcza w scenie
    def draw_item_on_scene(self, image):
        # Utwórz QImage z obrazu numpy (z zachowaniem przezroczystości)
        height, width, channel = image.shape
        bytes_per_line = 4 * width

        # Tworzymy QImage z formatem BGRA
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGBA8888)

        # Utwórz QPixmap z QImage
        pixmap = QPixmap.fromImage(qimage)

        # Dodanie nowego prostokąta do sceny
        self.temp_rectangle_item = QGraphicsPixmapItem(pixmap)
        self.view.scene.addItem(self.temp_rectangle_item)

    #Potem się przyda gdy będziemy chcieli usunąć tymczasowy obiekt
    def delete_temp_rectangle(self):
        if self.temp_rectangle_item:
            self.view.scene.removeItem(self.temp_rectangle_item)
            self.temp_rectangle_item = None

    def get_rectangle_points(self):
        return self.points

