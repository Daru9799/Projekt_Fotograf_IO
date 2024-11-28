# from poligony import polygons
from PyQt5.QtCore import QObject
import cv2
import numpy as np
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap

class ScenePresenter:
    def __init__(self, view, presenter, project):
        self.view = view
        self.presenter = presenter
        self.project = project

        self.annotations = [] #lista adnotacji
        self.polygons = [] #przechowuje liste dwuelementową (punkty, kolor): [[(x,y), (x,y), ...], RGB]
        self.active_image_model = None
        self.point_radius = 5  # Promień kółek dla wierzchołków
        self.polygons_pixmap_ref = None
        self.selected_polygon = [[],[]]

    # pobiera listę "annotations" obrazu i na jej podstawie generuje liste "polygons"
    def get_annotations_from_project(self):
        image = self.presenter.image_item
        self.active_image_model = self.project.get_img_by_filename(image.text())
        self.annotations = self.active_image_model.get_annotation_list()
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
                #Wypełnianie polygona kolorem:
                #if self.selected_polygon is not None:
                if poly[0] == self.selected_polygon[0]:
                    fill_color = (poly[1][0], poly[1][1], poly[1][2], 120)
                    cv2.fillPoly(drawing_surface, [np_points], color=fill_color)
                    for point in np_points:
                        cv2.circle(drawing_surface, tuple(point[0]), self.point_radius, border_color, -1)

                else:
                    fill_color = (poly[1][0], poly[1][1], poly[1][2], 160)
                    cv2.fillPoly(drawing_surface, [np_points], color=fill_color)

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


    def save_annotations(self):
        # zapisz do listy annotation_objects wszystkie adnotacje z listy adnotacji obrazka (obiekty)
        pass

    # Funkcja która po klinięciu na polygon ustawia go jako aktywny/selected
    def select_polygon_on_click(self,x,y):
        selected_polygon = None
        for poly in self.polygons:
            result = self.check_inclusion(poly[0],x,y)
            if result >= 0:
                selected_polygon = poly
                break
        if selected_polygon is not None:
            self.selected_polygon = selected_polygon
        else:
            self.selected_polygon = [[],[]]
        print("Wybrany polygon to:",self.selected_polygon)



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
        #np_points = np_points.reshape((-1, 1, 2))
        result = cv2.pointPolygonTest(np_points, (x,y), False)
        return result

    def get_seleted_polygon(self):
        polygon = self.selected_polygon[0]
        return polygon

    def set_seleted_polygon(self,poly):
        for p in self.polygons:
            if p[0] == poly:
                self.selected_polygon = p;