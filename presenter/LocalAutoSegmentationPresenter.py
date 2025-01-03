from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from ultralytics import SAM
import torch
import cv2
import numpy as np
from numpy import asarray

from PIL import Image

from scipy.ndimage import median_filter

class LocalAutoSegmentationPresenter:
    def __init__(self, view, presenter):
        self.view = view
        self.presenter = presenter

        self.temp_segment = []
        self.temp_segment_ref = None
        self.score = 0.0

        self.color = (171, 127, 89, 255)

        #self.active_model = SAM("sam2_s.pt")
        #self.active_model = SAM("sam2.1_l.pt")

        print("PyTorch version:", torch.__version__)
        print("CUDA version:", torch.version.cuda)
        print("CUDA available:", torch.cuda.is_available())
        print("Devices:", torch.cuda.device_count())
        if torch.cuda.is_available():
            print("GPU:", torch.cuda.get_device_name(0))

        # Wybierz urządzenie: GPU lub CPU
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #print("Using device:", self.device)

        # Inicjalizacja modelu na wybranym urządzeniu
        self.active_model = SAM("sam2_s.pt").to(self.device)

    def rectangle_to_bbox(self,points):
        # Rozdzielenie współrzędnych x i y
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]

        # Wyznaczenie minimalnych i maksymalnych wartości
        min_x = min(x_coords)
        min_y = min(y_coords)
        max_x = max(x_coords)
        max_y = max(y_coords)

        return min_x, min_y, max_x, max_y

    def calculate_vertexes(self, path, points_list):

        # Wywołanie modelu
        # visualize=True,show=True
        bbox = self.rectangle_to_bbox(points_list)
        results = self.active_model.predict(source=path, bboxes=[bbox], conf=0.6)

        # Pobranie maski
        mask = results[0].masks.data[0].cpu().numpy()
        # Pobranie punktacji maski (0.0 - 1.0)
        self.score = float(results[0].boxes.conf[0])
        contours = self.mask_to_polygon(mask)

        # Jeśli kontury są puste, zwróć pustą listę
        if not contours:
            self.temp_segment = []
            self.view.set_notification_label(f"Automatyczne zaznaczanie: Wybierz punkt początkowy LPM.")

        else:
            # Zmniejsz liczbę punktów konturu
            simplified_contours = self.simplify_polygon(contours[0], epsilon=2.0)

            # Wygładź kontury
            smoothed_contours = self.smooth_polygon(simplified_contours, size=3)

            self.temp_segment = smoothed_contours

            self.view.set_notification_label(f"Automatyczne zaznaczanie: Potwierdź wygenerowane zaznaczenie - 'Enter'")

        self.draw_temp_segment()

    def draw_temp_segment(self):
        #print("--- Lista aktualnych punktów polygona: ---")
        #print( self.current_polygon_points)
        drawing_surface = np.zeros((self.view.pixmap_item.pixmap().height(), self.view.pixmap_item.pixmap().width(), 4),dtype=np.uint8)
        #drawing_surface[:, :, 3] = 255
        #border_color = (abs(self.color[0] - 50), abs(self.color[1] - 50), abs(self.color[2] - 50))
        if len(self.temp_segment) != 0:

            # konwersja listy punktów((x,y)) -> np.array, dla poprawnego rysowania cv2
            np_points = np.array(self.temp_segment, dtype=np.int32)
            np_points = np_points.reshape((-1, 1, 2))

            cv2.polylines(drawing_surface, [np_points], isClosed=True, thickness=2, color=self.color )

            # for point in np_points:
            #     cv2.circle(drawing_surface, tuple(point[0]), self.point_radius, self.color, -1)

            fill_color = (self.color[0], self.color[1], self.color[2], 220)
            cv2.fillPoly(drawing_surface, [np_points], color=fill_color)

            #self.add_text_to_segment(drawing_surface, np_points, f"Temp({self.score:.2f})")


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
        self.view.scene.removeItem(self.temp_segment_ref)
        self.temp_segment_ref  = QGraphicsPixmapItem(pixmap)
        self.view.scene.addItem(self.temp_segment_ref)

    # def calculate_vertexes_cropped(self,path,points_list):
    #     new_bbox = self.rectangle_to_bbox(points_list)
    #     print("new_bbox: ", new_bbox)
    #
    #     # Wywołanie modelu
    #     # visualize=True,show=True
    #     img = Image.open(path)
    #     img.load()
    #     print(img.mode)
    #     if img.mode != "RGB":
    #         img = img.convert("RGB")
    #     np_img = np.asarray( img, dtype="uint8" )
    #     cropped_image = self.crop_image(np_img,new_bbox)
    #     #cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
    #     results = self.active_model.predict(source=cropped_image, conf=0.6,visualize=True,show=True)
    #
    #     # Jeśli nic nie wykryje
    #     if not results[0].masks:
    #         return []
    #     # Pobranie maski
    #     mask = results[0].masks.data[0].cpu().numpy()
    #     contours = self.mask_to_polygon(mask)
    #
    #     # Jeśli kontury są puste, zwróć pustą listę
    #     if not contours:
    #         return []
    #
    #     x_offset, y_offset = new_bbox[0], new_bbox[1]
    #
    #     scaled_contours = []
    #     for contour in contours:
    #         scaled_contour = [(x + x_offset, y + y_offset) for x, y in contour]
    #         scaled_contours.append(scaled_contour)
    #
    #     # Zmniejsz liczbę punktów konturu (upraszczanie)
    #     simplified_contours = [
    #         self.simplify_polygon(scaled_contour, epsilon=2.0)
    #         for scaled_contour in scaled_contours
    #     ]
    #
    #     # Wygładź kontury
    #     smoothed_contours = [
    #         self.smooth_polygon(simplified_contour, size=3)
    #         for simplified_contour in simplified_contours
    #     ]
    #
    #     # # Posortuj kontury według obszaru w kolejności malejącej
    #     # smoothed_contours_sorted = sorted(
    #     #     smoothed_contours,
    #     #     key=lambda contour: cv2.contourArea(np.array(contour, dtype=np.int32)),
    #     #     reverse=True
    #     # )
    #
    #     return smoothed_contours


    # Kod/Metoda narazie nie wykorzystywana:
    def calculate_vertexes_cropped(self, path, points_list):
        new_bbox = self.rectangle_to_bbox(points_list)
        print("new_bbox: ", new_bbox)

        # Wczytanie obrazu
        img = Image.open(path)
        img.load()
        print(img.mode)
        if img.mode != "RGB":
            img = img.convert("RGB")
        np_img = np.asarray(img, dtype="uint8")

        # Przycięcie obrazu
        cropped_image = self.crop_image(np_img, new_bbox)
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)

        # Wywołanie modelu
        results = self.active_model.predict(source=cropped_image, conf=0.6, visualize=True, show=True)

        # Jeśli nic nie wykryje
        if not results[0].masks:
            return []

        # Pobranie masek
        masks = results[0].masks.data.cpu().numpy()

        # Znalezienie środka obrazu
        center_x = cropped_image.shape[1] // 2
        center_y = cropped_image.shape[0] // 2

        # Zwracanie tylko maski obejmującej środek obrazu
        selected_mask = None
        for mask in masks:
            if mask[center_y, center_x] > 0:  # Sprawdzenie, czy środek obrazu leży w masce
                selected_mask = mask
                break

        # Jeśli żadna maska nie zawiera środka, zwróć pustą listę
        if selected_mask is None:
            return []

        # Konwersja maski na kontur
        contours = self.mask_to_polygon(selected_mask)

        # Jeśli kontury są puste, zwróć pustą listę
        if not contours:
            return []

        x_offset, y_offset = new_bbox[0], new_bbox[1]

        scaled_contours = []
        for contour in contours:
            scaled_contour = [(x + x_offset, y + y_offset) for x, y in contour]
            scaled_contours.append(scaled_contour)

        # Zmniejsz liczbę punktów konturu (upraszczanie)
        simplified_contours = [
            self.simplify_polygon(scaled_contour, epsilon=2.0)
            for scaled_contour in scaled_contours
        ]

        # Wygładź kontury
        smoothed_contours = [
            self.smooth_polygon(simplified_contour, size=3)
            for simplified_contour in simplified_contours
        ]

        return smoothed_contours

    def mask_to_polygon(self, mask):
        contours, _ = cv2.findContours((mask > 0).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        polygons = []
        for contour in contours:
            if cv2.contourArea(contour) > 10:
                # Konwersja konturu na listę krotek (x, y)
                polygon = [tuple(point[0]) for point in contour]
                if len(polygon) >= 6:  # Minimalna liczba punktów to 3 (żeby utworzyć wielokąt)
                    polygons.append(polygon)
        print(f"Generated {len(polygons)} valid polygons")
        polygons.sort(key=len, reverse=True)
        return polygons

    def smooth_polygon(self, polygon, size=3):
        """
        Apply median filter to smooth the polygon points and reduce noise.

        :param polygon: List of points [(x1, y1), (x2, y2), ...]
        :param size: Size of the median filter.
        :return: Smoothed polygon.
        """
        # Rozdzielenie na współrzędne X i Y
        x_coords = [point[0] for point in polygon]
        y_coords = [point[1] for point in polygon]

        # Zastosowanie filtru medianowego
        smoothed_x = median_filter(x_coords, size=size)
        smoothed_y = median_filter(y_coords, size=size)

        # Połączenie wygładzonych współrzędnych
        smoothed_polygon = list(zip(smoothed_x, smoothed_y))

        return smoothed_polygon

    def simplify_polygon(self, polygon, epsilon=2.0):
        """
        Simplifies the polygon using the Douglas-Peucker algorithm.

        :param polygon: List of points [(x1, y1), (x2, y2), ...]
        :param epsilon: The distance threshold to simplify the polygon.
                        Larger values result in fewer points.
        :return: Simplified polygon.
        """
        # Convert polygon to NumPy array
        polygon_np = np.array(polygon, dtype=np.int32)

        # Apply the Douglas-Peucker algorithm (cv2.approxPolyDP)
        epsilon = epsilon  # Adjust epsilon to control simplification
        simplified_polygon = cv2.approxPolyDP(polygon_np, epsilon, True)

        # Convert back to list of tuples
        simplified_polygon = [tuple(point[0]) for point in simplified_polygon]

        return simplified_polygon

    def crop_image(self,image, bbox):
        x, y, width, height = bbox
        x_min, x_max = x, x + width
        y_min, y_max = y, y + height
        return image[y_min:y_max, x_min:x_max]

    def cancel_auto_segmentation(self):
        self.view.set_auto_selection_button_text("Automatyczne zaznaczanie")
        self.remove_temp_segment()

    def remove_temp_segment(self):
        self.view.scene.removeItem(self.temp_segment_ref)
        self.temp_segment_ref = None
        self.temp_segment = []

    def add_text_to_segment(self,drawing_surface, np_points, text):
        # Obliczanie środka ciężkości polygona (centroid)
        M = cv2.moments(np_points)
        if M["m00"] != 0:
            centroid_x = int(M["m10"] / M["m00"])
            centroid_y = int(M["m01"] / M["m00"])
        else:
            # W przypadku gdy pole wynosi 0 (np. linia), użyj średniej punktów
            centroid_x = int(np.mean(np_points[:, 0, 0]))
            centroid_y = int(np.mean(np_points[:, 0, 1]))

        # Obliczanie pola powierzchni polygona
        area = cv2.contourArea(np_points)

        # Dynamiczne skalowanie rozmiaru czcionki na podstawie pola powierzchni
        # Ustal minimalny i maksymalny rozmiar czcionki
        min_font_size = 0.5
        max_font_size = 1.5
        base_area = 2500  # Obszar bazowy dla czcionki minimalnej
        font_scale = max(min_font_size, min(max_font_size, area / base_area))

        print("Area:", (area/base_area))
        print("Font scale:", font_scale)

        # Dodawanie napisu na środku
        font = cv2.FONT_HERSHEY_SIMPLEX
        #font_scale = 0.3
        font_color = (69, 50, 34, 200)  # Biały kolor
        thickness = 2

        cv2.putText(
            drawing_surface,
            text,
            (centroid_x - 60, centroid_y + 10),  # Ustawienie pozycji tekstu
            font,
            font_scale,
            font_color,
            thickness
        )

    def comboBox_sam_model_change(self):
        curent_idx = self.view.comboBox_sam_model.currentIndex()
        if curent_idx == 0:
            self.active_model = SAM("sam2_s.pt").to(self.device)
        elif curent_idx == 1:
            self.active_model = SAM("sam2_b.pt").to(self.device)
        elif curent_idx == 2:
            self.active_model = SAM("sam2_l.pt").to(self.device)
        #print(self.active_model)



