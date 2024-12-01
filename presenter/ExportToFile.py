import os
import json
import shutil
from PyQt5.QtWidgets import QFileDialog

class ExportToFile:
    def __init__(self, view, project):
        self.view = view
        self.json_path = None
        self.project = project

    def select_save_location_and_create_folder(self):
        # Otwórz okno dialogowe do wyboru lokalizacji i nazwy pliku
        self.json_path, _ = QFileDialog.getSaveFileName(
            self.view.centralwidget.parent(), "Wybierz plik JSON", "",
            "JSON Files (*.json);"
        )
        return self.json_path

    def create_folder_structure(self, path):
        # Wyodrębniamy ścieżkę folderu i nazwę pliku z wybranej ścieżki pliku
        folder_path = os.path.dirname(path)
        file_name = os.path.basename(path).replace(".json", "")  # Usuwamy rozszerzenie '.json'

        new_folder_path = os.path.join(folder_path, file_name)

        # Sprawdzamy, czy folder istnieje; jeśli nie, tworzymy go
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # Tworzymy podfolder 'images' w nowo utworzonym folderze
        images_folder = os.path.join(new_folder_path, 'images')
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        # Tworzymy pusty plik JSON w nowo utworzonym folderze
        json_file_path = os.path.join(new_folder_path, file_name + '.json')

        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w') as json_file:
                json.dump({}, json_file)  # Inicjujemy pustym obiektem JSON

        return json_file_path

    def export_images(self, folder_path):
        images_folder = os.path.join(folder_path, 'images')
        os.makedirs(images_folder, exist_ok=True)  # Tworzymy folder 'images', jeśli nie istnieje

        for img_obj in self.project.list_of_images_model:
            source_path = self.project.get_full_path_by_filename(img_obj.filename)

            if not source_path:
                self.view.show_message("Błąd", f"Nie znaleziono ścieżki dla pliku: {img_obj.filename}")
                continue

            destination_path = os.path.join(images_folder, os.path.basename(source_path))

            try:
                shutil.copy(source_path, destination_path)
                self.view.file_list_widget.addItem(os.path.basename(source_path))  # Dodajemy plik do widoku
            except Exception as e:
                self.view.show_message("Błąd", f"Nie udało się skopiować obrazu {img_obj.filename}: {str(e)}")

    def create_json_file(self, output_path):
        # Przygotowanie danych JSON
        selected_image_name = self.view.get_selected_image()
        img_obj = self.project.get_img_by_filename(selected_image_name)
        annotation_list=img_obj.list_of_annotations

        images = [
            {
                "file_name": img.filename,
                "height": img.height,
                "width": img.width,
                "id": img.image_id
            } for img in self.project.list_of_images_model
        ]

        categories = [
            {
                "id": cl.class_id,
                "name": cl.name
            } for cl in self.project.list_of_classes_model
        ]
        annotations=[
            {
                "annotation_id":an.annotation_id,
                "class_id":an.class_id,
                "segmentatiob":an.segmentation

            }for an in annotation_list
        ]

        data = {
            "images": images,
            "categories": categories,
            "annotations": annotations
        }

        try:
            # Tworzymy foldery, jeśli nie istnieją
            folder_path = os.path.dirname(output_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Zapisujemy dane do pliku JSON
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Plik JSON został utworzony: {output_path}")
        except Exception as e:
            print(f"Błąd podczas tworzenia pliku JSON: {str(e)}")
