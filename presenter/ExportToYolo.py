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
        # Dodanie nazwy pliku data.yaml do podanej ścieżki folderu
        output_path = os.path.join(folder_path, "data.yaml")

        # Pobranie nazw klas z listy klas w projekcie
        class_names = [cl.name for cl in self.project.list_of_classes_model]

        # Konfiguracja danych
        data = {
            "names": class_names,  # Nazwy klas
            "nc": len(class_names),  # Liczba klas
            "train": os.path.join(folder_path, 'train', 'images'),  # Ścieżka do folderu train/images
            "val": os.path.join(folder_path, 'valid', 'images'),  # Ścieżka do folderu valid/images
            "test": "../test/images"  # Ścieżka do folderu test/images 
        }

        try:
            # Tworzymy foldery, jeśli nie istnieją
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Zapisujemy dane do pliku YAML
            with open(output_path, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(data, yaml_file, allow_unicode=True, default_flow_style=False)

            print(f"Plik YAML został utworzony: {output_path}")
        except Exception as e:
            print(f"Błąd podczas tworzenia pliku YAML: {str(e)}")





