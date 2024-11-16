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
        self.drawing_tool = None  #Aktywne narzędzie rysowania (w przypadku braku ustawiamy na None) Dostępne opcje: "rectangle", "polygon"
        #Podprezentery do obsługi poszczególnych modułów aplikacji
        self.file_list_presenter = FileListPresenter(None)
        self.classManagerPresenter = ClassManagerPresenter(None,self.new_project)
        self.rectangle_presenter = RectanglePresenter(None)

    #Aktualizacja widokow w podprezeterach (WAZNE! NALEZY ZAWSZE DODAC TUTAJ NOWY PODPREZENTER)
    def update_view(self, view):
        self.view = view
        self.file_list_presenter.view = view
        self.classManagerPresenter.view = view
        self.rectangle_presenter.view = view

    #Utworzenie nowego projektu, wczytanie danych do modelu
    def create_new_project(self):
        folder_path = QFileDialog.getExistingDirectory(self.view.centralwidget.parent(), "Wybierz folder ze zdjęciami")
        if folder_path:
            self.new_project.folder_path = folder_path
            self.new_project.load_images() #Zaladowanie zdjec do modelu
            #Lista plików aktualizacja w podprezenterze
            self.file_list_presenter.update_project(self.new_project)
            self.file_list_presenter.load_files_to_widget()
        else:
            self.view.set_notification_label("Nie wybrano folderu.")

    #Aktualizacja sceny po zmianie obrazka w liście po prawej stronie
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

    #Aktualizacja zooma
    def zoom_slider(self):
        if self.new_project.list_of_images_model: #Jeśli nie ma obrazka to nic nie rób
            self.file_list_presenter.on_zoom_slider_changed()

    #Obsluga klikniecia myszy w obszar obrazka (dostaje współrzędne kliknięcia x i y)
    def handle_mouse_click(self, x, y):
        print(f"Współrzędne kliknięcia: x={x}, y={y}")
        #Logika rysowania prostokąta
        if self.drawing_tool == "rectangle":
            if self.rectangle_presenter.rectangle_start_point == (None, None):
                self.rectangle_presenter.update_start_point(x, y)
                self.view.set_notification_label(f"Rysowanie prostokąta. Wybrano punkt początkowy {int(x)}, {int(y)}. Proszę wybrać punkt końcowy")
            else:
                points = self.rectangle_presenter.get_rectangle_points()
                self.view.set_notification_label(f"Pomyślnie narysowano prostokąt! Jego współrzędne to: " + str(points))
                #self.rectangle_presenter.delete_temp_rectangle() #Usunięcie tymczasowego obiektu
                ###Tutaj trzeba obsłużyć wysyłanie prośby o dodanie adnotacji i update sceny z nowym narysowanym obiektem (narysować go ponownie z innymi)
                self.rectangle_presenter.update_start_point(None, None)

        #Logika rysowania poligona
        if self.drawing_tool == "polygon":
            self.view.set_notification_label(f"Rysowanie poligona: ")

    #Obsluga przesuwania myszy w obrębie obszaru obrazka (współrzędne zawsze odnoszą się do obrazka nie całego graphic_view)
    def handle_mouse_move(self, x, y):
        x, y = int(x), int(y) #Zamiana współrzędnych na wartości int
        #Obsługa przesunięcia podczas rysowania prostokąta
        if self.rectangle_presenter.rectangle_start_point != (None, None):
            self.rectangle_presenter.delete_temp_rectangle() #usuwa poprzedni cień
            print("siema jesteś tu: " + str(x) + ", " + str(y))
            self.rectangle_presenter.draw_rectangle(self.rectangle_presenter.rectangle_start_point[0], self.rectangle_presenter.rectangle_start_point[1], x, y)




