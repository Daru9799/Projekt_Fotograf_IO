import os
from PyQt5.QtWidgets import QFileDialog

#Modele
from model.ProjectModel import ProjectModel
from model.ImageModel import ImageModel
from model.ClassModel import ClassModel

class Presenter:
    def __init__(self, view):
        self.view = view
        self.new_project = ProjectModel(None)

    #Utworzenie nowego projektu, wczytanie danych do modelu
    def create_new_project(self):
        folder_path = QFileDialog.getExistingDirectory(self.view.centralwidget.parent(), "Wybierz folder ze zdjęciami")
        if folder_path:
            self.new_project.folder_path = folder_path
            print(f'Wybrano: {self.new_project.folder_path}') #W ramach testów zeby podejrzeć jaką ściezke przesyła
            self.new_project.load_images() #Zaladowanie zdjec do modelu
            self.load_files_to_widget() #Wczytanie pliku ze zdjęciami do listy w widoku
        else:
            print("Nie wybrano folderu.")

    #Załadowanie plików do listy po prawej stronie
    def load_files_to_widget(self):
        #Czyszczenie poprzedniej listy
        self.view.file_list_widget.clear()
        # Załadowanie plików z modelu do listy
        for img_obj in self.new_project.list_of_images_model:
            self.view.file_list_widget.addItem(img_obj.filename)

    #Zdarzenie po naciśnięciu obrazka na liście po prawej stronie
    def folder_list_on_click(self, item):
        file_name = item.text()
        image_path = os.path.join(self.new_project.folder_path, file_name)
        print(image_path)
        self.view.display_image(image_path)


