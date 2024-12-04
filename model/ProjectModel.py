import os
from operator import indexOf
from PIL import Image
import random
import copy
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
        #self.addNewClass("test")
        #self.list_of_classes_model[0].color = (20,44,255)

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
                exif_obj = ExifModel.create_exif_obj(file_path)
                #Utworzenie obiektu i zapisanie na liscie
                img_obj = ImageModel(image_id, filename, img_width, img_height, exif_obj, None)
                self.list_of_images_model.append(img_obj)
                image_id+=1

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

    def uppdate_annotation_by_image_object(self, img_obj, annot_list):
        for img in self.list_of_images_model:
            if img.image_id == img_obj.image_id:
                imgIndex = indexOf(self.list_of_images_model, img)
                new_annot = copy.deepcopy(annot_list)
                img.set_annotation_list(new_annot)
                self.list_of_images_model[imgIndex] = img


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

    def get_name_by_class_id(self, class_id):
        for cl in self.list_of_classes_model:
            if cl.class_id == class_id:
                return cl.name
        return

    def get_full_path_by_filename(self, filename):
        for i in self.list_of_images_model:
            if i.filename == filename:
                return os.path.join(self.folder_path, filename)  # Tworzy pełną ścieżkę
        return None  # Jeśli nie znaleziono pliku, zwraca None


