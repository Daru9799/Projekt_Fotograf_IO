from PyQt5 import QtWidgets


#potem do wywalenia:
from view.CreateClassWindowView import CreateClassWindowView


class StatisticsPresenter:
    def __init__(self, view, project, presenter):
        self.view = view
        self.project = project
        self.presenter = presenter

        # Tworzenie widoku
        self.window = QtWidgets.QDialog(self.view)  # Użycie QDialog zamiast QMainWindow() pozwala na zlockowanie głównego widoku
        self.window.setModal(True)
        # self.windowUi = CreateClassWindowView()
        # self.windowUi.setupUi(self.window, self)


    def open_statistics_window(self):
        # self.windowUi.Class_name_line_edit.setText("")
        self.window.show()

    # STATYSTYKI Adnotacji:
    # Zliczenie wszystkich adnotacji
    def count_all_adnotations(self) -> int:
        imgs_list = self.project.get_images_list()
        annotations_cntr = 0
        for img in imgs_list:
            if img.has_annotation:
                annot_list = img.get_annotation_list()
                annotations_cntr += len(annot_list)
        return annotations_cntr

    # Zliczenie zdjęć z adnotacjami
    def count_img_with_annotations(self) -> int:
        imgs_list = self.project.get_images_list()
        annotations_cntr = 0
        for img in imgs_list:
            if img.has_annotation:
                annotations_cntr += 1
        return annotations_cntr

    # Zliczenie zdjęć bez adnotacjami
    def count_img_without_annotation(self) -> int:
        imgs_list = self.project.get_images_list()
        annotations_cntr = 0
        for img in imgs_list:
            if not img.has_annotation:
                annotations_cntr += 1
        return annotations_cntr

    # Ilość zdjęć z kilkoma adnotacjami
    def count_img_with_mult_annotations(self):
        pass

    # Ilość zdjęć z kilkoma adnotacjami tej samej kalsy
    def count_img_mult_annotations_same_class(self):
        pass

    # Średnia ilość adnotacji na zdjęcie
    def calculate_avarage_ammount_annotations_per_img(self) -> float:
        pass

    # Rozkład liczby adnotacji na obraz: Wykres pokazujący, ile obrazów ma konkretną liczbę adnotacji.


    # STATYSTYKI KLAS:

    # Liczba obiektów dla każdej klasy
    def count_class_usage(self):
        pass

    #Procentowy udział klas w zbiorze danych:
    def calcualte_class_procentage_usage(self):
        pass

    def calculate_avarage_class_usage_per_img(self):
        pass


    # STATYSTYKI OBRAZÓW W PROJEKCIE:
    # Rozdzielczość obrazów: Średnia, minimalna, maksymalna rozdzielczość obrazów.
    def determine_min_max_avarage_img_resolution(self):
        pass

    # Udział poszczególnych formatów obrazów w zbiorze(procentowy lub ilościowy)
    def count_img_format_usage(self):
        pass


    # STATYSTYKI EXIF:
    #(Trzeba uwzględnić brak danych na temat exif do każdego zliczania)

    # Zwraca nazwy producentów oraz ilość zdjęć wykoanych przez te aparaty
    def count_camera_producer(self):
        pass

    def count_camera_models(self):
        pass

    # Zwraca listę elementów typu: ("nazwa_obrazu.jpg", data)
    def get_imgs_capture_data(self):
        pass

    # ? Eksport statystyk:
    # - w formie json'a
    # - w formie raportu pdf?