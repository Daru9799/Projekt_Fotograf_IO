import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import QRectF

# Prezenter zarządzający listą plików i interakcjami z nią
class FileListPresenter:
    def __init__(self, view):
        self.view = view
        self.project = None


    def update_project(self, project):
        self.project = project


    def load_files_to_widget(self):
        # Czyszczenie poprzedniej listy plików
        self.view.file_list_widget.clear()
        # Załadowanie plików z modelu do listy
        for img_obj in self.project.list_of_images_model:
            self.view.file_list_widget.addItem(img_obj.filename)
        # Zaznaczenie pierwszego pliku na liście, jeśli lista nie jest pusta
        if self.view.file_list_widget.count() > 0:
            first_item = self.view.file_list_widget.item(0)
            self.view.file_list_widget.setCurrentItem(first_item)
            self.show_image(first_item)
            self.view.set_zoom_slider_visibility(True)
        else:
            # Aktualizacja etykiety informacyjnej na brak aktywnego obrazu
            self.view.set_image_size_label("Brak aktywnego obrazu")
            self.view.pixmap_item = None #zmiana obrazka na None (żeby zniwelować problem z poruszaniem po scenie przy powtórnym załadowaniu pustego folderu)
            self.view.scene.clear()
            self.view.set_zoom_slider_visibility(False)

    def show_image(self, item):
        file_name = item.text()
        image_path = os.path.join(self.project.folder_path, file_name)
        print(image_path)
        self.display_image(image_path)


        # Wyszukiwanie obrazu w projekcie
        active_image = self.project.get_img_by_filename(file_name)
        if active_image is not None:
            # Aktualizacja etykiety z informacjami o rozmiarze obrazu
            self.view.set_image_size_label(f"{active_image.width}x{active_image.height}")

            # Sprawdzenie, czy zoom został już ustawiony; jeśli nie, ustaw na 70%
            if not hasattr(active_image, 'zoom') or active_image.zoom is None:
                active_image.zoom = 0.7

            # Użycie aktualnej wartości zoomu (czy to nowej, czy już istniejącej)
            initial_zoom_value = active_image.zoom
        else:
            # W przypadku problemów z obrazem ustawienie wartości domyślnej zoomu
            self.view.set_image_size_label("Wystąpiły problemy")
            initial_zoom_value = 0.7

        # Aktualizacja wartości suwaka, aby odzwierciedlić aktualny poziom zoomu w procentach
        self.view.zoom_image_slider.setValue(int(initial_zoom_value * 100))
        self.view.apply_zooming(initial_zoom_value)

    def display_image(self, image_path):
        try:
            print(f"Loading image from path: {image_path}")
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                print(f"Failed to load image: {image_path}")
                return

            print("Image loaded successfully!")

            # Czyszczenie sceny przed dodaniem nowego obrazu
            self.view.scene.clear()

            # Utworzenie elementu graficznego obrazu
            self.view.pixmap_item = QGraphicsPixmapItem(pixmap)
            self.view.scene.addItem(self.view.pixmap_item)

            # Ustawienie rozmiaru sceny na rozmiar obrazka
            scene_rect = QRectF(pixmap.rect())
            print(f"Setting scene rect: {scene_rect}")
            self.view.graphics_view.setSceneRect(scene_rect)
            self.view.graphics_view.resetTransform()
        except Exception as e:
            print(f"Error while displaying image: {e}")

    def on_zoom_slider_changed(self):
        zoom_value = self.view.zoom_image_slider.value() / 100.0  # Przekształcenie wartości na zakres od 0.1 do 3.0
        # Aktualizacja zoomu w modelu obrazu
        active_image = self.project.get_img_by_filename(self.view.file_list_widget.currentItem().text())
        if active_image is not None:
            active_image.zoom_change(zoom_value)

        self.view.apply_zooming(zoom_value)

    def increase_zoom(self):
        current_item = self.view.file_list_widget.currentItem()
        if current_item:
            active_image = self.project.get_img_by_filename(current_item.text())
            if active_image:
                active_image.zoom = min(active_image.zoom + 0.1, 5.0)  # Limit zoom to 500%
                self.view.zoom_image_slider.setValue(int(active_image.zoom * 100))
                self.view.apply_zooming(active_image.zoom)

    def decrease_zoom(self):
        current_item = self.view.file_list_widget.currentItem()
        if current_item:
            active_image = self.project.get_img_by_filename(current_item.text())
            if active_image:
                active_image.zoom = max(active_image.zoom - 0.1, 0.1)  # Minimum zoom 10%
                self.view.zoom_image_slider.setValue(int(active_image.zoom * 100))
                self.view.apply_zooming(active_image.zoom)
