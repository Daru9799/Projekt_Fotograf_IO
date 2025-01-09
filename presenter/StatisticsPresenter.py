from PyQt5 import QtWidgets
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QListWidgetItem, QHeaderView

#potem do wywalenia:
from view.StatisticsAnnotationsView import StatisticsAnnotationsView
from view.StatisticsClassView import StatisticsClassView
from view.StatisticsImageView import StatisticsImageView
from view.StatisticsExifView import StatisticsExifView

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

        # Tworzenie widoku Exif
        self.exif_window = QtWidgets.QDialog(self.view)
        self.exif_window.setModal(True)
        self.windowUiExif = StatisticsExifView()
        self.windowUiExif.setupUi(self.exif_window, self)



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

    def open_exif_window(self):
        self.refresh_exif_window()
        self.exif_window.show()

    def refresh_annot_list(self):
        #item = QListWidgetItem(f"Ilość wszystkich adnotacji: {self.count_all_adnotations()}")
        self.windowUiAnnotations.annotation_listWidget.clear()
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość wszystkich adnotacji: {self.count_all_adnotations()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów z adnotacjami: {self.count_img_with_annotations()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów bez adnotacjami: {self.count_img_without_annotation()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów z wieloma adnotacjami: {self.count_img_with_mult_annotations()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Ilość obrazów z wieloma adnotacjami tej samej klasy: {self.count_img_mult_annotations_same_class()}")
        self.windowUiAnnotations.annotation_listWidget.addItem(f"Średnia ilość adnotacji na obraz: {self.calculate_avarage_ammount_annotations_per_img():.2f}")

    def refresh_class_window(self):
        class_list = self.project.get_classes_list()
        cnt_class = self.count_class_usage()
        proc_class = self.calcualte_class_procentage_usage()
        avg_class = self.calculate_avarage_class_usage_per_img()
        iterat = 1
        header = ["LP", "Nazwa", "Ilość", "Procent", "Średnia"]
        tooltips = ["Liczba począdkowa", "Nazwa klasy", "Ilość adnotacji", "Procent udziału w projekcie", "Średnia ilość na obraz"]

        data = []
        # if len(class_list)>0:
        for cl in class_list:
            tmp = [iterat, cl.name, cnt_class[cl.class_id], f"{int(proc_class[cl.class_id])}%",f"{avg_class[cl.class_id]:.2f}"]
            iterat += 1
            data.append(tmp)


        model = CustomTableModel(data, header,tooltips)
        self.windowUiClass.class_tableView.setModel(model)
        self.windowUiClass.class_tableView.setSortingEnabled(True)
        self.windowUiClass.class_tableView.resizeColumnsToContents()
        self.windowUiClass.class_tableView.verticalHeader().setVisible(False)

    def refresh_image_window(self):
        imgs_sizes = self.determine_min_max_average_img_resolution()
        self.windowUiImage.image_listWidget.clear()
        self.windowUiImage.image_listWidget.addItem(f"Ilość obrazów w projekcie: {self.project.get_list_of_images_size()}")
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

    def refresh_exif_window(self):
        self.clear_charts()
        self.create_charts()

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
        #imgs_list = imgs_list[0] <-- generuje błąd
        data = {}
        for img in imgs_list:
            data[img.image_id] = [img.width, img.height]
        return data

    # STATYSTYKI EXIF:

    def get_imgs_exifs(self):
        imgs_list = self.project.get_images_list()
        exifs = []
        for img in imgs_list:
            exifs.append(img.get_exif_obj())
        return exifs

    def create_charts(self):
        # Pobieramy dane EXIF
        exifs = self.get_imgs_exifs()

        # Dane kategoryczne
        producers = {}
        models = {}

        # Dane liczbowe
        iso = []
        iso_no_data = []
        focal_length = []
        focal_length_no_data = []
        exposure_time = []
        exposure_time_no_data = []
        saturation = []
        saturation_no_data = []
        contrast = []
        contrast_no_data = []
        sharpness = []
        sharpness_no_data = []
        brightness_value = []
        brightness_value_no_data = []
        exposure_bias = []
        exposure_bias_no_data = []

        # Przetwarzanie danych
        for exif in exifs:
            producers[exif.producer] = producers.get(exif.producer, 0) + 1
            models[exif.model_of_camera] = models.get(exif.model_of_camera, 0) + 1

            # ISO
            if exif.iso == "No data":
                iso_no_data.append(0)
            else:
                iso.append(float(exif.iso))

            # Ogniskowa
            if exif.focal_length == "No data":
                focal_length_no_data.append(0)
            else:
                focal_length.append(float(exif.focal_length))

            if exif.exposure_time == "No data":
                exposure_time_no_data.append(0)
            else:
                exposure_time.append(float(exif.exposure_time))

            # Saturacja
            if exif.saturation == "No data":
                saturation_no_data.append(0)
            else:
                saturation.append(float(exif.saturation))

            # Kontrast
            if exif.contrast == "No data":
                contrast_no_data.append(0)
            else:
                contrast.append(float(exif.contrast))

            # Ostrość
            if exif.sharpness == "No data":
                sharpness_no_data.append(0)
            else:
                sharpness.append(float(exif.sharpness))

            # Jasność
            if exif.brightness_value == "No data":
                brightness_value_no_data.append(0)
            else:
                brightness_value.append(float(exif.brightness_value))

            # Korekta ekspozycji
            if exif.exposure_bias == "No data":
                exposure_bias_no_data.append(0)
            else:
                exposure_bias.append(float(exif.exposure_bias))

        # Tworzymy wykresy
        self.plot_bar_chart(producers, "Producenci", "Producer")
        self.plot_bar_chart(models, "Modele Kamer", "Camera Model")

        # Histogramy z wyróżnieniem "No data"
        self.plot_histogram(iso, iso_no_data, "ISO", "Wartość ISO")
        self.plot_histogram(focal_length, focal_length_no_data, "Ogniskowa", "Ogniskowa (mm)")
        self.plot_histogram(exposure_time, exposure_time_no_data, "Czas naświetlania", "Czas naświetlania (1/x s)")
        self.plot_histogram(brightness_value, brightness_value_no_data, "Jasność", "Wartość Jasności")
        self.plot_histogram(exposure_bias, exposure_bias_no_data, "Korekta ekspozycji", "Korekta ekspozycji (EV)")

        levels = {
            0: "Normalny",
            1: "Niski",
            2: "Wysoki"
        }

        # Wykresy dla saturation, contrast, sharpness
        self.plot_bar_chart_with_labels(saturation, saturation_no_data, "Saturacja", "Poziom", levels)
        self.plot_bar_chart_with_labels(contrast, contrast_no_data, "Kontrast", "Poziom", levels)
        self.plot_bar_chart_with_labels(sharpness, sharpness_no_data, "Ostrość", "Poziom", levels)

    def plot_bar_chart(self, data, title, xlabel):
        # Przygotowujemy dane wykresu
        labels = list(data.keys())
        values = list(data.values())

        # Tworzymy wykres
        fig, ax = plt.subplots(figsize=(6, 4))  # Większy rozmiar wykresu
        ax.bar(labels, values)

        # Ustawiamy tytuł i etykiety
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Liczba wystąpień")

        # Tworzymy widget do wyświetlania wykresu
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(740, 400)  # Stały rozmiar
        self.windowUiExif.scrollLayout.addWidget(canvas)
        canvas.draw()

    def plot_histogram(self, data, no_data, title, xlabel):
        # Przygotowanie danych
        all_data = data + no_data  # Wszystkie dane razem
        bins = np.linspace(min(all_data), max(all_data), 15)  # 15 przedziałów dynamicznie dopasowanych do zakresu
        data_counts, _ = np.histogram(data, bins=bins)
        no_data_counts, _ = np.histogram(no_data, bins=bins)

        # Tworzenie wykresu
        fig, ax = plt.subplots(figsize=(6, 4))  # Stały rozmiar wykresu

        # Dynamiczna szerokość kolumn
        bin_width = bins[1] - bins[0]  # Szerokość jednego przedziału
        bin_centers = bins[:-1] + bin_width / 2  # Środek każdego przedziału

        # Skumulowane kolumny
        ax.bar(bin_centers, data_counts, width=bin_width * 0.9, color='skyblue', edgecolor='black',
               label="Naturalne dane")  # 90% szerokości dla estetyki
        ax.bar(bin_centers, no_data_counts, width=bin_width * 0.9, bottom=data_counts, color='red', edgecolor='black',
               alpha=0.7, label="Brak danych ('No data')")

        # Ustawienia wykresu
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Liczba wystąpień")
        ax.legend()

        # Tworzymy widget do wyświetlania wykresu
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(740, 400)  # Stały rozmiar
        self.windowUiExif.scrollLayout.addWidget(canvas)
        canvas.draw()

    def plot_bar_chart_with_labels(self, data, no_data, title, xlabel, levels):
        # Przygotowanie danych
        all_data = [levels.get(value, "Nieznane") for value in data]
        unique_labels = list(levels.values())
        unique_labels.append("No data")  # Dodajemy kolumnę dla "No data"

        # Liczba wystąpień dla każdej kategorii
        counts = [all_data.count(label) for label in unique_labels[:-1]]
        counts.append(len(no_data))  # Liczba "No data"

        # Tworzenie wykresu
        fig, ax = plt.subplots(figsize=(6, 4))  # Stały rozmiar wykresu
        x = np.arange(len(unique_labels))  # Pozycje kategorii

        # Wykres słupkowy
        bar_width = 0.6  # Szerokość słupków
        ax.bar(x, counts, width=bar_width, color=['skyblue'] * len(unique_labels[:-1]) + ['red'], edgecolor='black')

        # Ustawienia osi i etykiet
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Liczba wystąpień")
        ax.set_xticks(x)
        ax.set_xticklabels(unique_labels)
        ax.set_ylim(0, max(counts) + 1)  # Dodajemy trochę przestrzeni nad najwyższym słupkiem

        # Tworzymy widget do wyświetlania wykresu
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(740, 400)  # Stały rozmiar
        self.windowUiExif.scrollLayout.addWidget(canvas)
        canvas.draw()

    def clear_charts(self):
        # Iteracja przez wszystkie widgety w scrollLayout
        for i in reversed(range(self.windowUiExif.scrollLayout.count())):
            widget = self.windowUiExif.scrollLayout.itemAt(i).widget()
            if widget:
                widget.deleteLater()  # Usuwanie widgetu

##########################################################################################################

from PyQt5.QtCore import Qt, QAbstractTableModel

class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, headers, tooltips):
        super().__init__()
        self._data = data
        self._headers = headers
        self._tooltips = tooltips

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
        elif role == Qt.ToolTipRole:  # Dodanie obsługi tooltipów
            if orientation == Qt.Horizontal:
                return self._tooltips[section]

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
