import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import QRectF
# from spyder.plugins.help.utils.conf import project


#Prezenter zarządzający listą plików i interakcjami z nią
class FileListPresenter:
    def __init__(self, view):
        self.view = view
        self.project = None

    def update_view(self, view):
        self.view = view
        # Dodanie połączenia po tym, jak widok został zaktualizowany
        if self.view and self.view.zoom_image_slider:
            self.view.zoom_image_slider.valueChanged.connect(self.on_zoom_slider_changed)

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
    # def show_image(self, item):
    #     file_name = item.text()
    #     image_path = os.path.join(self.project.folder_path, file_name)
    #     print(image_path)
    #     self.display_image(image_path)
    #     self.apply_zooming(0.7) # minimalna wielkosc obrazka (70% orginału)
    #     #Aktualizacja label z informacjami o wielkosci
    #     active_image = self.project.get_img_by_filename(file_name)
    #     if active_image is not None:
    #         self.view.set_image_size_label(str(active_image.width) + "x" + str(active_image.height))
    #     else:
    #         self.view.set_image_size_label("Wystapily problemy")

    def show_image(self, item):
        file_name = item.text()
        image_path = os.path.join(self.project.folder_path, file_name)
        print(image_path)
        self.display_image(image_path)

        # Znajdź obraz w projekcie i ustaw zoom
        active_image = self.project.get_img_by_filename(file_name)
        if active_image is not None:
            self.view.set_image_size_label(f"{active_image.width}x{active_image.height}")
            initial_zoom_value = active_image.zoom  # Użyj atrybutu zoom z modelu obrazu
        else:
            self.view.set_image_size_label("Wystąpiły problemy")
            initial_zoom_value = 0.7  # Jeśli nie udało się znaleźć obrazu, ustaw zoom na 100%

        # Zaktualizowanie wartości suwaka
        self.view.zoom_image_slider.setValue(initial_zoom_value * 300)  # Przekształć na procenty (0-100)

        # Wywołanie zoomowania z początkową wartością
        self.apply_zooming(initial_zoom_value)  # Używamy zoomu z modelu obrazu

    def display_image(self, image_path): # niedokonczona
        try:
            print(f"Loading image from path: {image_path}")
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                print(f"Failed to load image: {image_path}")
                return

            print("Image loaded successfully!")

            self.view.scene.clear()

            self.view.pixmap_item = QGraphicsPixmapItem(pixmap)
            self.view.scene.addItem(self.view.pixmap_item)

            # Ustawienie sceny na rozmiar obrazka
            scene_rect = QRectF(pixmap.rect())  # Konwertowanie QRect na QRectF
            print(f"Setting scene rect: {scene_rect}")
            self.view.graphics_view.setSceneRect(scene_rect)


            # Resetowanie poprzednich transformacji
            self.view.graphics_view.resetTransform()

        except Exception as e:
            print(f"Error while displaying image: {e}")

    # def apply_zooming(self,value): # niedokonczona
    #     scale_factor = max(self.view.zoom_image_slider.value() / 30, value)  #im wieksza liczba tym mniej skaluje się obrazek
    #     print(f"Applying zoom: {scale_factor}")  # Logowanie poziomu zoomu
    #     self.view.graphics_view.scale(scale_factor, scale_factor)

    def apply_zooming(self, zoom_value):
        try:
            # Resetowanie transformacji przed zastosowaniem nowego współczynnika skalowania
            self.view.graphics_view.resetTransform()

            # Zastosowanie nowego skalowania
            self.view.graphics_view.scale(zoom_value, zoom_value)

            print(f"Applied zoom: scale_factor={zoom_value}")  # Logowanie dla celów diagnostycznych
        except Exception as e:
            print(f"Error in apply_zooming: {e}")

    # def on_zoom_slider_changed(self):
    #     zoom_value = self.view.zoom_image_slider.value() / 30  # Dopasowanie wartości zoomu
    #     self.apply_zooming(zoom_value)

    def on_zoom_slider_changed(self):
        # Pobierz wartość suwaka (zakładając, że suwak ma zakres od 0 do 100)
        zoom_value = self.view.zoom_image_slider.value() / 30.0  # Zamiana na wartość między 0 a 1

        # Zaktualizowanie zoomu w modelu
        active_image = self.project.get_img_by_filename(self.view.file_list_widget.currentItem().text())
        if active_image is not None:
            active_image.zoom_change(zoom_value)

        # Zastosowanie nowego zoomu
        self.apply_zooming(zoom_value)



