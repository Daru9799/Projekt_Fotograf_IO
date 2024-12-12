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
        self.point_radius = 4  # Promień kółek dla wierzchołków [px]
        self.point_dst_multiplier = 2 # musi być int
        self.expand_dst = 5 # [px]
        self.polygons_pixmap_ref = None
        self.selected_polygon = [[],[]]
        self.vertex_expand_dst = int((self.point_radius*self.point_dst_multiplier) + 5)

        self.is_dragging = False
        self.selected_vertex = None

    # pobiera listę "annotations" obrazu i na jej podstawie generuje liste "polygons"
    def get_annotations_from_project(self):
        image = self.presenter.image_item
        self.active_image_model = self.project.get_img_by_filename(image.text())
        self.annotations = self.active_image_model.get_annotation_list()
        self.polygons = []  # Czyszczenie polygonów

        # Pobranie ID ukrytych klas
        hidden_class_ids = {cl.class_id for cl in
                            self.presenter.classManagerPresenter.getHiddenClass()}  # Zbiór ID ukrytych klas
        print("Ukryte klasy (IDs):", hidden_class_ids)

        # Dodanie poligonów tylko dla widocznych klas
        for obj in self.annotations:
            if obj.class_id not in hidden_class_ids:  # Sprawdzanie, czy klasa nie jest ukryta
                points_list = obj.get_segmentation()
                color = self.project.get_color_by_class_id(obj.class_id)
                self.polygons.append([points_list, color])

    # na podstawie listy polygons narysuj poligony
    def draw_annotations(self):
        # na podstawie listy polygons narysuj poligony i dodaj kazdego z nich do listy referencji polygons_item
        drawing_surface = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4), dtype=np.uint8)
        if self.active_image_model.has_annotation:
            for poly in self.polygons:
                np_points = np.array(poly[0], dtype=np.int32)
                np_points = np_points.reshape((-1, 1, 2))

                # do testy:
                # <------------------------------
                # centroid = np.mean(np_points, axis=0)
                #
                # # Obliczenie wektorów normalnych i przesunięcie wierzchołków
                # expansion_distance = self.expand_dst  # Powiększenie o 10 piksele
                # expanded_polygon = []
                # for point in np_points:
                #     # Wektor od środka ciężkości do wierzchołka
                #     direction = point - centroid
                #     # Normalizacja wektora kierunku i przesunięcie
                #     normalized_direction = direction / (np.linalg.norm(direction) + 1e-6)
                #     expanded_point = point + normalized_direction * expansion_distance
                #     expanded_polygon.append(expanded_point)
                #
                # expanded_polygon = np.array(expanded_polygon, dtype=np.int32)
                # -------------------------->

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

                    # testowo -------------
                    # point_radius_tmp = self.vertex_expand_dst
                    # for point in np_points:
                    #     cv2.circle(drawing_surface, tuple(point[0]), point_radius_tmp, fill_color, -1)
                    # cv2.polylines(drawing_surface, [np_points], isClosed=True, thickness=2, color=border_color)
                    # ---------------------

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

        # Kod który sprawdza czy nie klikneliśmy obok wierzchołka zaznaczonego/aktywnego poligona
        near_active_polygon_point = False
        for point in self.selected_polygon[0]:
            distance = np.linalg.norm(np.array([x, y]) - np.array(point))
            if distance <= self.vertex_expand_dst:             # powiększenie point radius
                near_active_polygon_point = True  # Punkt jest blisko wierzchołka

        if near_active_polygon_point:   # jeśli klikneliśmy obok wierzchołka zaznaczonego/aktywnego poligona
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

    def is_near_edge(self, x, y, polygon):
        """Sprawdza, czy punkt (x, y) jest blisko krawędzi wielokąta."""
        for i in range(len(polygon)):
            p1 = np.array(polygon[i])
            p2 = np.array(polygon[(i + 1) % len(polygon)])  # Następny wierzchołek (zamknięcie pętli)
            edge_vec = p2 - p1
            point_vec = np.array([x, y]) - p1
            edge_length = np.linalg.norm(edge_vec)
            if edge_length == 0:
                continue
            projection_length = np.dot(point_vec, edge_vec) / edge_length
            if 0 <= projection_length <= edge_length:
                projection_point = p1 + projection_length * (edge_vec / edge_length)
                distance = np.linalg.norm(np.array([x, y]) - projection_point)
                if distance < self.point_radius * 2:  # Wartość progu dla kliknięcia
                    return i, tuple(projection_point)
        return None, None

    def active_dragging(self, x, y):
        old_selection = self.selected_polygon
        self.handle_select_polygon(x, y)

        if self.selected_polygon != [[], []]:  # Sprawdź czy jest zaznaczony jakiś poligon
            if self.selected_polygon == old_selection:  # Sprawdź czy to co kliknęliśmy nie było już zaznaczone
                polygon_points = self.selected_polygon
                closest_distance = float('inf')
                closest_vertex_idx = None

                # Znalezienie najbliższego wierzchołka
                for idx, polygon_point in enumerate(polygon_points[0]):
                    distance = np.linalg.norm(np.array([x, y]) - np.array(polygon_point))
                    if distance < self.vertex_expand_dst and distance < closest_distance:  # point_radius powiększone o 5
                        closest_distance = distance
                        closest_vertex_idx = idx

                if closest_vertex_idx is not None:
                    self.selected_vertex = (polygon_points[0], closest_vertex_idx)
                    self.is_dragging = True

                # Jeśli żaden wierzchołek nie został wybrany, sprawdzamy krawędzie
                if not self.is_dragging:
                    for polygon_points, color in self.polygons:
                        edge_index, new_vertex = self.is_near_edge(x, y, polygon_points)
                        if edge_index is not None:
                            polygon_points.insert(edge_index + 1, (int(new_vertex[0]), int(new_vertex[1])))
                            self.selected_polygon[0] = polygon_points
                            self.selected_vertex = (polygon_points, (edge_index + 1))
                            self.is_dragging = True
                            self.draw_annotations()
                            break
            else:
                pass

        if self.is_dragging:
            self.draw_annotations()

    def dragging_move(self,x,y):
        if self.is_dragging and self.selected_vertex:
            # Przesuwanie wybranego wierzchołka
            polygon_points, idx = self.selected_vertex[0] ,self.selected_vertex[1]
            polygon_points[idx] = (x, y)
            # print("*" * 20)
            # print("polygon_points")
            # print(polygon_points)
            # print("selected_polygon")
            # print(self.selected_polygon[0])
            # print("*"*20)
            self.draw_annotations()  # Aktualizacja obrazu po przesunięciu wierzchołka

    def release_dragging_click(self):
        # if self.selected_vertex is not None:
            # print("aktualne poligony")
            # for i in self.polygons:
            #     print(i)
            # print("puszczenie LP myszy")

        #print(self.selected_polygon)
        if self.is_dragging: # jeśli wierzchołek był przesuwany
            self.save_edited_annotations()
            self.presenter.annotation_presenter.update_items() # Odświeżenie listy adnotacji
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


    # Sorawdza czy punkt znajduje się w obrębie poligona
    # Wierzchołki jako większe punkty też się wliczają w obszar poligona
    def check_inclusion(self,polygon,x,y):
        np_points = np.array(polygon, dtype=np.int32)
        centroid = np.mean(np_points, axis=0)

        # Obliczenie wektorów normalnych i przesunięcie wierzchołków
        expansion_distance = self.expand_dst  # Powiększenie o 10 piksele
        expanded_polygon = []
        for point in np_points:
            # Wektor od środka ciężkości do wierzchołka
            direction = point - centroid
            # Normalizacja wektora kierunku i przesunięcie
            normalized_direction = direction / (np.linalg.norm(direction) + 1e-6)
            expanded_point = point + normalized_direction * expansion_distance
            expanded_polygon.append(expanded_point)

        expanded_polygon = np.array(expanded_polygon, dtype=np.int32)

        # Sprawdzenie, czy punkt znajduje się wewnątrz wielokąta
        result = cv2.pointPolygonTest(expanded_polygon, (x, y), False)

        if result >= 0:
            return True  # Punkt jest wewnątrz lub na krawędzi wielokąta

        # Sprawdzenie, czy punkt jest w pobliżu któregokolwiek wierzchołka
        for point in np_points:
            distance = np.linalg.norm(np.array([x, y]) - np.array(point))
            if distance <= self.vertex_expand_dst:            # point_radius powiększone
                return True  # Punkt jest blisko wierzchołka

        return False

    def get_seleted_polygon(self):
        polygon = self.selected_polygon[0]
        return polygon

    def set_seleted_polygon(self,poly):
        for p in self.polygons:
            if p[0] == poly:
                self.selected_polygon = p

