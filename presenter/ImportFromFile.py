from PyQt5.QtWidgets import QFileDialog

class ImportFromFile:
    def __init__(self, view):
        self.view = view
        #Zmienne z listami do wczytania obiektów, potem są zwracane głównemu prezenterowi i na ich podstawie jest tworzony nowy projekt
        self.images_list = None
        self.classes_list = None
        self.annotations_list = None
        self.json_path = None

    #Funkcja importu z COCO do projektu
    def import_from_COCO(self):
        print("Importowanie")
        self.json_path, _ = QFileDialog.getOpenFileName(self.view.centralwidget.parent(), "Wybierz plik JSON", "", "JSON Files (*.json);")
        #Tutaj trzeba by sprawdzic czy istnieje self.json_path/images a potem sprawdzic czy nazwy plikow zgadzają sie z images w jsonie


        return self.images_list, self.classes_list, self.annotations_list, self.json_path