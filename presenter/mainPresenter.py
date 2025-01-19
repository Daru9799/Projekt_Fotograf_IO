import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

#Modele
from model.ProjectModel import ProjectModel
from model.AnnotationModel import AnnotationModel
from model.ImageModel import ImageModel
from model.ClassModel import ClassModel
from presenter.ClassGeneratorPresenter import ClassGeneratorPresenter
from random import randrange

#Podprezentery
from presenter.FileListPresenter import FileListPresenter
from presenter.ClassManagerPresenter import ClassManagerPresenter
from presenter.RectanglePresenter import RectanglePresenter
from presenter.AnnotationPresenter import AnnotationPreseter
from presenter.PolygonPresenter import PolygonPresenter
from presenter.ScenePreseter import ScenePresenter
from presenter.ImportFromFile import ImportFromFile
from presenter.ExportToCoco import ExportToCoco
from presenter.LocalAutoSegmentationPresenter import LocalAutoSegmentationPresenter
from view.ExifWindowView import ExifWindow
from presenter.ExportProject import ExportProject
from presenter.ExportToYolo import ExportToYolo
from presenter.StatisticsPresenter import StatisticsPresenter
from view.ClassGeneratorWindowView import ClassGeneratorWindowView

# Mirzenie czasu działa kodu:
import time

#Głowny prezenter który jest przekazywany widokowi
class Presenter:
    def __init__(self, view):
        self.view = view
        self.new_project = ProjectModel(None)
        self.drawing_tool = None  #Aktywne narzędzie rysowania (w przypadku braku ustawiamy na None) Dostępne opcje: "rectangle", "polygon"
        self.image_item = None #Aktywne zdjęcie w liście po prawej
        self.class_generator_window = None

        #Podprezentery do obsługi poszczególnych modułów aplikacji
        self.file_list_presenter = FileListPresenter(None, self)
        self.classManagerPresenter = ClassManagerPresenter(None,self.new_project,self)
        self.rectangle_presenter = RectanglePresenter(None, self)
        self.polygon_presenter = PolygonPresenter(None, self)
        self.annotation_presenter = AnnotationPreseter(None, self, self.new_project)
        self.scene_presenter = ScenePresenter(None,self,self.new_project)

        start_time = time.time()
        self.local_auto_segm_presenter = LocalAutoSegmentationPresenter(None,self)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Czas inicjalizacji LocalAutoSegmentationPresenter: {execution_time:.5f} sekund")

        self.import_from_file = ImportFromFile(None)
        self.export_to_file = ExportToCoco(None, self.new_project)
        self.export_project=ExportProject(None,self.new_project)
        self.export_to_yolo=ExportToYolo(None,self.new_project)

        start_time = time.time()
        self.statistics_presenter = StatisticsPresenter(None, self.new_project, self)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Czas inicjalizacji StatisticsPresenter: {execution_time:.5f} sekund")

        self.class_generator_presenter = ClassGeneratorPresenter(None)


    #Aktualizacja widokow w podprezeterach (WAZNE! NALEZY ZAWSZE DODAC TUTAJ NOWY PODPREZENTER)
    def update_view(self, view):
        self.view = view
        self.file_list_presenter.view = view
        self.classManagerPresenter.view = view
        self.rectangle_presenter.view = view
        self.polygon_presenter.view = view
        self.annotation_presenter.view = view
        self.scene_presenter.view = view
        self.local_auto_segm_presenter.view = view
        self.import_from_file.view = view
        self.export_to_file.view= view
        self.export_project.view = view
        self.export_to_yolo.view=view
        self.statistics_presenter.view = view
        self.classManagerPresenter.updateItems()
        self.view.toggle_all_buttons(False)
        self.class_generator_presenter.view = view


        # !!!
        # Linia poniżej finalnie do usunięcia
        # self.create_new_project()
        # !!!

    #Utworzenie nowego projektu, wczytanie danych do modelu
    def create_new_project(self):
        # !!!
        # linie poniżej odkomentować
        folder_path = QFileDialog.getExistingDirectory(self.view.centralwidget.parent(), "Wybierz folder ze zdjęciami")
        # linie poniżej też usunąć
        # folder_path = "./!OBRAZKI DO TESTÓW"
        # !!!
        if self.new_project.list_of_images_model:
            confirmation = self.view.show_message_Yes_No("Uwaga!", "Wczytanie nowego folderu spowoduje utratę wszystkich niezapisanych danych. Czy chcesz kontynuować?")
            if confirmation:
                if folder_path:
                    self.update_model_after_loading_new_project(folder_path)
                    self.update_file_list_panel()
                    self.update_annotations_on_image()
                    self.view.statistics_menu.setEnabled(True)
                    self.view.toggle_all_buttons(True)
                else:
                    self.view.set_notification_label("Nie wybrano folderu.")
        else:
            if folder_path:
                self.update_model_after_loading_new_project(folder_path)
                self.update_file_list_panel()
                self.update_annotations_on_image()
                self.view.statistics_menu.setEnabled(True)
                self.view.toggle_all_buttons(True) # "Włączenie" przycisków

    #Ta funkcja ma za zadanie przypisać projektowi odnośnik do folderu ze zdjęciami, a także zaladować nowe zdjęcia do modelu
    def update_model_after_loading_new_project(self, folder_path):
        self.new_project.folder_path = folder_path
        #print("Ścieżka do folderu: " + self.new_project.folder_path)
        self.new_project.load_images()  # Zaladowanie zdjec do modelu

        # Przypisanie pierwszego pokazanego zdjęcia do image_item
        #self.image_item = self.new_project.get_img_by_filename(self.new_project.list_of_images_model[0].filename)

    def update_annotations_on_image(self):
        self.annotation_presenter.update_items()
        self.scene_presenter.reset_to_default()
        self.scene_presenter.get_annotations_from_project()  # Pobranie adnotacji do rysowania
        self.scene_presenter.draw_annotations()  # Rysowanie wczytanych adnotacji

    def update_file_list_panel(self):
        # Lista plików aktualizacja w podprezenterze
        self.file_list_presenter.update_project(self.new_project)
        self.file_list_presenter.load_files_to_widget()

    #Aktualizacja sceny po zmianie obrazka w liście po prawej stronie
    def folder_list_on_click(self, item):
        self.rectangle_presenter.cancel_drawing_rectangle()     #Anulowanie rysowania prostokąta po kliknięciu w prawy panel
        self.polygon_presenter.prepare_to_change_current_img()         #Anulowanie rysowania polygona --//--
        self.local_auto_segm_presenter.cancel_auto_segmentation()
        self.drawing_tool = None
        self.view.set_no_active_tool_text()
        if self.image_item != item:
            self.file_list_presenter.show_image(item)
            self.annotation_presenter.update_items()
            self.image_item = item

            self.scene_presenter.reset_to_default()
            #self.scene_presenter.refresh()           # Rysowanie wczytanych adnotacji


    #Aktywacja bądź dezaktywacja narzędzia rectangle
    def activate_rectangle_tool(self):
        if self.drawing_tool != "rectangle":
            self.scene_presenter.reset_selected_polygon()

            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
            self.local_auto_segm_presenter.cancel_auto_segmentation()
            self.drawing_tool = "rectangle"
            self.view.set_notification_label("Tryb rysowania prostokąta aktywny. Wybierz punkt początkowy LPM.")
            self.view.set_draw_rectangle_button_text("Anuluj rysowanie prostokąta")
            self.view.change_to_cross_cursor()
        else:
            self.drawing_tool = None
            self.view.set_no_active_tool_text()
            self.rectangle_presenter.cancel_drawing_rectangle()

    # Aktywacja bądź dezaktywacja narzędzia polygon
    def activate_polygon_tool(self):
        if self.drawing_tool != "polygon":
            self.scene_presenter.reset_selected_polygon()

            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
            self.local_auto_segm_presenter.cancel_auto_segmentation()
            self.drawing_tool = "polygon"
            self.view.set_notification_label("Tryb rysowania poligona aktywny")
            self.view.set_draw_polygon_button_text("Anuluj rysowanie poligona")
            self.view.change_to_cross_cursor()
        else:
            self.drawing_tool = None
            self.view.set_no_active_tool_text()
            self.polygon_presenter.cancel_drawing_polygon()

    def activate_auto_selection_tool(self):
        if self.drawing_tool != "auto_segmentation":
            self.scene_presenter.reset_selected_polygon()

            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
            self.local_auto_segm_presenter.cancel_auto_segmentation()

            self.drawing_tool = "auto_segmentation"
            self.view.set_notification_label("Tryb automatycznego zaznaczania aktywny")
            self.view.set_auto_selection_button_text("Anuluj automatyczne zaznaczanie")
            self.view.change_to_cross_cursor()
        else:
            self.drawing_tool = None
            self.view.set_no_active_tool_text()
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.local_auto_segm_presenter.cancel_auto_segmentation()


    #Aktualizacja zooma
    def zoom_slider(self):
        if self.new_project.list_of_images_model: #Jeśli nie ma obrazka to nic nie rób
            self.file_list_presenter.on_zoom_slider_changed()

    def zoom_value(self):
        if self.new_project.list_of_images_model:  # Jeśli nie ma obrazka to nic nie rób
            self.file_list_presenter.on_zoom_value_changed()


    #Obsluga klikniecia myszy w obszar obrazka (dostaje współrzędne kliknięcia x i y)
    def handle_mouse_click(self, x, y):
        print(f"Współrzędne kliknięcia: x={x}, y={y}")
        selected_class = self.view.get_selected_class()

        #Logika rysowania prostokąta
        if self.drawing_tool == "rectangle":
            if self.rectangle_presenter.rectangle_start_point == (None, None):
                if selected_class:
                    self.rectangle_presenter.update_start_point(x, y)
                    self.rectangle_presenter.update_color(selected_class.Class.color)
                    self.view.set_notification_label(f"Rysowanie prostokąta. Wybrano punkt początkowy. Proszę wybrać punkt końcowy LPM.")
                else:
                    self.view.show_message_OK("Informacja", "Proszę o wybranie klasy")
            else:
                points = self.rectangle_presenter.get_rectangle_points()
                print(f"Pomyślnie narysowano prostokąt! Jego współrzędne to: " + str(points))
                self.view.set_notification_label(f"Pomyślnie utworzono nową adnotację! Tryb rysowania prostokąta aktywny. Wybierz punkt początkowy LPM.")
                self.rectangle_presenter.delete_temp_rectangle() #Usunięcie tymczasowego obiektu

                self.annotation_presenter.add_annotation(points)
                self.scene_presenter.get_annotations_from_project()  # Pobranie adnotacji do rysowania
                self.scene_presenter.draw_annotations()  # Rysowanie wczytanych adnotacji

                ###Tutaj trzeba obsłużyć update sceny z nowym narysowanym obiektem (narysować go ponownie z innymi)
                self.rectangle_presenter.update_start_point(None, None)

        #Logika rysowania poligona
        elif self.drawing_tool == "polygon":

            if not selected_class: # sprawdzenie czy klasa jest wybrana
                self.view.show_message_OK("Informacja", "Proszę o wybranie klasy")
                return

            self.view.set_notification_label(f"Rysowanie poligona: ")
            self.polygon_presenter.update_color(selected_class.Class.color) # update koloru

            # jeśli plolygon ma conajmniej 3 punkty i klikneliśmy obok współżendnych początkowych
            if len(self.polygon_presenter.current_polygon_points) > 2 and self.polygon_presenter.is_near_starting_point(x, y):
                self.polygon_presenter.polygon_closed = True
                self.polygon_presenter.drawing_polygon()
                points = self.polygon_presenter.current_polygon_points
                self.annotation_presenter.add_annotation(points) # dodajemy wielokąt do listy adnotacji
                self.polygon_presenter.current_polygon_points.clear()
                self.polygon_presenter.polygon_closed = False
                self.polygon_presenter.drawing_polygon()                  # usuwa narysowany, zamknięty poligon

                self.scene_presenter.get_annotations_from_project()       # Pobranie adnotacji do rysowania
                self.scene_presenter.draw_annotations()                   # Rysowanie wczytanych adnotacji
            else:
                self.polygon_presenter.current_polygon_points.append((int(x),int(y)))
                self.polygon_presenter.drawing_polygon()

        elif self.drawing_tool == "auto_segmentation":

            if self.rectangle_presenter.rectangle_start_point == (None, None):
                if selected_class:
                    self.rectangle_presenter.update_start_point(x, y)
                    self.rectangle_presenter.update_color(selected_class.Class.color)
                    self.view.set_notification_label(f"Automatyczne zaznaczanie: Wybrano punkt początkowy. Proszę wybrać punkt końcowy LPM.")
                else:
                    self.view.show_message_OK("Informacja", "Proszę o wybranie klasy")
            else:
                points = self.rectangle_presenter.get_rectangle_points()
                self.view.set_notification_label(f"Automatyczne zaznaczanie: Wybierz punkt początkowy LPM.")
                self.rectangle_presenter.delete_temp_rectangle() #Usunięcie tymczasowego obiektu

                image_path = self.new_project.folder_path+"/"+self.image_item.text()
                self.local_auto_segm_presenter.image_path = image_path
                self.local_auto_segm_presenter.calculate_vertexes(image_path, points)

                self.scene_presenter.get_annotations_from_project()  # Pobranie adnotacji do rysowania
                self.scene_presenter.draw_annotations()  # Rysowanie wczytanych adnotacji

                ###Tutaj trzeba obsłużyć update sceny z nowym narysowanym obiektem (narysować go ponownie z innymi)
                self.rectangle_presenter.update_start_point(None, None)


        elif self.drawing_tool is None:
            self.scene_presenter.active_dragging(int(x), int(y))
            self.scene_presenter.draw_annotations()  # Odświerzenie widoku


    #Obsluga przesuwania myszy w obrębie obszaru obrazka (współrzędne zawsze odnoszą się do obrazka nie całego graphic_view)
    def handle_mouse_move(self, x, y):
        x, y = int(x), int(y) #Zamiana współrzędnych na wartości int
        #Obsługa przesunięcia podczas rysowania prostokąta
        if self.rectangle_presenter.rectangle_start_point != (None, None):
            self.rectangle_presenter.delete_temp_rectangle() #usuwa poprzedni cień
            self.rectangle_presenter.draw_rectangle(self.rectangle_presenter.rectangle_start_point[0], self.rectangle_presenter.rectangle_start_point[1], x, y)
        if self.drawing_tool == "polygon":
            self.polygon_presenter.set_cursor_pos(x,y)
        if self.drawing_tool is None:
            self.scene_presenter.dragging_move(x,y)

    def handle_mouse_left_click_release(self):
        self.scene_presenter.release_dragging_click()
        items = [self.view.annotation_list_widget.item(i) for i in range(self.view.annotation_list_widget.count())]
        for i in items:
            i.setSelected(False)  # Na początku odznacz
            custom_i = self.view.annotation_list_widget.itemWidget(i)
            if custom_i.getAnnotation().get_segmentation() == self.scene_presenter.get_seleted_polygon():
                i.setSelected(True)

    def handle_escape_click(self):
        self.rectangle_presenter.cancel_drawing_rectangle()
        self.polygon_presenter.cancel_drawing_polygon()
        self.local_auto_segm_presenter.cancel_auto_segmentation()
        self.drawing_tool = None
        self.view.set_no_active_tool_text()

    def handle_enter_click(self):
        if self.drawing_tool == "auto_segmentation" and len(self.local_auto_segm_presenter.temp_segment) != 0:
            self.annotation_presenter.add_annotation(self.local_auto_segm_presenter.temp_segment)
            self.local_auto_segm_presenter.remove_temp_segment()
            self.view.set_notification_label(f"Automatyczne zaznaczanie: Wybierz punkt początkowy LPM.")
            self.scene_presenter.get_annotations_from_project()  # Pobranie adnotacji do rysowania
            self.scene_presenter.draw_annotations()              # Rysowanie wczytanych adnotacji

    def handle_crtl_minus(self):
        self.file_list_presenter.decrease_zoom()

    def handle_crtl_plus(self):
        self.file_list_presenter.increase_zoom()

    def handle_scroll_up(self):
        self.file_list_presenter.increase_zoom()

    def handle_scroll_down(self):
        self.file_list_presenter.decrease_zoom()

    #Funkcja odpowiedzialna za przekazanie informacji exif do okna, które wyświetla je i otworzenie tego okna
    def open_exif_window(self):
        selected_image_name = self.view.get_selected_image()
        img_obj = self.new_project.get_img_by_filename(selected_image_name)
        if selected_image_name is not None:
            exif_data = img_obj.exif_obj
            if exif_data is not None:
                self.exif_window = ExifWindow(exif_data, selected_image_name)
                self.exif_window.exec_()
        else:
            self.view.show_message_OK("Informacja", "Proszę wybrać obraz z listy.")

    def import_from_coco(self):
        # Wyłączenie wszystkich narzędzi do adnotacji:
        self.drawing_tool = None
        self.view.set_no_active_tool_text()
        if self.new_project.folder_path:
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
        self.local_auto_segm_presenter.cancel_auto_segmentation()

        if self.new_project.list_of_images_model:
            confirmation = self.view.show_message_Yes_No("Uwaga!", "Import spowoduje utratę wszystkich niezapisanych danych. Czy chcesz kontynuować?")
            if confirmation:
                img_list, class_list, json_folder = self.import_from_file.import_from_COCO()
            else:
                return 0
        else:
            img_list, class_list, json_folder = self.import_from_file.import_from_COCO()

        #Anulowanie importu poprzez zamkniecie
        if img_list is None or class_list is None or json_folder is None:
            return 0

        ##Przypisywanie obrazków i klas do listy projektowej
        self.new_project.list_of_images_model = img_list
        self.new_project.list_of_classes_model = class_list
        #Aktualizacja widoku
        self.view.statistics_menu.setEnabled(True)
        self.view.toggle_all_buttons(True)
        self.new_project.folder_path = os.path.join(json_folder, "images")
        self.classManagerPresenter.updateItems() #aktualizuje panel z listą klas
        self.update_file_list_panel()
        self.update_annotations_on_image()

        ##Czyszczenie prezentera importu po zakonczeniu dzialania
        self.import_from_file.reset_imported_data()

    def import_from_yolo(self):
        self.drawing_tool = None
        self.view.set_no_active_tool_text()
        if self.new_project.folder_path:
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
        self.local_auto_segm_presenter.cancel_auto_segmentation()

        if self.new_project.list_of_images_model:
            confirmation = self.view.show_message_Yes_No("Uwaga!", "Import spowoduje utratę wszystkich niezapisanych danych. Czy chcesz kontynuować?")
            if confirmation:
                print("Pobranie list")
                img_list, class_list, yaml_folder = self.import_from_file.import_from_YOLO()
            else:
                return 0
        else:
            print("Pobranie list")
            img_list, class_list, yaml_folder = self.import_from_file.import_from_YOLO()

        # Anulowanie importu poprzez zamkniecie
        if img_list is None or class_list is None or yaml_folder is None:
            return 0

        ##Przypisywanie obrazków i klas do listy projektowej
        self.new_project.list_of_images_model = img_list
        self.new_project.list_of_classes_model = class_list
        # Aktualizacja widoku
        self.view.statistics_menu.setEnabled(True)
        self.view.toggle_all_buttons(True)
        self.new_project.folder_path = os.path.join(yaml_folder, "train\images")
        self.classManagerPresenter.updateItems()  # aktualizuje panel z listą klas
        self.update_file_list_panel()
        self.update_annotations_on_image()

        ##Czyszczenie prezentera importu po zakonczeniu dzialania
        self.import_from_file.reset_imported_data()

    def import_project(self):
        # Wyłączenie wszystkich narzędzi do adnotacji:
        self.export_project.unlock_file()
        self.drawing_tool = None
        self.view.set_no_active_tool_text()
        if self.new_project.folder_path:
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
        self.local_auto_segm_presenter.cancel_auto_segmentation()

        if self.new_project.list_of_images_model:
            confirmation = self.view.show_message_Yes_No("Uwaga!", "Import spowoduje utratę wszystkich niezapisanych danych. Czy chcesz kontynuować?")
            if confirmation:
                img_list, class_list, image_folder = self.import_from_file.import_from_project_file()
            else:
                return 0
        else:
            img_list, class_list, image_folder = self.import_from_file.import_from_project_file()

        # Anulowanie importu poprzez zamkniecie
        if img_list is None or class_list is None or image_folder is None:
            return 0
        ##Przypisywanie obrazków i klas do listy projektowej
        self.new_project.list_of_images_model = img_list
        self.new_project.list_of_classes_model = class_list
        # Aktualizacja widoku
        self.view.statistics_menu.setEnabled(True)
        self.view.toggle_all_buttons(True)
        self.new_project.folder_path = image_folder #Przypisanie sciezki
        self.classManagerPresenter.updateItems()  # aktualizuje panel z listą klas
        self.update_file_list_panel()
        self.update_annotations_on_image()

        ##Czyszczenie prezentera importu po zakonczeniu dzialania
        self.import_from_file.reset_imported_data()
        self.export_project.project_path=self.import_from_file.project_path

        self.export_project.lock_file(self.export_project.project_path)

    #Stąd przekazanie importów/eksportów do podprezenterów
    def save_as_project_fun(self):
        # Wyłączenie wszystkich narzędzi do adnotacji:
        if self.new_project.list_of_images_model:
            self.drawing_tool = None
            self.view.set_no_active_tool_text()
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
            self.local_auto_segm_presenter.cancel_auto_segmentation()

            # 1. Wybierz lokalizację zapisu
            save_path = self.export_project.select_save_location()
            if not save_path:
                # self.view.show_message_OK("Błąd", "Nie wybrano lokalizacji zapisu.")
                return

            if not save_path.endswith(".pro"):
                save_path += ".pro"

            # 3. Utwórz i zapisz dane do pliku .pro (JSON)
            try:
                self.export_project.create_file(save_path)
                self.export_project.lock_file(save_path)
                self.update_file_list_panel()
                self.update_annotations_on_image()
                self.view.show_message_OK("Sukces", f"Projekt został wyeksportowany do {save_path}")
            except Exception as e:
                self.view.show_message_OK("Błąd", f"Wystąpił problem podczas eksportu: {str(e)}")
        else:
            self.view.show_message_OK("Błąd", "Brak danych do zapisu")

    def save_project_fun(self):
        if self.new_project.list_of_images_model:
            self.drawing_tool = None
            self.view.set_no_active_tool_text()
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.polygon_presenter.cancel_drawing_polygon()
            self.local_auto_segm_presenter.cancel_auto_segmentation()
            # Zapisz zmiany w istniejącej lokalizacji lub otwórz okno wyboru, jeśli brak lokalizacji
            try:
                if self.export_project.save_project():
                    self.update_file_list_panel()
                    self.update_annotations_on_image()
                    self.view.show_message_OK("Sukces", f"Projekt został zapisany do {self.export_project.project_path}")
                self.export_project.lock_file(self.export_project.project_path)

                # else:
                #     self.view.show_message_OK("Błąd", "Nie wybrano lokalizacji zapisu.")
            except Exception as e:
                self.view.show_message_OK("Błąd", f"Wystąpił problem podczas zapisu: {str(e)}")
        else:
            self.view.show_message_OK("Błąd", "Brak danych do zapisu")

    def export_to_coco_fun(self):
        # Wyłączenie wszystkich narzędzi do adnotacji:
        self.drawing_tool = None
        self.view.set_no_active_tool_text()
        self.rectangle_presenter.cancel_drawing_rectangle()
        self.polygon_presenter.cancel_drawing_polygon()
        self.local_auto_segm_presenter.cancel_auto_segmentation()

        # Sprawdzenie, czy istnieją adnotacje w projekcie
        annotations_exist = any(
            img.list_of_annotations for img in self.new_project.list_of_images_model
        )
        if not annotations_exist:
            self.view.show_message_OK("Błąd", "Brak adnotacji do eksportu.")
            return

        if self.new_project.list_of_images_model:
            # 1. Wybierz lokalizację zapisu
            save_path = self.export_to_file.select_save_location()
            if not save_path:
                return

            # 2. Utwórz strukturę folderów i pobierz ścieżkę do pliku JSON
            json_file_path = self.export_to_file.create_folder_structure(save_path)

            # 3. Eksportuj obrazy
            folder_path = os.path.dirname(json_file_path)
            self.export_to_file.export_images(folder_path)

            # 4. Utwórz i zapisz dane JSON
            self.export_to_file.create_json_file(json_file_path)
            self.update_file_list_panel()
            self.update_annotations_on_image()
            normalized_path = os.path.normpath(folder_path).replace("\\", "/")
            self.view.show_message_OK("Sukces", f"Projekt został wyeksportowany do {normalized_path}")
        else:
            self.view.show_message_OK("Błąd", "Brak danych do eksportu.")

    def export_to_yolo_fun(self):
        # Wyłączenie wszystkich narzędzi do adnotacji:
        self.drawing_tool = None
        self.view.set_no_active_tool_text()
        self.rectangle_presenter.cancel_drawing_rectangle()
        self.polygon_presenter.cancel_drawing_polygon()
        self.local_auto_segm_presenter.cancel_auto_segmentation()

        annotations_exist = any(
            img.list_of_annotations for img in self.new_project.list_of_images_model
        )
        if not annotations_exist:
            self.view.show_message_OK("Błąd", "Brak adnotacji do eksportu.")
            return

        if self.new_project.list_of_images_model:
            save_path= self.export_to_yolo.select_save_location()
            if not save_path:
                # self.view.show_message_OK("Błąd", "Nie wybrano lokalizacji zapisu.")
                return

            self.export_to_yolo.create_folder_structure(save_path)
            self.export_to_yolo.export_images(save_path)
            self.export_to_yolo.create_yaml_file(save_path)
            self.update_file_list_panel()
            self.update_annotations_on_image()
            self.view.show_message_OK("Sukces", f"Projekt został wyeksportowany do {save_path}")
        else:
            self.view.show_message_OK("Błąd", "Brak danych do eksportu")

    #Generowanie klas dla zaznaczonego obrazka
    def generate_classes(self):
        self.class_generator_presenter.load_key_and_endpoint()
        self.class_generator_presenter.create_client()
        if self.class_generator_presenter.vision_client is None:
            self.view.show_message_OK("Uwaga!", "Połączenie z chmurą jest niedostępne, sprawdź połączenie internetowe lub skontaktuj się z administratorem.")
            return 0
        self.class_generator_window = ClassGeneratorWindowView(self)
        self.class_generator_window.exec_()

    def handle_create_tags_click(self, language, min_accuracy):
        # Tutaj trzeba ustawic w class generator presenterze zmienną obrazka na aktualnei zaznaczony (jego ścieżke)
        selected_img_name = self.view.get_selected_image()
        self.class_generator_presenter.img_path = os.path.join(self.new_project.folder_path, selected_img_name)
        tag_dict = self.class_generator_presenter.generate_tags(language, min_accuracy)
        self.class_generator_window.tags = tag_dict

    def create_classes_from_tags(self, selected_items):
        for name, color in selected_items:
            uniqueId = randrange(1000000, 9999999)
            isUnique = False
            # Generowanie unikatowego id
            while not isUnique:
                isUnique = True
                for c in self.new_project.list_of_classes_model:
                    if c.class_id == uniqueId:
                        uniqueId = randrange(1000000, 9999999)
                        isUnique = False

            class_obj = ClassModel(class_id=uniqueId, name=name, color=color)
            self.new_project.list_of_classes_model.append(class_obj)
        self.classManagerPresenter.updateItems()









