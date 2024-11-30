import os
import json
import shutil

from PyQt5.QtWidgets import QFileDialog, QMessageBox

class ExportToFile:
    def __init__(self, view, project):
        self.view = view
        self.json_path = None
        self.project= project

    def select_save_location_and_create_folder(self):
        # Otwórz okno dialogowe do wyboru lokalizacji i nazwy pliku
        self.json_path, _ = QFileDialog.getSaveFileName(self.view.centralwidget.parent(), "Wybierz plik JSON", "",
                                                        "JSON Files (*.json);")
        return self.json_path

    def create_folder_structure(self, path):
        # Wyodrębniamy ścieżkę folderu i nazwę pliku z wybranej ścieżki pliku
        folder_path = os.path.dirname(path)
        file_name = os.path.basename(path).replace(".json",
                                                   "")  # Usuwamy rozszerzenie '.json', aby uzyskać nazwę folderu

        # Tworzymy nowy folder o tej samej nazwie co plik (bez rozszerzenia)
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

        # Tworzymy plik JSON z pustym obiektem, jeśli nie istnieje
        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w') as json_file:
                json.dump({}, json_file)  # Inicjujemy pustym obiektem JSON

        return json_file_path

    def export_images(self, folder_path):
        # Usuwamy rozszerzenie .json z folder_path, aby wskazywało na folder
        folder_path = os.path.splitext(folder_path)[0]
        images_folder = os.path.join(folder_path, 'images')
        print(images_folder)

        if not os.path.exists(images_folder):
            os.makedirs(images_folder)  # Tworzymy folder 'images', jeśli nie istnieje

        # Iterujemy po obrazkach
        for img_obj in self.project.list_of_images_model:
            source_path = img_obj.filename
            print(str(source_path))
            destination_path = os.path.join(images_folder, os.path.basename(source_path))

            try:
                shutil.copy(source_path, destination_path)
                self.view.file_list_widget.addItem(os.path.basename(source_path))
            except Exception as e:
                self.view.show_message("Błąd", f"Nie udało się skopiować obrazu {img_obj.filename}: {str(e)}")



