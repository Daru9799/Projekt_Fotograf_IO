from ultralytics import SAM
import torch



class LocalAutoSegmentationPresenter:
    def __init__(self, view, presenter):
        self.view = view
        self.presenter = presenter
        self.active_model = SAM("sam2.1_b.pt")

        #print(self.active_model.info())
        if torch.cuda.is_available():
            print(f"GPU jest dostępne: {torch.cuda.get_device_name(0)}")
        else:
            print("GPU nie jest dostępne. Upewnij się, że CUDA i sterowniki są poprawnie zainstalowane.")

    def rectangle_to_bbox(points):
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

        return x_min, y_min, width, height