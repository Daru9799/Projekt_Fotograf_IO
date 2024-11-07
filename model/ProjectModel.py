import os

from numpy.ma.extras import unique

from model.ImageModel import ImageModel
from random import randrange
from model.ClassModel import ClassModel

class ProjectModel:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.list_of_images_model = []
        self.list_of_classes_model = []

    #Wczytanie zdjec z folderu, utworzenie obiektow i zapisanie ich na liscie
    def load_images(self):
        self.list_of_images_model = []
        image_id = 1
        for filename in os.listdir(self.folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                #Na razie bez ustalenia innych danych poza path i id
                img_obj = ImageModel(image_id, filename, 0, 0, None, None)
                self.list_of_images_model.append(img_obj)
                image_id+=1

        for img in self.list_of_images_model: #Test
            print(img.filename)

    # def load_classes(self): -> klasa do zaladowania listy klas podczas importu
    #     return 0

    # Obsługa dodawania nowej klasy do listy klas
    def addNewClass(self, clName):
        uniqueId = randrange(1000000,9999999)
        isUnique = False
        #Generowanie unikatowego id
        while not isUnique: # <-------------- do testów ta pentla
            isUnique = True
            for c in self.list_of_classes_model:
                if c.class_id == uniqueId:
                    uniqueId = randrange(1000000,9999999)
                    isUnique = False
        newClass = ClassModel(class_id=uniqueId, name=clName) # tworzenie obiektu ClassModel
        self.list_of_classes_model.append(newClass)


