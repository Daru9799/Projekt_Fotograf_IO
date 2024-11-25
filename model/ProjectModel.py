import os
from operator import indexOf
from PIL import Image
from PIL.ExifTags import TAGS
import random
# from statsmodels.sandbox.stats.contrast_tools import contrast_labels

from model.ImageModel import ImageModel
from random import randrange
from model.ClassModel import ClassModel
from model.ExifModel import ExifModel

#Model projektu (przechowuje informacji o aktualnie wczytanych obrazkach i klasach)
class ProjectModel:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.list_of_images_model = []
        self.list_of_classes_model = []

        # Seedowanie klas do testów:
        self.addNewClass("test")
        self.list_of_classes_model[0].color = (20,44,255)

    #Wczytanie zdjec z folderu, utworzenie obiektow i zapisanie ich na liscie
    def load_images(self):
        self.list_of_images_model = []
        image_id = 1
        for filename in os.listdir(self.folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                # Pelna sciezka
                file_path = os.path.join(self.folder_path, filename)
                # wczytanie informacji o rozmiarze zdjecia (wykorzystanie PILLOW)
                with Image.open(file_path) as img:
                    img_width, img_height = img.size
                #Utworzenie obiektu exif
                exif_obj = self.create_exif_obj(file_path)
                #Utworzenie obiektu i zapisanie na liscie
                img_obj = ImageModel(image_id, filename, img_width, img_height, exif_obj, None)
                self.list_of_images_model.append(img_obj)
                image_id+=1
        #Test w konsoli
        for img in self.list_of_images_model:
            print(str(img.image_id) + "; " + img.filename +  "; " + str(img.width) +  "; " + str(img.height))
            if img.exif_obj:
                print("EXIF:")
                img.exif_obj.get_info()

    def create_exif_obj(self, file_path):
        exif_info = self.get_exif_data(file_path)
        #Jeśli nic nie znalazł to zwraca None
        if not exif_info:
            print("No EXIF data found.")
            return None

        producer = exif_info.get("Make", "No data")
        model_of_camera = exif_info.get("Model", "No data")
        lens = exif_info.get("LensModel", "No data")
        orientation = exif_info.get("Orientation", "No data")
        flash = exif_info.get("Flash", "No data")
        capture_data = exif_info.get("DateTimeOriginal", "No data")
        iso = exif_info.get("ISOSpeedRatings", "No data")
        focal_length = exif_info.get("FocalLength", "No data")
        exposure_time = exif_info.get("ExposureTime", "No data")
        aperture = exif_info.get("FNumber", "No data")
        saturation = exif_info.get("Saturation","No data")
        contrast = exif_info.get("Contrast", "No data")
        sharpness = exif_info.get("Sharpness", "No data")
        digital_zoom_ratio = exif_info.get("DigitalZoomRatio", "No data")
        brightness_value = exif_info.get("BrightnessValue", "No Data")
        exposure_bias = exif_info.get("ExposureBiasValue", "No data")

        exif_model = ExifModel(
            producer = producer,
            model_of_camera = model_of_camera,
            lens = lens,
            orientation = orientation,
            flash = flash,
            capture_data = capture_data,
            iso = iso,
            focal_length = focal_length,
            exposure_time = exposure_time,
            aperture = aperture,
            saturation = saturation,
            contrast = contrast,
            sharpness = sharpness,
            digital_zoom_ratio = digital_zoom_ratio,
            brightness_value = brightness_value,
            exposure_bias = exposure_bias
        )
        return exif_model

    def get_exif_data(self, file_path):
        image = Image.open(file_path)
        #Pobranie danych EXIF
        exif_data = image._getexif()
        if exif_data is None:
            return None
        #Przygotowanie danych EXIF
        exif_info = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            exif_info[tag_name] = value
        print(exif_info)
        return exif_info

    # def load_classes(self): -> klasa do zaladowania listy klas podczas importu
    #     return 0

    # Obsługa dodawania nowej klasy do listy klas
    def addNewClass(self, clName):
        uniqueId = randrange(1000000,9999999)
        isUnique = False
        #Generowanie unikatowego id
        while not isUnique:
            isUnique = True
            for c in self.list_of_classes_model:
                if c.class_id == uniqueId:
                    uniqueId = randrange(1000000,9999999)
                    isUnique = False
        newClass = ClassModel(class_id=uniqueId, name=clName, color=self.random_color()) # tworzenie obiektu ClassModel
        self.list_of_classes_model.append(newClass)

    def deleteClass(self, clId): # niedokończone
        # !!! Trzeba uwzględnić potem usuwanie adnotacji powiązanych z usuniętą klasą
        classIndex = -1
        for cl in self.list_of_classes_model:
            if cl.class_id == clId:
                classIndex = indexOf(self.list_of_classes_model,cl)
        self.list_of_classes_model.pop(classIndex)

    # Podmienia starą klasę na nową
    def updateClass(self, classObj):
        for cl in self.list_of_classes_model:
            if cl.class_id == classObj.class_id:
                classIndex = indexOf(self.list_of_classes_model,cl)
                self.list_of_classes_model[classIndex] = classObj

    def random_color(self):
        """Zwraca losowy kolor w formacie RGB."""
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    ### Gettery do list
    # Zwrócenie obrazu na podstawie nazwy pliku
    def get_img_by_filename(self, filename):
        for img_obj in self.list_of_images_model:
            if img_obj.filename == filename:
                return img_obj
        return None  # Jeśli nie znaleziono obrazu o podanej nazwie zwroci None

    def get_color_by_class_id(self,class_id):
        for cl in self.list_of_classes_model:
            if cl.class_id==class_id:
                return cl.color
        return
