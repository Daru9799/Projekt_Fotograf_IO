from PyQt5.QtWidgets import QFileDialog
#Modele
from model.ProjectModel import ProjectModel
from model.ImageModel import ImageModel
from model.ClassModel import ClassModel
#Podprezentery
from presenter.FileListPresenter import FileListPresenter
from presenter.ClassManagerPresenter import ClassManagerPresenter
from presenter.RectanglePresenter import RectanglePresenter

#Głowny prezenter który jest przekazywany widokowi
class Presenter:
    def __init__(self, view):
        self.view = view
        self.new_project = ProjectModel(None)
        self.drawing_tool = None  # Aktywne narzędzie rysowania (w przypadku braku ustawiamy na None) Dostępne opcje: "rectangle"
        self.start_point = (None, None) #Punkt początkowy (potrzebne do rectangle)
        # Podprezentery?
        self.file_list_presenter = FileListPresenter(None)
        self.classManagerPresenter = ClassManagerPresenter(None,self.new_project)
        self.rectangle_presenter = RectanglePresenter(None)

    def update_view(self, view):
        self.view = view
        # Aktualizacja widokow w podprezeterach (WAZNE! NALEZY ZAWSZE DODAC TUTAJ NOWY PODPREZENTER)
        self.file_list_presenter.view=view
        self.classManagerPresenter.view = view
        self.rectangle_presenter.view = view

    #Utworzenie nowego projektu, wczytanie danych do modelu
    def create_new_project(self):
        folder_path = QFileDialog.getExistingDirectory(self.view.centralwidget.parent(), "Wybierz folder ze zdjęciami")
        if folder_path:
            self.new_project.folder_path = folder_path
            print(f'Wybrano: {self.new_project.folder_path}') #W ramach testów zeby podejrzeć jaką ściezke przesyła
            self.new_project.load_images() #Zaladowanie zdjec do modelu

            #Lista plików aktualizacja w podprezenterze
            self.file_list_presenter.update_project(self.new_project)
            self.file_list_presenter.load_files_to_widget()
        else:
            #Mozna to potem jakos obsluzyc i gdzies wyswietlac (moze tam gdzie info o rozmiarze?)
            print("Nie wybrano folderu.")

    #Wysylam do podprezentera prosbe o aktualizacje
    def folder_list_on_click(self, item):
        self.file_list_presenter.show_image(item)

    #Aktywacja bądź dezaktywacja narzędzia rectangle
    def activate_rectangle_tool(self):
        if self.drawing_tool != "rectangle":
            self.drawing_tool = "rectangle"
            self.view.set_notification_label("Tryb rysowania prostokąta aktywny")
        else:
            self.drawing_tool = None
            self.view.set_notification_label("Brak aktywnego narzędzia")

    # Aktywacja bądź dezaktywacja narzędzia polygon
    def activate_polygon_tool(self):
        if self.drawing_tool != "polygon":
            self.drawing_tool = "polygon"
            self.view.set_notification_label("Tryb rysowania poligona aktywny")
        else:
            self.drawing_tool = None
            self.view.set_notification_label("Brak aktywnego narzędzia")

    #Obsluga klikniecia myszy w obszar obrazka (dostaje współrzędne kliknięcia x i y)
    def handle_mouse_click(self, x, y):
        print(f"Współrzędne kliknięcia: x={x}, y={y}")
        #Tutaj mozna obsłużyć logike jesli chodzi o rysowanie i moze przekazywac to do rectangle presenter?
        if self.drawing_tool == "rectangle":
            if self.start_point == (None, None):
                self.start_point = (x, y)
                self.view.set_notification_label(f"Rysowanie prostokąta. Wybrano punkt początkowy {int(x)}, {int(y)}. Proszę wybrać punkt końcowy")
                self.rectangle_presenter.draw_first_point(x, y)
            else:
                self.view.set_notification_label(f"Pomyślnie narysowano prostokąt!")
                self.rectangle_presenter.draw_rectangle(self.start_point[0], self.start_point[1], x, y)
                self.start_point = (None, None)
        if self.drawing_tool == "polygon":
            self.view.set_notification_label(f"Rysowanie poligona: ")

    #Aktualizacja zooma
    def zoom_slider(self):
        #Jeśli nie ma obrazka to nic nie rób
        if self.new_project.list_of_images_model:
            self.file_list_presenter.on_zoom_slider_changed()


