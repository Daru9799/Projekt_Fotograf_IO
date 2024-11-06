import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem

#Prezenter zarządzający listą plików i interakcjami z nią
class FileListPresenter:
    def __init__(self, view):
        self.view = view
        self.project = None

    def update_project(self, project):
        self.project = project

    # Załadowanie plików do listy po prawej stronie
    def load_files_to_widget(self):
        # Czyszczenie poprzedniej listy
        self.view.file_list_widget.clear()
        # Załadowanie plików z modelu do listy
        for img_obj in self.project.list_of_images_model:
            self.view.file_list_widget.addItem(img_obj.filename)

    # Zdarzenie po naciśnięciu obrazka na liście po prawej stronie
    def show_image(self, item):
        file_name = item.text()
        image_path = os.path.join(self.project.folder_path, file_name)
        print(image_path)
        self.display_image(image_path)

    # metoda do wyswietlania obrazka
    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Nie udało się załadować obrazu.")
            return
        self.view.scene.clear()
        self.view.scene.addItem(QGraphicsPixmapItem(pixmap))