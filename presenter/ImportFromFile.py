from PyQt5.QtWidgets import QFileDialog
from model.ClassModel import ClassModel
from model.ImageModel import ImageModel
from model.ExifModel import ExifModel
from model.AnnotationModel import AnnotationModel
from PIL import Image
import random
import json
import os
import yaml

class ImportFromFile:
    def __init__(self, view):
        self.view = view
        #Zmienne z listami do wczytania obiektów, potem są zwracane głównemu prezenterowi i na ich podstawie jest tworzony nowy projekt
        self.images_list = []
        self.classes_list = []
        #COCO (JSON)
        self.json_path = None #Ściezka do JSONA
        self.json_folder = None #Ściezka do samego folderu
        self.json_data = None #Zmienna przechowujaca zawartosc jsona
        #PROJEKTOWY (.PRO)
        self.project_path = None #Ścieżka do pliku projektowego
        self.project_images_folder = None #Ściezka do zdjec do ktorych odnosi sie plik projektowy
        self.project_data = None #Zmienna przechowywujaca zawartosc pliku projektowego
        #YOLO (YAML)
        self.yaml_path = None #Ściezka do YAML
        self.yaml_folder = None #Ściezka do samego folderu
        self.yaml_data = None #Zmienna przechowujaca zawartosc yamla

    #Funkcja importu z COCO do projektu
    def import_from_COCO(self):
        try:
            self.json_path, _ = QFileDialog.getOpenFileName(self.view.centralwidget.parent(), "Wybierz plik JSON", "", "JSON Files (*.json);")
            #Jeśli nic sie nie wybierze:
            if not self.json_path:
                return None, None, None

            #Zapis sciezki do folderu w osobnej zmiennej
            self.json_folder = os.path.dirname(self.json_path)

            #Zapisanie zawartości jsona do zmiennej
            with open(self.json_path, 'r', encoding='utf-8') as json_file:
                self.json_data = json.load(json_file)

            #Sprawdzenie struktury czy wszystkie klucze istnieją
            required_keys = ["categories", "images", "annotations"]
            for key in required_keys:
                if key not in self.json_data:
                    self.view.show_message_OK("Błąd", f"Brak wymaganego klucza w JSON: '{key}'")
                    return None, None, None

            #Sprawdzenie czy folder z obrazkami istnieje
            image_folder_path = os.path.join(self.json_folder, "images")
            if not os.path.isdir(image_folder_path):
                self.view.show_message_OK("Błąd", f"Folder 'images' nie istnieje!")
                return None, None, None

            #Sprawdzenie czy folder zawiera odpowiednie obrazki ()
            missing_files = [image["file_name"] for image in self.json_data["images"] if not os.path.isfile(os.path.join(image_folder_path, image["file_name"]))]
            if missing_files:
                self.view.show_message_OK("Błąd", f"Brakujące pliki obrazów w folderze 'images':\n{', '.join(missing_files)}")
                return None, None, None

            #Import klas
            self.load_classes_from_json()
            #Import obrazków (wraz z adnotacjami)
            self.load_images_from_json()

            return self.images_list, self.classes_list, self.json_folder

        except Exception as e:
            self.view.show_message_OK("Błąd krytyczny", f"Wystąpił nieoczekiwany błąd! Prawdopodobnie plik jest uszkodzony!")
            print(e)
            return None, None, None

    def load_classes_from_json(self):
        categories = self.json_data["categories"]
        for category in categories:
            class_obj = ClassModel(class_id=category["id"], name=category["name"], color=self.generate_random_color())
            self.classes_list.append(class_obj)

    def load_images_from_json(self):
        images = self.json_data.get("images")
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
        self.yaml_path = None
        self.yaml_folder = None
        self.yaml_data = None

    def import_from_project_file(self):
        try:
            self.project_path, _ = QFileDialog.getOpenFileName(self.view.centralwidget.parent(), "Wybierz plik projektowy", "", "Project Files (*.pro);")
            # Jeśli nic sie nie wybierze:
            if not self.project_path:
                return None, None, None

            # Zapisanie zawartości pliku projektowego do zmiennej
            with open(self.project_path, 'r', encoding='utf-8') as json_file:
                self.project_data = json.load(json_file)

            #Sprawdzenie struktury czy wszystkie klucze istnieją
            required_keys = ["categories", "images", "annotations", "image_path"]
            for key in required_keys:
                if key not in self.project_data:
                    self.view.show_message_OK("Błąd", f"Brak wymaganego klucza w pliku: '{key}'")
                    return None, None, None

            #Zapis sciezki folderu z obrazkami w osobnej zmiennej (potem zwraca main_presenterowi)
            self.project_images_folder = self.project_data.get("image_path")

            # Sprawdzenie czy folder z obrazkami istnieje
            if not os.path.isdir(self.project_images_folder):
                self.view.show_message_OK("Błąd", "Nie udało się zlokalizować folderu zawierającego obrazy!")
                return None, None, None

            # Sprawdzenie czy folder zawiera odpowiednie obrazki
            missing_files = [image["file_name"] for image in self.project_data["images"] if not os.path.isfile(os.path.join(self.project_images_folder, image["file_name"]))]
            if missing_files:
                self.view.show_message_OK("Błąd", f"Brakujące pliki obrazów w folderze:\n{', '.join(missing_files)}")
                return None, None, None

            # Import klas
            self.load_classes_from_project_file()
            # Import obrazków (wraz z adnotacjami)
            self.load_images_from_project_file()
            return self.images_list, self.classes_list, self.project_images_folder

        except Exception as e:
            self.view.show_message_OK("Błąd krytyczny", f"Wystąpił nieoczekiwany błąd! Prawdopodobnie plik jest uszkodzony!")
            print(e)
            return None, None, None

    def load_classes_from_project_file(self):
        categories = self.project_data["categories"]
        for category in categories:
            class_obj = ClassModel(class_id=category["id"], name=category["name"], color=tuple(category["color"])) #Konwersja do koloru do krotki (z tablicy)
            self.classes_list.append(class_obj)

    def load_images_from_project_file(self):
        images = self.project_data.get("images")
        annotations = self.project_data.get("annotations")
        self.load_images_to_objects(images, annotations, self.project_images_folder)

    def import_from_YOLO(self):
        try:
            #Wybór pliku YAML
            self.yaml_path, _ = QFileDialog.getOpenFileName(self.view.centralwidget.parent(), "Wybierz plik YAML", "","YOLO Config Files (*.yaml *.yml)")
            #Jeśli nic nie wybrano
            if not self.yaml_path:
                return None, None, None

            #Zapis sciezki do folderu w osobnej zmiennej
            self.yaml_folder = os.path.dirname(self.yaml_path)

            #Zapisanie zawartości yamla do zmiennej
            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                self.yaml_data = yaml.safe_load(f)

            #Sprawdzenie struktury YOLO
            required_keys = ["names", "train"]
            for key in required_keys:
                if key not in self.yaml_data:
                    self.view.show_message_OK("Błąd", f"Brak wymaganego klucza w YAML: '{key}'")
                    return None, None, None

            #Sprawdzenie folderu z obrazkami
            yaml_images_folder = os.path.join(self.yaml_folder, "train", "images")
            if not os.path.isdir(yaml_images_folder):
                self.view.show_message_OK("Błąd", "Folder 'train/images' nie istnieje!")
                return None, None, None

            #Sprawdzenie folderu z etykietami
            yaml_labels_folder = os.path.join(self.yaml_folder, "train", "labels")
            if not os.path.isdir(yaml_labels_folder):
                self.view.show_message_OK("Błąd", "Folder 'train/labels' nie istnieje!")
                return None, None, None

            # Sprawdzenie czy każdy obrazek ma plik etykiety
            image_files = [file for file in os.listdir(yaml_images_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            missing_labels = []
            for image_file in image_files:
                label_file = os.path.splitext(image_file)[0] + ".txt"
                label_path = os.path.join(yaml_labels_folder, label_file)
                if not os.path.isfile(label_path):
                    missing_labels.append(image_file)

            if missing_labels:
                self.view.show_message_OK("Błąd", f"Dla następujących obrazków brakuje plików etykiet:\n{', '.join(missing_labels)}")
                return None, None, None

            #Import klas
            self.load_classes_from_yaml()
            #Import obrazków (wraz z adnotacjami)
            self.load_images_from_yolo()

            return self.images_list, self.classes_list, self.yaml_folder

        except Exception as e:
            self.view.show_message_OK("Błąd krytyczny", f"Wystąpił nieoczekiwany błąd! Prawdopodobnie plik jest uszkodzony!")
            print(e)
            return None, None, None

    def load_classes_from_yaml(self):
        categories = self.yaml_data.get('names', {})
        for class_id, name in categories.items():
            print(f"ID: {class_id}, Name: {name}")
            class_obj = ClassModel(class_id=class_id, name=name, color=self.generate_random_color())
            self.classes_list.append(class_obj)

    def load_images_from_yolo(self):
        yaml_images_folder = os.path.join(self.yaml_folder, "train", "images")
        yaml_labels_folder = os.path.join(self.yaml_folder, "train", "labels")
        image_id_counter = 1 #Do nadawania id obrazkom (YOLO w przeciwieńswie do COCO nie zapisuje tego nigdzie)
        for image_file in os.listdir(yaml_images_folder):
            if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            image_path = os.path.join(yaml_images_folder, image_file)
            label_file = os.path.splitext(image_file)[0] + ".txt"
            label_path = os.path.join(yaml_labels_folder, label_file)

            #Pobranie wysokosci i szerokosci obrazka
            with Image.open(image_path) as img:
                width, height = img.size

            #EXIFY
            exif_obj = ExifModel.create_exif_obj(image_path)
            #Adnotacje
            list_of_annotations = []
            annotation_id_counter = 1
            with open(label_path, 'r') as label:
                for line in label:
                    parts = line.strip().split()
                    class_id = int(parts[0]) #Id klasy danej adnotacji jest zawsze 1 wartością
                    #Jeśli linia ma wiecej jak 5 wartosci to jest to segmentacja (zapis poligona)
                    if len(parts) > 5:
                        normalized_segmentation = list(map(float, parts[1:]))
                        #Konwersja na współrzędne
                        segmentation = [(normalized_segmentation[i] * width if i % 2 == 0 else normalized_segmentation[i] * height) for i in range(len(normalized_segmentation))]
                        print(f"Skonwertowana segmentacja (współrzędne): {segmentation}")
                        segmentation_points = [(segmentation[i], segmentation[i + 1]) for i in range(0, len(segmentation), 2)]
                        annot_obj = AnnotationModel(annotation_id=annotation_id_counter, area=segmentation_points, class_id=class_id)
                        list_of_annotations.append(annot_obj)
                    #W innym wypadku odczytuje bounding box
                    else:
                        center_x, center_y, box_width, box_height = map(float, parts[1:])
                        #Konwersja współrzędnych YOLO do punktów
                        x_min = (center_x - box_width / 2) * width
                        y_min = (center_y - box_height / 2) * height
                        x_max = (center_x + box_width / 2) * width
                        y_max = (center_y + box_height / 2) * height
                        #Konwersja na współrzędne
                        segmentation_points = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
                        annot_obj = AnnotationModel(annotation_id=annotation_id_counter, area=segmentation_points, class_id=class_id)
                        list_of_annotations.append(annot_obj)
                    annotation_id_counter += 1

            #Obiekt obrazka
            img_obj = ImageModel(image_id=image_id_counter, filename=image_file, width=width, height=height, exif_obj=exif_obj, list_of_annotations=list_of_annotations)
            self.images_list.append(img_obj)
            image_id_counter += 1