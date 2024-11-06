import os
from model.ImageModel import ImageModel

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
