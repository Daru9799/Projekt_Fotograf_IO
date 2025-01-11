import os
import json
import platform
import threading
import time
from PyQt5.QtWidgets import QFileDialog

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl

class ExportProject:
    def __init__(self, view, project):
        self.view = view
        self.project_path = None
        self.project = project
        self.file_lock = None
        self.watch_thread = None
        self.stop_watching = False

    def select_save_location(self):
        self.project_path, _ = QFileDialog.getSaveFileName(
            self.view.centralwidget.parent(), "Wybierz lokalizację do zapisu", "",
            "Pliki Project (*.pro);;"
        )
        return self.project_path

    def create_file(self, output_path):
        annotations = []
        images = []
        categories = []

        # Populate data if present
        if self.project.list_of_images_model:
            for img in self.project.list_of_images_model:
                image_annotations = []

                for an in getattr(img, 'list_of_annotations', []):
                    segmentation_flat = [coord for point in an.segmentation for coord in point]

                    annotation = {
                        "id": an.annotation_id,
                        "category_id": an.class_id,
                        "image_id": img.image_id,
                        "segmentation": [segmentation_flat]
                    }

                    image_annotations.append(annotation)

                annotations.extend(image_annotations)

                images.append({
                    "file_name": img.filename,
                    "height": img.height,
                    "width": img.width,
                    "id": img.image_id
                })

        if self.project.list_of_classes_model:
            categories = [
                {
                    "id": cl.class_id,
                    "name": cl.name,
                    "color": cl.color
                } for cl in self.project.list_of_classes_model
            ]

        image_path = ""
        if self.project.list_of_images_model:
            image_path = os.path.dirname(self.project.get_full_path_by_filename(self.project.list_of_images_model[0].filename))
        print("ok")

        data = {
            "images": images,
            "categories": categories,
            "annotations": annotations,
            "image_path": image_path
        }

        try:
            folder_path = os.path.dirname(output_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Plik .pro został utworzony: {output_path}")
        except Exception as e:
            print(f"Błąd podczas tworzenia pliku .pro: {str(e)}")

    def save_project(self):
        if not self.project_path:
            self.project_path = self.select_save_location()

        if not self.project_path:
            return False  # Użytkownik anulował wybór

        if not self.project_path.endswith(".pro"):
            self.project_path += ".pro"

        self.unlock_file()
        self.create_file(self.project_path)
        self.lock_file(self.project_path)
        return True

    def lock_file(self, file_path):
        try:
            self.file_lock = open(file_path, 'r+')
            if platform.system() == "Windows":
                msvcrt.locking(self.file_lock.fileno(), msvcrt.LK_NBLCK, os.path.getsize(file_path))
            else:
                fcntl.flock(self.file_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            print(f"Plik {file_path} został zablokowany.")
        except Exception as e:
            print(f"Nie można zablokować pliku: {str(e)}")

    def unlock_file(self):
        if self.file_lock:
            try:
                if platform.system() == "Windows":
                    msvcrt.locking(self.file_lock.fileno(), msvcrt.LK_UNLCK, os.path.getsize(self.file_lock.name))
                else:
                    fcntl.flock(self.file_lock, fcntl.LOCK_UN)
                self.file_lock.close()
                self.file_lock = None
                print("Plik został odblokowany.")
            except Exception as e:
                print(f"Nie można odblokować pliku: {str(e)}")
