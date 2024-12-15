import os
import shutil
import yaml
from PyQt5.QtWidgets import QFileDialog

class ExportToYolo:
    def __init__(self, view, project):
        self.view = view
        self.path = None
        self.project = project

    def select_save_location(self):
        # Otwórz okno dialogowe do wyboru lokalizacji i nazwy pliku
        self.path, _ = QFileDialog.getSaveFileName(
            self.view.centralwidget.parent(), "Wybierz lokalizację do zapisu", "",""
        )
        return self.path

    def create_folder_structure(self, path):
        # Wyodrębniamy ścieżkę folderu i nazwę pliku z wybranej ścieżki
        folder_path = os.path.dirname(path)
        folder_name = os.path.basename(path).replace(".yaml", "")  # Usuwamy rozszerzenie '.yaml'

        # Tworzymy główny folder
        new_folder_path = os.path.join(folder_path, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # Tworzymy podfoldery 'train' i 'valid'
        train_folder = os.path.join(new_folder_path, 'train')
        valid_folder = os.path.join(new_folder_path, 'valid')

        os.makedirs(train_folder, exist_ok=True)
        os.makedirs(valid_folder, exist_ok=True)

        # Tworzymy podfoldery 'images' i 'labels' w 'train' oraz 'valid'
        for subfolder in [train_folder, valid_folder]:
            images_folder = os.path.join(subfolder, 'images')
            labels_folder = os.path.join(subfolder, 'labels')
            os.makedirs(images_folder, exist_ok=True)
            os.makedirs(labels_folder, exist_ok=True)


    def export_images(self, folder_path):
        # Tworzymy ścieżkę do folderu 'train/images'
        images_folder = os.path.join(folder_path, 'train', 'images')
        os.makedirs(images_folder, exist_ok=True)  # Tworzymy folder, jeśli nie istnieje

        for img_obj in self.project.list_of_images_model:
            # Sprawdzamy, czy obraz ma przypisane adnotacje
            if not img_obj.list_of_annotations:
                continue

            source_path = self.project.get_full_path_by_filename(img_obj.filename)

            if not source_path:
                self.view.show_message("Błąd", f"Nie znaleziono ścieżki dla pliku: {img_obj.filename}")
                continue

            destination_path = os.path.join(images_folder, os.path.basename(source_path))

            try:
                shutil.copy(source_path, destination_path)
                # Dodajemy plik do widoku
                self.view.file_list_widget.addItem(os.path.basename(source_path))
            except Exception as e:
                self.view.show_message("Błąd", f"Nie udało się skopiować obrazu {img_obj.filename}: {str(e)}")


    def create_yaml_file(self, folder_path):
        # Tworzenie pełnej ścieżki do pliku data.yaml
        yaml_output_path = os.path.join(folder_path, "data.yaml")

        # Pobranie nazw klas z listy klas w projekcie
        class_names = [cl.name for cl in self.project.list_of_classes_model]

        # Konfiguracja danych YAML
        yaml_data = {
            "names": class_names,
            "nc": len(class_names),  # Liczba klas
            "train": os.path.join(folder_path, 'train', 'images'),  # Ścieżka do folderu train/images
            "val": os.path.join(folder_path, 'valid', 'images'),  # Ścieżka do folderu valid/images
            "test": "../test/images"  # Ścieżka do folderu test/images
        }

        try:
            # Tworzenie wymaganych folderów
            labels_folder = os.path.join(folder_path, "train", "labels")
            os.makedirs(labels_folder, exist_ok=True)

            # Tworzenie pliku YAML
            with open(yaml_output_path, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(yaml_data, yaml_file, allow_unicode=True, default_flow_style=False)
            print(f"Plik YAML został utworzony: {yaml_output_path}")

            # Tworzenie plików tekstowych dla YOLO
            for img in self.project.list_of_images_model:
                print(f"Przetwarzanie obrazu: {img.filename}")  # Debug: wydruk nazwy obrazu

                # Ścieżka pliku tekstowego
                label_file_path = os.path.join(labels_folder, f"{os.path.splitext(img.filename)[0]}.txt")

                if not img.list_of_annotations:
                    print(f"Brak adnotacji dla obrazu: {img.filename}")  # Debug: brak adnotacji
                    continue

                with open(label_file_path, 'w', encoding='utf-8') as label_file:
                    for an in img.list_of_annotations:
                        if hasattr(an, 'segmentation') and an.segmentation:  # Sprawdzanie, czy adnotacja ma segmentację
                            # YOLO format: class_id x1 y1 x2 y2 ... (dla segmentacji)
                            segmentation_flat = [coord for point in an.segmentation for coord in point]
                            normalized_segmentation = [
                                coord / img.width if i % 2 == 0 else coord / img.height
                                for i, coord in enumerate(segmentation_flat)
                            ]
                            label_line = f"{an.class_id} " + " ".join(
                                f"{value:.6f}" for value in normalized_segmentation) + "\n"
                            label_file.write(label_line)
                        elif hasattr(an, 'bbox') and an.bbox:  # Sprawdzanie, czy adnotacja ma bbox
                            # YOLO format: class_id center_x center_y width height
                            x, y, w, h = an.bbox
                            center_x = (x + w / 2) / img.width
                            center_y = (y + h / 2) / img.height
                            width = w / img.width
                            height = h / img.height
                            label_line = f"{an.class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n"
                            label_file.write(label_line)

                print(f"Plik etykiet został utworzony: {label_file_path}")

        except Exception as e:
            print(f"Błąd podczas tworzenia plików: {str(e)}")



