from PyQt5.QtWidgets import QFileDialog
#Modele
from model.ProjectModel import ProjectModel
from model.AnnotationModel import AnnotationModel
from model.ImageModel import ImageModel
from model.ClassModel import ClassModel
#Podprezentery
from presenter.FileListPresenter import FileListPresenter
from presenter.ClassManagerPresenter import ClassManagerPresenter
from presenter.RectanglePresenter import RectanglePresenter
from presenter.AnnotationPresenter import AnnotationPreseter
from presenter.PolygonPresenter import PolygonPresenter

#Głowny prezenter który jest przekazywany widokowi
class Presenter:
    def __init__(self, view):
        self.view = view
        self.new_project = ProjectModel(None)
        self.drawing_tool = None  #Aktywne narzędzie rysowania (w przypadku braku ustawiamy na None) Dostępne opcje: "rectangle", "polygon"
        self.image_item = None #Aktywne zdjęcie w liście po prawej
        #Podprezentery do obsługi poszczególnych modułów aplikacji
        self.file_list_presenter = FileListPresenter(None)
        self.classManagerPresenter = ClassManagerPresenter(None,self.new_project)
        self.rectangle_presenter = RectanglePresenter(None)
        self.polygon_presenter = PolygonPresenter(None)
        self.annotation_presenter = AnnotationPreseter(None)

    #Aktualizacja widokow w podprezeterach (WAZNE! NALEZY ZAWSZE DODAC TUTAJ NOWY PODPREZENTER)
    def update_view(self, view):
        self.view = view
        self.file_list_presenter.view = view
        self.classManagerPresenter.view = view
        self.rectangle_presenter.view = view
        self.polygon_presenter.view = view
        self.annotation_presenter.view = view

        self.classManagerPresenter.updateItems()
        # !!!
        # Linia poniżej finalnie do usunięcia
        self.create_new_project()
        # !!!

    #Utworzenie nowego projektu, wczytanie danych do modelu
    def create_new_project(self):
        # !!!
        # linie poniżej odkomentować
        # folder_path = QFileDialog.getExistingDirectory(self.view.centralwidget.parent(), "Wybierz folder ze zdjęciami")
        # linie poniżej też usunąć
        folder_path = "./!OBRAZKI DO TESTÓW"
        # !!!
        if folder_path:
            self.new_project.folder_path = folder_path
            print("Ścieżka do folderu: "+self.new_project.folder_path)
            self.new_project.load_images()      #Zaladowanie zdjec do modelu

            #Lista plików aktualizacja w podprezenterze
            self.file_list_presenter.update_project(self.new_project)
            self.file_list_presenter.load_files_to_widget()
        else:
            self.view.set_notification_label("Nie wybrano folderu.")

    #Aktualizacja sceny po zmianie obrazka w liście po prawej stronie
    def folder_list_on_click(self, item):
        self.rectangle_presenter.cancel_drawing_rectangle()     #Anulowanie rysowania prostokąta po kliknięciu w prawy panel
        self.polygon_presenter.cancel_drawing_polygon()         #Anulowanie rysowania polygona --//--
        self.drawing_tool = None
        self.view.set_notification_label("Brak aktywnego narzędzia")
        if self.image_item != item:
            self.file_list_presenter.show_image(item)
            self.image_item = item

    #Aktywacja bądź dezaktywacja narzędzia rectangle
    def activate_rectangle_tool(self):
        if self.drawing_tool != "rectangle":
            self.polygon_presenter.cancel_drawing_polygon()
            self.drawing_tool = "rectangle"
            self.view.set_notification_label("Tryb rysowania prostokąta aktywny")
            self.view.set_draw_rectangle_button_text("Anuluj rysowanie prostokąta")
            self.view.change_to_cross_cursor()
        else:
            self.drawing_tool = None
            self.view.set_notification_label("Brak aktywnego narzędzia")
            self.rectangle_presenter.cancel_drawing_rectangle()

    # Aktywacja bądź dezaktywacja narzędzia polygon
    def activate_polygon_tool(self):
        if self.drawing_tool != "polygon":
            self.rectangle_presenter.cancel_drawing_rectangle()
            self.drawing_tool = "polygon"
            self.view.set_notification_label("Tryb rysowania poligona aktywny")
            self.view.set_draw_polygon_button_text("Anuluj rysowanie poligona")
            self.view.change_to_cross_cursor()
        else:
            self.drawing_tool = None
            self.view.set_notification_label("Brak aktywnego narzędzia")
            self.polygon_presenter.cancel_drawing_polygon()

            #Aktualizacja zooma
    def zoom_slider(self):
        if self.new_project.list_of_images_model: #Jeśli nie ma obrazka to nic nie rób
            self.file_list_presenter.on_zoom_slider_changed()

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
                    self.view.set_notification_label(f"Rysowanie prostokąta. Wybrano punkt początkowy {int(x)}, {int(y)}. Proszę wybrać punkt końcowy")
                else:
                    self.view.show_message_OK("Informacja", "Proszę o wybranie klasy")
            else:
                points = self.rectangle_presenter.get_rectangle_points()
                self.view.set_notification_label(f"Pomyślnie narysowano prostokąt! Jego współrzędne to: " + str(points))
                self.rectangle_presenter.delete_temp_rectangle() #Usunięcie tymczasowego obiektu
                self.annotation_presenter.add_annotation(points, self.new_project)
                ###Tutaj trzeba obsłużyć update sceny z nowym narysowanym obiektem (narysować go ponownie z innymi)
                self.rectangle_presenter.update_start_point(None, None)

        #Logika rysowania poligona
        if self.drawing_tool == "polygon":
            self.view.set_notification_label(f"Rysowanie poligona: ")

            if not selected_class: # sprawdzenie czy klasa jest wybrana
                self.view.show_message_OK("Informacja", "Proszę o wybranie klasy")
                return

            self.polygon_presenter.update_color(selected_class.Class.color) # update koloru
            if not self.polygon_presenter.polygon_closed:
                # jeśli plolygon ma conajmniej 3 punkty i klikneliśmy obok współżendnych początkowych
                if len(self.polygon_presenter.current_polygon_points) > 2 and self.polygon_presenter.is_near_starting_point(x, y):
                    self.polygon_presenter.polygon_closed = True
                    self.polygon_presenter.current_polygon_points.append((int(x), int(y)))
                    self.polygon_presenter.drawing_polygon()

                    points = self.polygon_presenter.current_polygon_points
                    self.annotation_presenter.add_annotation(points, self.new_project) # dodajemy wielokąt do listy adnotacji

                    # self.polygon_presenter.current_polygon_points.clear()   # do odkomentowania potem
                    # self.polygon_presenter.polygon_closed = False             # do odkomentowania potem
                else:
                    self.polygon_presenter.current_polygon_points.append((int(x),int(y)))
                    self.polygon_presenter.drawing_polygon()
            else:
                # Tymczasowe,testowe: sprawdzanie czy kliknięty punkt znajduje się obszarze polygona
                result = self.polygon_presenter.check_inclusion(int(x),int(y))
                if result > 0:
                    print("Punkt znajduje się wewnątrz wielokąta.")
                elif result == 0:
                    print("Punkt znajduje się na krawędzi wielokąta.")
                else:
                    print("Punkt znajduje się na zewnątrz wielokąta.")
                    self.polygon_presenter.current_polygon_points.clear()   # do odkomentowania potem
                    self.polygon_presenter.polygon_closed = False
                    self.polygon_presenter.drawing_polygon()




    #Obsluga przesuwania myszy w obrębie obszaru obrazka (współrzędne zawsze odnoszą się do obrazka nie całego graphic_view)
    def handle_mouse_move(self, x, y):
        x, y = int(x), int(y) #Zamiana współrzędnych na wartości int
        #Obsługa przesunięcia podczas rysowania prostokąta
        if self.rectangle_presenter.rectangle_start_point != (None, None):
            self.rectangle_presenter.delete_temp_rectangle() #usuwa poprzedni cień
            self.rectangle_presenter.draw_rectangle(self.rectangle_presenter.rectangle_start_point[0], self.rectangle_presenter.rectangle_start_point[1], x, y)
        if self.drawing_tool == "polygon":
            self.polygon_presenter.set_cursor_pos(x,y)

    def handle_escape_click(self):
        self.rectangle_presenter.cancel_drawing_rectangle()
        self.polygon_presenter.cancel_drawing_polygon()
        self.drawing_tool = None
        self.view.set_notification_label("Brak aktywnego narzędzia")

    def handle_crtl_minus(self):
        self.file_list_presenter.decrease_zoom()

    def handle_crtl_plus(self):
        self.file_list_presenter.increase_zoom()

    def handle_scroll_up(self):
        self.file_list_presenter.increase_zoom()

    def handle_scroll_down(self):
        self.file_list_presenter.decrease_zoom()


