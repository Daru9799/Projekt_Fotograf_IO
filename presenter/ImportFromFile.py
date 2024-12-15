from PyQt5.QtWidgets import QFileDialog
from model.ClassModel import ClassModel
from model.ImageModel import ImageModel
from model.ExifModel import ExifModel
from model.AnnotationModel import AnnotationModel
import random
import json
import os

class ImportFromFile:
    def __init__(self, view):
        self.view = view
        #Zmienne z listami do wczytania obiektów, potem są zwracane głównemu prezenterowi i na ich podstawie jest tworzony nowy projekt
        self.images_list = []
        self.classes_list = []
        self.json_path = None #Ściezka do JSONA
        self.json_folder = None #Ściezka do samego folderu
        self.json_data = None #Zmienna przechowujaca zawartosc jsona
        self.project_path = None #Ścieżka do pliku projektowego
        self.project_images_folder = None #Ściezka do zdjec do ktorych odnosi sie plik projektowy
        self.project_data = None #Zmienna przechowywujaca zawartosc pliku projektowego

    #Funkcja importu z COCO do projektu
    def import_from_COCO(self):
        print("Importowanie")
        self.json_path, _ = QFileDialog.getOpenFileName(self.view.centralwidget.parent(), "Wybierz plik JSON", "", "JSON Files (*.json);")
        #Jeśli nic sie nei wybierze:
        if not self.json_path:
            return None, None, None

        #Zapis sciezki do folderu w osobnej zmiennej
        self.json_folder = os.path.dirname(self.json_path)
        #Zapisanie zawartości jsona do zmiennej
        with open(self.json_path, 'r', encoding='utf-8') as json_file:
            self.json_data = json.load(json_file)
        #Tutaj trzeba by sprawdzic czy istnieje self.json_path/images a potem sprawdzic czy nazwy plikow zgadzają sie z images w jsonie

        #Import klas
        self.load_classes_from_json()
        #Import obrazków (wraz z adnotacjami)
        self.load_images_from_json()

        return self.images_list, self.classes_list, self.json_folder

    def load_classes_from_json(self):
        categories = self.json_data["categories"]
        for category in categories:
            class_obj = ClassModel(class_id=category["id"], name=category["name"], color=self.generate_random_color())
            self.classes_list.append(class_obj)

    def load_images_from_json(self):
        images = self.json_data.get("images")
        print(images)
        annotations = self.json_data.get("annotations")
        merge_image_path = os.path.join(self.json_folder, "images")
        self.load_images_to_objects(images, annotations, merge_image_path)

    def load_images_to_objects(self, images, annotations, path_to_folder):
        for image in images:
            file_path = os.path.join(path_to_folder, image["file_name"])
            #Exify
            exif_obj = ExifModel.create_exif_obj(file_path)
            #Adnotacje
            image_annotations = [annot for annot in annotations if annot["image_id"] == image["id"]] #Pobranie adnotacji dla danego obrazka
            list_of_annotations = []
            for annot in image_annotations:
                #Konwersja na liste krotek tzn tak jak w modelu jest [(10, 20), (30, 40), (50, 20), (30, 10)]
                segmentation_data = annot["segmentation"][0]
                segmentation = [(segmentation_data[i], segmentation_data[i + 1]) for i in range(0, len(segmentation_data), 2)]
                annot_obj = AnnotationModel(annotation_id=annot["id"], area=segmentation, class_id=annot["category_id"])
                list_of_annotations.append(annot_obj)
            #Obiekt obrazka
            img_obj = ImageModel(image_id=image["id"], filename=image["file_name"], width=image["width"], height=image["height"], exif_obj=exif_obj, list_of_annotations=list_of_annotations)
            self.images_list.append(img_obj)

    def generate_random_color(self):
        return tuple(random.randint(0, 255) for _ in range(3))

    def reset_imported_data(self):
        self.images_list = []
        self.classes_list = []
        self.json_path = None
        self.json_folder = None
        self.json_data = None
        self.project_images_folder = None
        self.project_data = None

    def import_from_project_file(self):
        print("Importowanie z pliku projektowego")
        self.project_path, _ = QFileDialog.getOpenFileName(self.view.centralwidget.parent(), "Wybierz plik projektowy", "", "Project Files (*.pro);")
        # Jeśli nic sie nie wybierze:
        if not self.project_path:
            return None, None, None

        # Zapisanie zawartości pliku projektowego do zmiennej
        with open(self.project_path, 'r', encoding='utf-8') as json_file:
            self.project_data = json.load(json_file)

        #Zapis sciezki folderu z obrazkami w osobnej zmiennej (potem zwraca main_presenterowi)
        self.project_images_folder = self.project_data.get("image_path")

        # Import klas
        self.load_classes_from_project_file()
        # Import obrazków (wraz z adnotacjami)
        self.load_images_from_project_file()
        return self.images_list, self.classes_list, self.project_images_folder

    def load_classes_from_project_file(self):
        categories = self.project_data["categories"]
        for category in categories:
            class_obj = ClassModel(class_id=category["id"], name=category["name"], color=tuple(category["color"])) #Konwersja do koloru do krotki (z tablicy)
            self.classes_list.append(class_obj)

    def load_images_from_project_file(self):
        images = self.project_data.get("images")
        annotations = self.project_data.get("annotations")
        self.load_images_to_objects(images, annotations, self.project_images_folder)