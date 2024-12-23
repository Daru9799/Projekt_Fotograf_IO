from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidgetItem

#potem do wywalenia:
from view.StatisticsAnnotationsView import StatisticsAnnotationsView
from view.StatisticsClassView import StatisticsClassView

class StatisticsPresenter:
    def __init__(self, view, project, presenter):
        self.view = view
        self.project = project
        self.presenter = presenter

        # Tworzenie widoku Annotation
        self.annotation_window = QtWidgets.QDialog(self.view)  # Użycie QDialog zamiast QMainWindow() pozwala na zlockowanie głównego widoku
        self.annotation_window.setModal(True)
        self.windowUiAnnotations = StatisticsAnnotationsView()
        self.windowUiAnnotations.setupUi(self.annotation_window, self)

        self.class_window = QtWidgets.QDialog(
            self.view)  # Użycie QDialog zamiast QMainWindow() pozwala na zlockowanie głównego widoku
        self.class_window.setModal(True)
        self.windowUiClass = StatisticsClassView()
        self.windowUiClass.setupUi(self.class_window , self)


    def open_annotation_window(self):
        self.refresh_annot_list()
        self.annotation_window.show()
        # self.annotation_window.setModal(True)

    def open_class_window(self):
        if len(self.project.get_classes_list())>0:
            self.refresh_class_window()
        self.class_window.show()

    def refresh_annot_list(self):
        #item = QListWidgetItem(f"Ilość wszystkich adnotacji: {self.count_all_adnotations()}")
        self.windowUiAnnotations.annotation_listWidget.clear()
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość wszystkich adnotacji: {self.count_all_adnotations()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów z adnotacjami: {self.count_img_with_annotations()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów bez adnotacjami: {self.count_img_without_annotation()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów z wieloma adnotacjami: {self.count_img_with_mult_annotations()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów z wieloma adnotacjami tej samej klasy: {self.count_img_mult_annotations_same_class()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Średnia ilość adnotacji na obraz: {self.calculate_avarage_ammount_annotations_per_img()}")

    def refresh_class_window(self):
        class_list = self.project.get_classes_list()
        cnt_class = self.count_class_usage()
        proc_class = self.calcualte_class_procentage_usage()
        avg_class = self.calculate_avarage_class_usage_per_img()
        iterat = 1
        header = ["LP", "Nazwa", "Ilość", "Procent", "Średnia"]
        data = []
        # if len(class_list)>0:
        for cl in class_list:
            tmp = [iterat, cl.name, cnt_class[cl.class_id], f"{int(proc_class[cl.class_id])}%",f"{avg_class[cl.class_id]:.2f}"]
            iterat += 1
            data.append(tmp)
        model = CustomTableModel(data, header)
        self.windowUiClass.class_tableView.setModel(model)
        self.windowUiClass.class_tableView.setSortingEnabled(True)
        self.windowUiClass.class_tableView.resizeColumnsToContents()
        self.windowUiClass.class_tableView.verticalHeader().setVisible(False)

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
    def count_img_with_mult_annotations(self) -> int:
        imgs_list = self.project.get_images_list()
        mult_annotations_cntr = 0
        for img in imgs_list:
            if img.has_annotation and (img.get_annotation_size()>1):
                mult_annotations_cntr += 1
        return mult_annotations_cntr

    # Ilość zdjęć z kilkoma adnotacjami tej samej kalsy
    def count_img_mult_annotations_same_class(self) -> int:
        imgs_list = self.project.get_images_list()
        mult_annotations_cntr = 0
        for img in imgs_list:
            if img.has_annotation and (img.get_annotation_size() > 1):
                annot_list = img.get_annotation_list()
                # Tworzymy słownik do zliczania wystąpień każdego class_id
                class_count = {}
                for annotation in annot_list:
                    class_id = annotation.class_id
                    if class_id in class_count:
                        class_count[class_id] += 1
                    else:
                        class_count[class_id] = 1

                # Sprawdzamy, czy istnieje co najmniej jeden class_id z więcej niż jedną adnotacją
                if any(count > 1 for count in class_count.values()):
                    mult_annotations_cntr += 1

        return mult_annotations_cntr

    # Średnia ilość adnotacji na zdjęcie
    def calculate_avarage_ammount_annotations_per_img(self) -> float:
        all_annot = self.count_all_adnotations()
        return all_annot/self.project.get_list_of_images_size()

    # Rozkład liczby adnotacji na obraz: Wykres pokazujący, ile obrazów ma konkretną liczbę adnotacji.


    # STATYSTYKI KLAS:

    # Liczba obiektów dla każdej klasy
    def count_class_usage(self) -> dict[int, int]:
        imgs_list = self.project.get_images_list()
        class_list = self.project.get_classes_list()
        class_count = {}

        for cl in class_list:
            class_count[cl.class_id] = 0

        for img in imgs_list:
            if img.has_annotation:
                annot_list = img.get_annotation_list()
                for annotation in annot_list:
                    class_id = annotation.class_id
                    if class_id in class_count:
                        class_count[class_id] += 1

        return class_count

    #Procentowy udział klas w zbiorze danych:
    def calcualte_class_procentage_usage(self) -> dict[int, float]:
        all_annot = self.count_all_adnotations()
        class_usage_dict = self.count_class_usage()
        proct_usage = {}
        for cl in class_usage_dict:
            if all_annot == 0:
                proct_usage[cl] = 0
            else:
                proct_usage[cl] = (class_usage_dict[cl] / all_annot) * 100
        return proct_usage

    def calculate_avarage_class_usage_per_img(self) -> dict[int, float]:
        class_usage_dict = self.count_class_usage()
        imgs_list_size = self.project.get_list_of_images_size()
        avarage_usage = {}
        for cl in class_usage_dict:
            if class_usage_dict[cl] == 0:
                avarage_usage[cl] = 0
            else:
                avarage_usage[cl] = (class_usage_dict[cl] / imgs_list_size)

        return avarage_usage

    # STATYSTYKI OBRAZÓW W PROJEKCIE:
    # Rozdzielczość obrazów: Średnia, minimalna, maksymalna rozdzielczość obrazów.
    def determine_min_max_avarage_img_resolution(self):
        imgs_list = self.project.get_images_list()
        # Sprawdzenie, czy lista obrazów nie jest pusta
        if not imgs_list:
            return [0, 0, 0]  # Zwracamy 0 dla każdej wartości, gdy brak obrazów

        resolutions = [img.width * img.height for img in imgs_list]

        # Wyznaczanie wartości minimalnej, maksymalnej oraz średniej
        min_resolution = min(resolutions)
        max_resolution = max(resolutions)
        avg_resolution = sum(resolutions) / len(resolutions)

        return [min_resolution, max_resolution, avg_resolution]

    # Udział poszczególnych formatów obrazów w zbiorze(procentowy lub ilościowy)
    def count_img_format_usage(self):
        imgs_list = self.project.get_images_list()

        # Słownik do przechowywania liczby zdjęć dla każdego formatu
        format_count = {}

        for img in imgs_list:
            # Pobieranie formatu obrazu na podstawie rozszerzenia pliku
            file_format = img.filename.split('.')[-1].lower()  # Pobieramy rozszerzenie i konwertujemy na małe litery

            # Inkrementacja licznika dla danego formatu
            if file_format in format_count:
                format_count[file_format] += 1
            else:
                format_count[file_format] = 1

        return format_count


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


from PyQt5.QtCore import Qt, QAbstractTableModel

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(key=lambda x: x[column], reverse=(order == Qt.DescendingOrder))
        self.layoutChanged.emit()