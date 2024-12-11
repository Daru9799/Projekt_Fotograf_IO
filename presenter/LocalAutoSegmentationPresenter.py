from ultralytics import SAM
import torch

class LocalAutoSegmentationPresenter:
    def __init__(self, view, presenter):
        self.view = view
        self.presenter = presenter
        #self.active_model = SAM("sam2.1_b.pt")
        self.active_model = SAM("sam2.1_l.pt")
        self.image_path = ""

        print("PyTorch version:", torch.__version__)
        print("CUDA version:", torch.version.cuda)
        print("CUDA available:", torch.cuda.is_available())
        print("Devices:", torch.cuda.device_count())
        if torch.cuda.is_available():
            print("GPU:", torch.cuda.get_device_name(0))

        # Wybierz urządzenie: GPU lub CPU
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print("Using device:", self.device)

        # Inicjalizacja modelu na wybranym urządzeniu
        self.active_model = SAM("sam2.1_b.pt").to(self.device)

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

    def calculate_vertexes(self, path, points_list):
        new_bbox = self.rectangle_to_bbox(points_list)
        print("new_bbox: ", new_bbox)

        # Wyliczenie granic bbox
        x_min, y_min, width, height = new_bbox
        x_max = x_min + width
        y_max = y_min + height

        # Wywołanie modelu
        result = list(self.active_model(path, bboxes=[new_bbox]))
        xy_list = result[0].masks.xy[0]  # Zakładamy, że mamy jedno wykrycie

        # Konwersja punktów na int i ograniczenie do bbox
        formatted_xy = [
            self.clamp_to_bbox((int(point[0]), int(point[1])), x_min, y_min, x_max, y_max)
            for point in xy_list
        ]
        print("Clamped Polygon Points: ", formatted_xy)


        # result = self.active_model.predict(path, bboxes=[new_bbox])
        #
        # for r in result:
        #     print(f"Detected {len(r.masks)} masks")

        return formatted_xy

    def clamp_to_bbox(self, point, x_min, y_min, x_max, y_max):
        """Ogranicz punkt (x, y) do granic bbox."""
        x = max(x_min, min(point[0], x_max))  # Ogranicz x do [x_min, x_max]
        y = max(y_min, min(point[1], y_max))  # Ogranicz y do [y_min, y_max]
        return (x, y)