import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMainWindow, QVBoxLayout, \
    QWidget, QCheckBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
import random


class RealTimeOpenCVViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Wstępne ustawienie
        # Białe tło
        #self.cv_image = np.ones((500, 500, 3), dtype=np.uint8) * 255

        #Chciałem wczytać jakiś obraz z !OBRAZKI DO TESTÓW dla przykładu, ale się nie dało
        # self.cv_image = cv2.imread(r"!OBRAZKI DO TESTÓW/12619301763_5513923709_b.jpg")

        # Ale udało się wczytać z obraz img/cameraIcon.png
        self.cv_image = cv2.imread("img/cameraIcon.png")
        self.current_polygon_points = []
        self.polygons = []  # Lista przechowująca wielokąty z ich kolorami
        self.polygon_closed = False
        self.current_color = self.random_color()  # Losowy kolor dla pierwszego wielokąta
        self.point_radius = 5  # Promień kółek dla wierzchołków
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.selected_vertex = None  # Zmienna przechowująca wybrany wierzchołek
        self.is_dragging = False  # Flaga informująca o rozpoczęciu przeciągania
        self.update_image()  # Pierwsza aktualizacja wyświetlania
        self.allow_drawing = True  # Flaga mówiąca, czy użytkownik może rysować nowe wielokąty

    def random_color(self):
        """Zwraca losowy kolor w formacie BGR."""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update_image(self):
        # Rysowanie wszystkich zamkniętych wielokątów
        temp_image = self.cv_image.copy()
        for points, color in self.polygons:
            if len(points) > 1:
                cv2.polylines(temp_image, [np.array(points)], isClosed=True, color=color, thickness=2)
                for point in points:
                    cv2.circle(temp_image, point, self.point_radius, color, -1)  # Rysowanie wierzchołków

        # Rysowanie aktualnie edytowanego wielokąta
        if len(self.current_polygon_points) > 1:
            cv2.polylines(temp_image, [np.array(self.current_polygon_points)], isClosed=self.polygon_closed,
                          color=self.current_color, thickness=2)
        for point in self.current_polygon_points:
            cv2.circle(temp_image, point, self.point_radius, self.current_color,
                       -1)  # Rysowanie wierzchołków bieżącego wielokąta

        # Konwersja OpenCV obrazu na QPixmap
        height, width, channel = temp_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(temp_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)

        # Aktualizacja QGraphicsPixmapItem w QGraphicsScene
        self.pixmap_item.setPixmap(pixmap)

    def is_near_starting_point(self, x, y):
        """Sprawdza, czy punkt (x, y) jest blisko pierwszego punktu bieżącego wielokąta."""
        if not self.current_polygon_points:
            return False
        start_point = self.current_polygon_points[0]
        distance = np.linalg.norm(np.array([x, y]) - np.array(start_point))
        return distance < self.point_radius * 2  # Zwiększony obszar dla łatwiejszego zamknięcia

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = event.pos()
            scene_point = self.mapToScene(point)
            x, y = int(scene_point.x()), int(scene_point.y())

            if self.allow_drawing:
                # Sprawdzanie, czy kliknięto na początkowy wierzchołek, aby zamknąć wielokąt
                if len(self.current_polygon_points) > 2 and self.is_near_starting_point(x, y):
                    self.polygon_closed = True
                    # Dodajemy zamknięty wielokąt do listy z jego kolorem
                    self.polygons.append((self.current_polygon_points.copy(), self.current_color))
                    self.current_polygon_points.clear()  # Czyścimy bieżące punkty
                    self.current_color = self.random_color()  # Generujemy nowy kolor dla następnego wielokąta
                    self.polygon_closed = False
                elif not self.is_dragging:
                    # Dodanie nowego punktu do bieżącego wielokąta
                    self.current_polygon_points.append((x, y))

                self.update_image()  # Aktualizacja obrazu po dodaniu punktu lub zamknięciu wielokąta
            else:
                # Jeśli checkbox jest odznaczony, możemy edytować istniejące poligony
                for polygon_points in self.polygons:
                    for idx, polygon_point in enumerate(polygon_points[0]):
                        distance = np.linalg.norm(np.array([x, y]) - np.array(polygon_point))
                        if distance < self.point_radius:
                            self.selected_vertex = (polygon_points[0], idx)
                            self.is_dragging = True
                            break

                # Jeśli kliknięto na wierzchołek bieżącego poligona
                if self.selected_vertex is None:
                    for idx, polygon_point in enumerate(self.current_polygon_points):
                        distance = np.linalg.norm(np.array([x, y]) - np.array(polygon_point))
                        if distance < self.point_radius:
                            self.selected_vertex = (self.current_polygon_points, idx)
                            self.is_dragging = True
                            break

                self.update_image()  # Aktualizacja obrazu

    def mouseMoveEvent(self, event):
        if self.is_dragging and self.selected_vertex:
            point = event.pos()
            scene_point = self.mapToScene(point)
            x, y = int(scene_point.x()), int(scene_point.y())

            # Przesuwanie wybranego wierzchołka
            polygon_points, idx = self.selected_vertex
            polygon_points[idx] = (x, y)
            self.update_image()  # Aktualizacja obrazu po przesunięciu wierzchołka

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.selected_vertex = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            # Resetowanie, gdy naciśniesz 'R'
            self.polygons.clear()
            self.current_polygon_points.clear()
            self.polygon_closed = False
            self.update_image()

    def set_drawing_mode(self, is_drawing):
        """Zmieniamy tryb: rysowanie nowych poligonów lub edytowanie istniejących."""
        self.allow_drawing = is_drawing


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.viewer = RealTimeOpenCVViewer()

        # Tworzymy checkbox do zmiany trybu
        self.checkbox = QCheckBox("Edytuj wierzchołki poligonów")
        self.checkbox.setChecked(False)
        self.checkbox.toggled.connect(self.on_checkbox_toggled)

        # Tworzymy układ z widżetem checkboxa i widokiem
        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.viewer)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("Real-Time OpenCV in QGraphicsView with Multiple Polygons and Vertex Editing")
        self.resize(520, 520)

    def on_checkbox_toggled(self):
        """Zmienia tryb w zależności od stanu checkboxa."""
        self.viewer.set_drawing_mode(not self.checkbox.isChecked())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
