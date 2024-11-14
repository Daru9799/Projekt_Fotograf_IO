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

    def draw_rectangle(self, x1, y1, x2, y2):
        # Utworzenie obrazu z przezroczystym tłem w OpenCV (BGRA) (Najpierw jest height potem width, muszą być to wymiary aktualnei wyswietlanego obrazka)
        image = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4),
                         dtype=np.uint8)

        # Konwersja współrzędnych na typ int
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Ustawienie koloru prostokąta (czerwony przezroczystością, potem bedzię bral kolor klasy!)
        alpha_value = 80  # Im mniejsza wartość, tym bardziej przezroczysty
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0 , 0, alpha_value), -1)

        # Utwórz QImage z obrazu numpy (z zachowaniem przezroczystości)
        height, width, channel = image.shape
        bytes_per_line = 4 * width

        # Tworzymy QImage z formatem BGRA
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGBA8888)

        # Utwórz QPixmap z QImage
        pixmap = QPixmap.fromImage(qimage)

        # Dodanie do sceny obrazka (na scene składa się wyświetlany obrazek)
        self.view.temp_rectangle_item = QGraphicsPixmapItem(pixmap)
        self.view.scene.addItem(self.view.temp_rectangle_item)