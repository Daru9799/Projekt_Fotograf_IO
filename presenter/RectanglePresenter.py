from PyQt5.QtCore import QObject
import cv2
import numpy as np
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap

class RectanglePresenter(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.rectangle_start_point = (None, None)  # Punkt początkowy nowo rysowanego prostokąta (x, y)
        self.points = [] #w tym przypadku zwróci 4 punkty (wierzchołki prostokąta w liście)
        self.temp_rectangle_item = None #referencja to rysowanego rectangle

    def draw_rectangle(self, x1, y1, x2, y2):
        #Utworzenie obrazu z przezroczystym tłem w OpenCV (BGRA) (Najpierw jest height potem width, muszą być to wymiary aktualnei wyswietlanego obrazka)
        image = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4), dtype=np.uint8)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) #Konwersja współrzędnych na typ int
        #Parametry obramówki i wypełnienia
        border_color = (200, 0, 0, 255)
        fill_color = (255, 0, 0, 80)  #Dla A im mniejsza wartość, tym bardziej przezroczysty
        border_thickness = 2
        #Ustawienie współrzędnych tak aby kolejność zawsze wskazywała podążanie od lewego górnego wierzchołka zgodnie ze wskazówkami zegara
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        #rysowanie wypełnienia
        cv2.rectangle(image, (x1, y1), (x2, y2), fill_color, thickness=-1)
        # rysowanie obramówki
        cv2.rectangle(image, (x1, y1), (x2, y2), border_color, thickness=border_thickness)
        #funkcja która rysuje to wszystko na scenie jako jeden element
        self.draw_item_on_scene(image)
        #Ustawienie współrzędnych prosotkąta. Od lewego górnego do lewego dolnego zgodnie ze wskazówkami zegara
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

    #Usuwanie tymczasowego obiektu ze sceny
    def delete_temp_rectangle(self):
        if self.temp_rectangle_item:
            self.view.scene.removeItem(self.temp_rectangle_item)
            self.temp_rectangle_item = None

    def get_rectangle_points(self):
        return self.points

    def update_start_point(self, x, y):
        self.rectangle_start_point = (x, y)

    def cancel_drawing_rectangle(self):
        if self.rectangle_start_point != (None, None):
            self.delete_temp_rectangle()
            self.update_start_point(None, None)
        self.view.set_draw_rectangle_button_text("Rysuj prostokąt")
        self.view.change_to_arrow_cursor()

