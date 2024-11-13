import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import QRectF
from spyder.plugins.help.utils.conf import project


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
        # Zaznaczenie pierwszego pliku, jeśli lista nie jest pusta
        if self.view.file_list_widget.count() > 0:
            first_item = self.view.file_list_widget.item(0)
            self.view.file_list_widget.setCurrentItem(first_item)
            # Wywołanie metody do wyświetlenia pierwszego obrazu
            self.show_image(first_item)
        else:
            self.view.set_image_size_label("Brak aktywnego obrazu") #Aktualizacja label z informacjami o wielkosci na Brak aktywnego obrazu
            self.view.scene.clear()


    # Zdarzenie po naciśnięciu obrazka na liście po prawej stronie
    def show_image(self, item):
        file_name = item.text()
        image_path = os.path.join(self.project.folder_path, file_name)
        print(image_path)
        self.display_image(image_path)
        self.apply_zooming(0.7) # minimalna wielkosc obrazka (70% orginału)
        #Aktualizacja label z informacjami o wielkosci
        active_image = self.project.get_img_by_filename(file_name)
        if active_image is not None:
            self.view.set_image_size_label(str(active_image.width) + "x" + str(active_image.height))
        else:
            self.view.set_image_size_label("Wystapily problemy")
    #
    # # metoda do wyswietlania obrazka
    # def display_image(self, image_path):
    #     pixmap = QPixmap(image_path)
    #     if pixmap.isNull():
    #         print("Nie udało się załadować obrazu.")
    #         return
    #     self.view.scene.clear()
    #

    def display_image(self, image_path): # niedokonczona
        try:
            print(f"Loading image from path: {image_path}")
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                print(f"Failed to load image: {image_path}")
                return

            print("Image loaded successfully!")

            self.view.scene.clear()
            self.view.scene.addItem(QGraphicsPixmapItem(pixmap))



            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.view.scene.addItem(pixmap_item)

            # Ustawienie sceny na rozmiar obrazka
            scene_rect = QRectF(pixmap.rect())  # Konwertowanie QRect na QRectF
            print(f"Setting scene rect: {scene_rect}")
            self.view.graphics_view.setSceneRect(scene_rect)


            # Resetowanie poprzednich transformacji
            self.view.graphics_view.resetTransform()

        except Exception as e:
            print(f"Error while displaying image: {e}")

    def apply_zooming(self,value): # niedokonczona
        scale_factor = max(self.view.zoom_image_slider.value() / 30, value)  #im wieksza liczba tym mniej skaluje się obrazek
        print(f"Applying zoom: {scale_factor}")  # Logowanie poziomu zoomu
        self.view.graphics_view.scale(scale_factor, scale_factor)


