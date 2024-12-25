from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QListWidgetItem

#potem do wywalenia:
from view.StatisticsAnnotationsView import StatisticsAnnotationsView
from view.StatisticsClassView import StatisticsClassView
from view.StatisticsImageView import StatisticsImageView

class StatisticsPresenter:
    def __init__(self, view, project, presenter):
        self.view = view
        self.project = project
        self.presenter = presenter

        self.plt_img_res_htmap = None

        # Tworzenie widoku Annotation
        self.annotation_window = QtWidgets.QDialog(self.view)  # Użycie QDialog zamiast QMainWindow() pozwala na zlockowanie głównego widoku
        self.annotation_window.setModal(True)
        self.windowUiAnnotations = StatisticsAnnotationsView()
        self.windowUiAnnotations.setupUi(self.annotation_window, self)

        # Tworzenie widoku Class
        self.class_window = QtWidgets.QDialog(self.view)
        self.class_window.setModal(True)
        self.windowUiClass = StatisticsClassView()
        self.windowUiClass.setupUi(self.class_window , self)

        # Tworzenie widoku Image
        self.image_window = QtWidgets.QDialog(self.view)
        self.image_window.setModal(True)

        self.windowUiImage = StatisticsImageView()
        self.windowUiImage.setupUi(self.image_window, self)



    def open_annotation_window(self):
        self.refresh_annot_list()
        self.annotation_window.show()
        # self.annotation_window.setModal(True)

    def open_class_window(self):
        if len(self.project.get_classes_list())>0:
            self.refresh_class_window()
        self.class_window.show()

    def open_image_window(self):
        if self.project.get_list_of_images_size() > 0 :
            self.refresh_image_window()
        self.image_window.show()

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

    def refresh_image_window(self):
        imgs_sizes = self.determine_min_max_average_img_resolution()
        self.windowUiImage.image_listWidget.clear()
        self.windowUiImage.image_listWidget.addItem(f"Najmniejsza rozdzielczość obrazu: {imgs_sizes[0][0]}x{imgs_sizes[0][1]}")
        self.windowUiImage.image_listWidget.addItem(f"Największa rozdzielczość obrazu: {imgs_sizes[1][0]}x{imgs_sizes[1][1]:.0f}")
        self.windowUiImage.image_listWidget.addItem(f"Średnia rozdzielczość obrazu: {imgs_sizes[2][0]:.0f}x{imgs_sizes[2][1]:.0f}")

        # Jeśli istnieje stary obiekt PlotCanvas, usuń go
        if hasattr(self, 'plt_img_res_htmap') and self.plt_img_res_htmap is not None:
            self.windowUiImage.verticalLayout.removeWidget(self.plt_img_res_htmap)
            self.plt_img_res_htmap.deleteLater()  # Bezpieczne usunięcie
        # Tworzenie nowego obiektu PlotCanvas
        self.plt_img_res_htmap = PlotCanvas(self, width=24, height=8)
        # Dodanie nowego obiektu PlotCanvas do layoutu
        self.windowUiImage.verticalLayout.addWidget(self.plt_img_res_htmap)
        # Rysowanie heatmapy
        self.plt_img_res_htmap.plot_heatmap(self.get_imgs_resolutions())

    # def plot_img_resolutions(resolutions: dict[int, list[int, int]]):
    #     # Wyodrębnienie szerokości i wysokości
    #     widths = [res[0] for res in resolutions.values()]
    #     heights = [res[1] for res in resolutions.values()]
    #
    #     # Tworzenie wykresu
    #     plt.figure(figsize=(10, 6))
    #     plt.scatter(widths, heights, c='blue', alpha=0.7, edgecolors='black')
    #
    #     # Ustawienia wykresu
    #     plt.title("Rozdzielczości obrazów", fontsize=16)
    #     plt.xlabel("Szerokość (pixels)", fontsize=12)
    #     plt.ylabel("Wysokość (pixels)", fontsize=12)
    #     plt.grid(True, linestyle='--', alpha=0.6)
    #
    #     # Ograniczenie osi, jeśli to konieczne
    #     plt.xlim(0, max(widths) + 100)
    #     plt.ylim(0, max(heights) + 100)
    #
    #     # Wyświetlenie wykresu
    #     plt.show()

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
    def determine_min_max_average_img_resolution(self):
        imgs_list = self.project.get_images_list()

        # Zbieramy wszystkie rozdzielczości w postaci krotek (width, height)
        resolutions = [(img.width, img.height) for img in imgs_list]

        # Znajdowanie obrazu z najmniejszą rozdzielczością (szerokość + wysokość)
        min_resolution = min(resolutions, key=lambda x: x[0] * x[1])  # Minimalna rozdzielczość (szerokość * wysokość)

        # Znajdowanie obrazu z największą rozdzielczością
        max_resolution = max(resolutions, key=lambda x: x[0] * x[1])  # Maksymalna rozdzielczość (szerokość * wysokość)

        # Obliczanie średniej rozdzielczości
        avg_width = sum(res[0] for res in resolutions) / len(resolutions)
        avg_height = sum(res[1] for res in resolutions) / len(resolutions)
        avg_resolution = (avg_width, avg_height)

        # Zwracamy listę z wynikami
        return [min_resolution, max_resolution, avg_resolution]

    # Udział poszczególnych formatów obrazów w zbiorze(procentowy lub ilościowy)
    def count_img_format_usage(self) -> dict[str,int]:
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

    def get_imgs_resolutions(self) -> dict[int,list[int,int]]:
        imgs_list = self.project.get_images_list()
        data = {}
        for img in imgs_list:
            data[img.image_id] = [img.width, img.height]
        return data

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
##########################################################################################################

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


#######################################################################################################
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Tworzenie obiektu Figure z Matplotlib
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)  # Dodanie osi
        super().__init__(self.fig)

    def plot_resolutions(self, resolutions: dict[int, list[int, int]]):
        # Wyodrębnienie szerokości i wysokości
        widths = [res[0] for res in resolutions.values()]
        heights = [res[1] for res in resolutions.values()]

        # Rysowanie wykresu
        self.axes.clear()  # Czyszczenie poprzedniego wykresu (jeśli istnieje)
        self.axes.scatter(widths, heights, c='blue', alpha=0.7, edgecolors='black')
        self.axes.set_title("Rozdzielczości obrazów", fontsize=16)
        self.axes.set_xlabel("Szerokość (pixels)", fontsize=12)
        self.axes.set_ylabel("Wysokość (pixels)", fontsize=12)
        self.axes.grid(True, linestyle='--', alpha=0.6)

        # Automatyczne skalowanie osi
        self.axes.set_xlim(0, max(widths) + 100)
        self.axes.set_ylim(0, max(heights) + 100)

        # Rysowanie wykresu
        self.draw()

    def plot_heatmap(self, resolutions: dict[int, list[int, int]]):
        # Wyodrębnienie szerokości i wysokości
        widths = [res[0] for res in resolutions.values()]
        heights = [res[1] for res in resolutions.values()]

        # Tworzenie jednego wykresu (heatmapa)
        self.fig.clear()
        ax = self.fig.add_subplot(111)  # Prawy wykres: histogram 2D (heatmap)

        # Histogram 2D (heatmap) z paletą "rocket"
        heatmap = ax.hist2d(widths, heights, bins=20, cmap=sns.color_palette("rocket", as_cmap=True), alpha=0.8)
        ax.set_title("Histogram 2D (Heatmap)", fontsize=14)  # Ustawienie mniejszego rozmiaru czcionki tytułu
        ax.set_xlabel("Szerokość (pixels)", fontsize=10)  # Czcionka dla osi X
        ax.set_ylabel("Wysokość (pixels)", fontsize=10)  # Czcionka dla osi Y

        # Dodanie paska kolorów dla histogramu 2D
        # Dodanie paska kolorów dla histogramu 2D
        cbar = self.fig.colorbar(heatmap[3], ax=ax, label="Liczba obrazów")

        # Ustawienie tylko wartości całkowitych na pasku kolorów
        cbar.locator = ticker.MaxNLocator(integer=True)
        cbar.update_ticks()

        # Dodanie siatki (grid)
        ax.grid(True, linestyle='--', alpha=0.6)

        self.fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)

        # Rysowanie wykresu
        self.draw()