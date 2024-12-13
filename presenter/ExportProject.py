import os
import json
from PyQt5.QtWidgets import QFileDialog

class ExportProject:
    def __init__(self, view, project):
        self.view = view
        self.project_path = None
        self.project = project

    def select_save_location(self):
        # Otwórz okno dialogowe do wyboru lokalizacji i nazwy pliku
        self.project_path, _ = QFileDialog.getSaveFileName(
            self.view.centralwidget.parent(), "Wybierz lokalizację do zapisu", "",
            "Project files (*.pro);;"
        )
        return self.project_path


    def create_file(self, output_path):
        # Przygotowanie danych JSON
        annotations = []
        images = []

        for img in self.project.list_of_images_model:
            image_annotations = []

            for an in img.list_of_annotations:
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

        categories = [
            {
                "id": cl.class_id,
                "name": cl.name,
                "color":cl.color
            } for cl in self.project.list_of_classes_model
        ]

        image_path = os.path.dirname(self.project.get_full_path_by_filename(self.project.list_of_images_model[0].filename))

        data = {
            "images": images,
            "categories": categories,
            "annotations": annotations,
            "image_path": image_path
        }

        try:
            # Tworzymy foldery, jeśli nie istnieją
            folder_path = os.path.dirname(output_path)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Zapisujemy dane do pliku .pro
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Plik .pro został utworzony: {output_path}")
        except Exception as e:
            print(f"Błąd podczas tworzenia pliku .pro: {str(e)}")

