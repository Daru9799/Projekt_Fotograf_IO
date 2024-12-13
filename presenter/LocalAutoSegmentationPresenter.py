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
        self.active_model = SAM("sam2_b.pt").to(self.device)

    def rectangle_to_bbox(self,points):
        # Ekstrakcja współrzędnych x i y
        x_coords = [point[0] for point in points]
        y_coords = [point[1] for point in points]

        # Obliczenie współrzędnych bbox
        x_min = min(x_coords)
        y_min = min(y_coords)
        x_max = max(x_coords)
        y_max = max(y_coords)

        # Obliczenie szerokości i wysokości
        width = x_max - x_min
        height = y_max - y_min

        return [x_min, y_min, width, height]

# Stary kod bez postprocsów, które wygładzają końcowego polygona
    # def calculate_vertexes(self, path, points_list,img_object):
    #     new_bbox = self.rectangle_to_bbox(points_list)
    #     print("new_bbox: ", new_bbox)
    #
    #     # Wyliczenie granic bbox
    #     x_min, y_min, width, height = new_bbox
    #     x_max = x_min + width
    #     y_max = y_min + height
    #
    #     #Pobranie rozmiarów obrazka
    #     #img_size = (img_object.height, img_object.width)
    #
    #     #Konwersja obrazu:
    #     img = Image.open(path)
    #     img.load()
    #     numpydata = np.asarray( img, dtype="uint8" )
    #
    #     # Wywołanie modelu
    #     results = self.active_model(source= numpydata, bboxes=[new_bbox], retina_masks=True,conf=0.6)
    #
    #     # Kod jeśli chcemy korzystać z maski binarnej {
    #     mask = results[0].masks.data[0].cpu().numpy()
    #     suma_mask = mask.sum() # testowo
    #     print(suma_mask)
    #
    #     countours = self.mask_to_polygon(mask)
    #
    #     # if countours == []:
    #     #     return []
    #     # return countours[]0
    #
    #     # }
    #
    #     xy_list = results[0].masks.xy[0]  # Zakładamy, że mamy jedno wykrycie
    #
    #     # Konwersja punktów na int i ograniczenie do bbox
    #     # formatted_xy = [
    #     #     self.clamp_to_bbox((int(point[0]), int(point[1])), x_min, y_min, x_max, y_max)
    #     #     for point in xy_list
    #     # ]
    #
    #     # zamiana punktów x,y na inty
    #     formatted_xy = [
    #         (int(point[0]), int(point[1]))
    #         for point in xy_list
    #     ]
    #
    #     #smoothed_points = median_filter(formatted_xy, size=3)
    #     print("Clamped Polygon Points: ", formatted_xy)
    #     # print("contur: ",countours[0])
    #
    #     # if countours == []:
    #     #     return []
    #
    #     #smooth_points = self.smooth_polygon(smoothed_points)
    #
    #     return formatted_xy

    def calculate_vertexes(self, path, points_list, img_object):
        new_bbox = self.rectangle_to_bbox(points_list)
        print("new_bbox: ", new_bbox)

        # Wywołanie modelu
        # visualize=True,show=True
        results = self.active_model(source=path, bboxes=[new_bbox], conf=0.6)

        # Pobranie maski
        mask = results[0].masks.data[0].cpu().numpy()
        contours = self.mask_to_polygon(mask)

        # Jeśli kontury są puste, zwróć pustą listę
        if not contours:
            return []

        # Zmniejsz liczbę punktów konturu
        simplified_contours = self.simplify_polygon(contours[0], epsilon=2.0)

        # Wygładź kontury
        smoothed_contours = self.smooth_polygon(simplified_contours, size=3)

        # print("Smoothed Polygon Points: ", smoothed_contours)

        return smoothed_contours
        # return contours[0]
    # funkcja która m ograniczyć punkty do obszaru zaznaczonego bboxa
    def clamp_to_bbox(self, point, x_min, y_min, x_max, y_max):
        """Ogranicz punkt (x, y) do granic bbox."""
        x = max(x_min, min(point[0], x_max))  # Ogranicz x do [x_min, x_max]
        y = max(y_min, min(point[1], y_max))  # Ogranicz y do [y_min, y_max]
        return (x, y)

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