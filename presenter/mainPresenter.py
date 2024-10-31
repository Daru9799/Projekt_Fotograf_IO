import os
from model.mainModel import Project
from PyQt5.QtWidgets import QFileDialog

class Presenter:
    def __init__(self, view):
        self.view = view
        self.new_project = Project(None)

    #Tworzenie nowego projektu (załadowanie folderu ze zdjęciami)
    def create_new_project(self):
        folder_path = QFileDialog.getExistingDirectory(self.view, "Wybierz folder ze zdjęciami")
        if folder_path:
            self.new_project.folderPath = folder_path
            print(f'Wybrano: {self.new_project.folderPath}') #W ramach testów zeby podejrzeć jaką ściezke przesyła

            # Wczytanie pliku ze zdjęciami do listy
            self.load_files(self.new_project.folderPath)
            #Przeslanie sciezki do widoku, zeby zaaktualizowac label
            self.view.update_folder_path(self.new_project.folderPath)
        else:
            print("Nie wybrano folderu.")

    def load_files(self, folder_path):
        #Czyszczenie poprzedniej listy
        self.view.file_list_widget.clear()

        # Załadowanie plików do listy
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Tutaj mozna dodac potem wiecej rozszerzen
                self.view.file_list_widget.addItem(filename)


    # Po kliknieciu na prawy panel z plikami uzyskujemy nazwe i wywolujemy odpowiednia funkcje
    def folder_list_on_click(self, item):
        file_name = item.text()
        image_path = os.path.join(self.new_project.folderPath, file_name)
        print(image_path)
        self.view.display_image(image_path)


