# from poligony import polygons
from PyQt5.QtCore import QObject
import cv2
import numpy as np
import copy
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap

from model.AnnotationModel import AnnotationModel


class ScenePresenter:
    def __init__(self, view, presenter, project):
        self.view = view
        self.presenter = presenter
        self.project = project

        self.annotations = [] #lista adnotacji
        self.polygons = [] #przechowuje liste dwuelementową (punkty, kolor): [[(x,y), (x,y), ...], RGB]
        self.active_image_model = None
        self.point_radius = 3  # Promień kółek dla wierzchołków
        self.polygons_pixmap_ref = None
        self.selected_polygon = [[],[]]

        self.is_dragging = False
        self.selected_vertex = None

    # pobiera listę "annotations" obrazu i na jej podstawie generuje liste "polygons"
    def get_annotations_from_project(self):
        image = self.presenter.image_item
        self.active_image_model = self.project.get_img_by_filename(image.text())
        self.annotations = self.active_image_model.get_annotation_list()
        self.polygons = []
        for obj in self.annotations:
            points_list = obj.get_segmentation()
            color = self.project.get_color_by_class_id(obj.class_id)
            self.polygons.append([points_list,color])
        # print("pobrano")

    # na podstawie listy polygons narysuj poligony
    def draw_annotations(self):
        # na podstawie listy polygons narysuj poligony i dodaj kazdego z nich do listy referencji polygons_item
        drawing_surface = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4), dtype=np.uint8)
        if self.active_image_model.has_annotation:
            for poly in self.polygons:
                np_points = np.array(poly[0], dtype=np.int32)
                np_points = np_points.reshape((-1, 1, 2))
                border_color = (poly[1][0], poly[1][1], poly[1][2], 255)
                # Rysowanie kontóra
                cv2.polylines(drawing_surface, [np_points], isClosed=True, thickness=2, color=border_color)

                # Czy poly ma takie samie wierzchołki co zaznaczony poligon
                if poly[0] == self.selected_polygon[0]:
                    fill_color = (poly[1][0], poly[1][1], poly[1][2], 120)
                    cv2.fillPoly(drawing_surface, [np_points], color=fill_color)
                    for point in np_points:
                        cv2.circle(drawing_surface, tuple(point[0]), self.point_radius, border_color, -1)
                    # print("Wirzchołki były takie same jak w selected_polygon")
                    # print(poly[0])
                    # print(self.selected_polygon[0])

                else:
                    # Wypełnianie polygona kolorem:
                    fill_color = (poly[1][0], poly[1][1], poly[1][2], 160)
                    cv2.fillPoly(drawing_surface, [np_points], color=fill_color)

            #Tymczasowo do sprawdzenia:
            # np_points = np.array(self.selected_vertex[0][1], dtype=np.int32)
            # np_points = np_points.reshape((-1, 1, 2))
            # border_color = (self.selected_vertex[0][1][0], self.selected_vertex[0][1][1], self.selected_vertex[0][1][2], 255)
            # cv2.polylines(drawing_surface, [np_points], isClosed=True, thickness=2, color=border_color)
            # cv2.fillPoly(drawing_surface, [np_points], color=border_color)


        self.draw_item_on_scene(drawing_surface)


    def draw_item_on_scene(self, draw_surf):
        # Utwórz QImage z obrazu numpy (z zachowaniem przezroczystości)
        height, width, channel = draw_surf.shape
        bytes_per_line = 4 * width
        # Tworzymy QImage z formatem BGRA
        qimage = QImage(draw_surf.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        # Utwórz QPixmap z QImage
        pixmap = QPixmap.fromImage(qimage)

        # Dodanie wszystkich adnotacji na obrazek
        # if self.polygons_pixmap_ref is not None:  # Sprawdź, czy obiekt wciąż istnieje w scenie
        #    self.view.scene.removeItem(self.polygons_pixmap_ref)
        # self.polygons_pixmap_ref = None
        self.view.scene.removeItem(self.polygons_pixmap_ref)
        self.polygons_pixmap_ref = QGraphicsPixmapItem(pixmap)
        self.view.scene.addItem(self.polygons_pixmap_ref)
        #print("Rysowanie na scenie")


    def handle_select_polygon(self,x,y):
        if self.selected_polygon == [[],[]]:
            poly = copy.deepcopy(self.select_polygon_on_click( x, y))
            self.selected_polygon = poly
            return

        near_active_polygon_point = False
        for point in self.selected_polygon[0]:
            distance = np.linalg.norm(np.array([x, y]) - np.array(point))
            if distance <= self.point_radius:
                near_active_polygon_point = True  # Punkt jest blisko wierzchołka

        if near_active_polygon_point:
            pass
        else:
            poly = copy.deepcopy(self.select_polygon_on_click(x, y))
            self.selected_polygon = poly


    # Funkcja która po zwraca tablice wierzchołków poligona po kliknięciu w jego obszar
    def select_polygon_on_click(self,x,y):
        selected_polygon = None
        for poly in self.polygons:
            result = self.check_inclusion(poly[0],x,y)
            if result:
                selected_polygon = poly
                break
        if selected_polygon is None:
            selected_polygon = [[],[]]
        return selected_polygon

        #print("Wybrany polygon to:",self.selected_polygon)


    def active_dragging(self,x,y):
        # for i in self.polygons:
        #     print(i)
        if self.selected_polygon != [[],[]]:        # Sprawdź czy jest zaznaczony jakiś polygon
            polygon_points = self.selected_polygon
            for idx, polygon_point in enumerate(polygon_points[0]):
                distance = np.linalg.norm(np.array([x, y]) - np.array(polygon_point))
                if distance < (self.point_radius + 3):                  # point_radius powiększone o 3
                    self.selected_vertex = (polygon_points[0], idx)     # aby łatwiej było chwytać
                    self.is_dragging = True
                    #self.polygons.remove(polygon_points)
                    break
        #print("aktualne poligony po kliknięciem")
        print("aktualne poligony kiedy kliknięto kliknięciem")
        for i in self.polygons:
            print(i)

    def dragging_move(self,x,y):
        if self.is_dragging and self.selected_vertex:
            # Przesuwanie wybranego wierzchołka
            polygon_points, idx = self.selected_vertex[0] ,self.selected_vertex[1]
            polygon_points[idx] = (x, y)
            # print("polygon_points")
            # print(polygon_points)
            self.draw_annotations()  # Aktualizacja obrazu po przesunięciu wierzchołka

    def release_dragging_click(self):
        if self.selected_vertex is not None:
            print("aktualne poligony")
            for i in self.polygons:
                print(i)
            print("puszczenie LP myszy")

        #print(self.selected_polygon)
        if self.is_dragging: # jeśli wierzchołek był przesuwany
            self.save_edited_annotations()
            self.presenter.annotation_presenter.updateItems() # Odświeżenie listy adnotacji
            self.draw_annotations()
        self.is_dragging = False
        self.selected_vertex = None


    def save_edited_annotations(self):
        for polygon in self.polygons:
            new_points, new_color = polygon  # Wierzchołki i kolor z listy self.polygons

            # Szukamy adnotacji, która najlepiej pasuje do obecnego polygonu
            best_match = None
            min_difference = float('inf')

            for annotation in self.annotations:
                current_points = annotation.get_segmentation()

                # Liczymy różnicę w liczbie i położeniu wierzchołków
                difference = len(set(new_points).symmetric_difference(set(current_points)))

                # Aktualizacja, jeśli różnica jest najmniejsza
                if difference < min_difference:
                    min_difference = difference
                    best_match = annotation

            # Aktualizujemy wierzchołki w najlepiej dopasowanym obiekcie adnotacji
            if best_match:
                best_match.set_segmentation(new_points)
        self.project.uppdate_annotation_by_image_object(self.active_image_model, self.annotations)
        print("ok")

    def reset_annotations(self):
        self.selected_polygon = [[],[]]
        self.annotations = []
        self.polygons = []

    def refresh(self):
        self.reset_annotations()
        self.get_annotations_from_project()
        self.draw_annotations()

    def reset_to_default(self):
        self.polygons_pixmap_ref = None
        self.reset_annotations()
        self.get_annotations_from_project()
        self.draw_annotations()

    def reset_selected_polygon(self):
        self.selected_polygon = [[],[]]

    def check_inclusion(self,polygon,x,y):
        np_points = np.array(polygon, dtype=np.int32)

        # Sprawdzenie, czy punkt znajduje się wewnątrz wielokąta
        result = cv2.pointPolygonTest(np_points, (x, y), False)

        if result >= 0:
            return True  # Punkt jest wewnątrz lub na krawędzi wielokąta

        # Sprawdzenie, czy punkt jest w pobliżu któregokolwiek wierzchołka
        for point in polygon:
            distance = np.linalg.norm(np.array([x, y]) - np.array(point))
            if distance <= (self.point_radius + 3):                               # point_radius powiększone o 3
                return True  # Punkt jest blisko wierzchołka

        return False

    def get_seleted_polygon(self):
        polygon = self.selected_polygon[0]
        return polygon

    def set_seleted_polygon(self,poly):
        for p in self.polygons:
            if p[0] == poly:
                self.selected_polygon = p

