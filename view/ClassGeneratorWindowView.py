from PyQt5.QtWidgets import (QHeaderView, QDesktopWidget, QColorDialog, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSlider, QPushButton, QCheckBox, QListWidget, QListWidgetItem, QStackedWidget, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import random

class ClassGeneratorWindowView(QDialog):
    def __init__(self, presenter):
        super().__init__()
        self.setWindowTitle("Automatyczne tworzenie klas")
        self.setGeometry(100, 100, 450, 350)
        self.setFixedSize(450, 350)
        self.presenter = presenter
        self.setWindowIcon(QIcon("img/classGeneratorIcon.png"))

        self.stacked_widget = QStackedWidget()

        #Centrowanie widgetu na ekranie
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

        #Inicjalizacja zmiennych
        self.lang_combo = None
        self.accuracy_slider = None
        self.accuracy_value_label = None
        self.tags = [{"name": "Tag1", "certainty": 90}]

        #Strony okienka
        self.page1 = self.create_page1()
        self.page2 = self.create_page2()

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def create_page1(self):
        page = QWidget()
        layout = QVBoxLayout()

        #Tworzenie layoutu dla wyśrodkowania
        central_layout = QVBoxLayout()
        central_layout.setSpacing(20)

        #Informacja
        info_layout = QHBoxLayout()
        info_label = QLabel("Uwaga! Dla aktualnie zaznaczonego obrazu zostaną wygenerowane tagi przy pomocy serwisu chmurowego. Prosimy o dostosowanie parametrów. Wybranie języka innego niż angielski poskutkuje dłuższym czasem oczekiwania na rezultat z powodu automatycznego tłumaczenia. Tłumaczenie może być nieprecyzyjne!")
        info_label.setWordWrap(True)
        info_label.setFixedWidth(420)
        font = QFont()
        font.setPointSize(10)
        info_label.setFont(font)
        info_layout.addWidget(info_label)
        central_layout.addLayout(info_layout)
        central_layout.addSpacing(10)

        #Wybór języka
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Język wygenerowanych tagów:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Angielski", "Polski", "Hiszpański"])
        #Zmiana koloru combo boxa (domyślnie byl czarny)
        self.lang_combo.setStyleSheet("""
            QComboBox { 
                color: white; 
                background-color: #333333; 
            }
            QComboBox QAbstractItemView {
                color: white; 
                background-color: #444444; 
            }
        """)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        central_layout.addLayout(lang_layout)

        #Dokładność
        accuracy_layout = QHBoxLayout()
        accuracy_label = QLabel("Minimalna pewność:")
        self.accuracy_slider = QSlider(Qt.Horizontal)
        self.accuracy_slider.setRange(1, 100)
        self.accuracy_slider.setValue(70)
        self.accuracy_value_label = QLabel("70%")
        self.accuracy_value_label.setFixedWidth(40)
        self.accuracy_slider.valueChanged.connect(self.update_accuracy_value)
        accuracy_layout.addWidget(accuracy_label)
        accuracy_layout.addWidget(self.accuracy_slider)
        accuracy_layout.addSpacing(5)
        accuracy_layout.addWidget(self.accuracy_value_label)
        central_layout.addLayout(accuracy_layout)

        #Przycisk "Wygeneruj tagi"
        generate_button = QPushButton("Wygeneruj tagi")
        generate_button.clicked.connect(self.switch_to_page2)
        central_layout.addSpacing(20)
        central_layout.addWidget(generate_button)

        #Centrowanie
        central_layout.setAlignment(Qt.AlignTop)
        layout.addLayout(central_layout)

        page.setLayout(layout)
        return page

    def create_page2(self):
        page = QWidget()
        layout = QVBoxLayout()

        #Tabela tagów
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Nazwa", " Pewność ", " Kolor ", "Dodaj"])

        #Wyłączenie numeracji wierszy
        table.verticalHeader().setVisible(False)

        #Zaznaczanie całego wiersza a nie komórek
        table.setSelectionBehavior(QTableWidget.SelectRows)

        #Dostosowanie headerów
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        table.setRowCount(len(self.tags))

        for row, tag in enumerate(self.tags):
            #Kolumna 1: Nazwa tagu
            name_item = QTableWidgetItem(tag["name"])
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            name_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, name_item)

            #Kolumna 2: Pewność
            certainty_item = QTableWidgetItem(f"{tag['certainty']}%")
            certainty_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            certainty_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, certainty_item)

            #Kolumna 3: Wybór koloru
            color_button = QPushButton()
            color_button.setStyleSheet("background-color: gray;")
            color_button.clicked.connect(lambda _, r=row: self.select_color(r, table))
            color_button.setFixedSize(20,20)
            table.setCellWidget(row, 2, color_button)

            #Kolumna 4: Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            table.setCellWidget(row, 3, checkbox)

        #Przycisk "Utwórz klasy" i "Wróć"
        create_class_button = QPushButton("Utwórz klasy z zaznaczonych elementów")
        create_class_button.clicked.connect(lambda: self.create_new_classes(table))

        button_layout = QHBoxLayout()
        button_layout.addWidget(create_class_button, 50)
        button_layout.addStretch(1)
        layout.addWidget(table)
        layout.addLayout(button_layout)

        page.setLayout(layout)
        return page

    #Przełączanie między stronami
    def switch_to_page2(self):
        ac = self.get_accuracy()
        lan = self.get_selected_language()
        self.stacked_widget.setCurrentIndex(1)
        #Przeslanie do prezentera
        self.presenter.handle_create_tags_click(lan, ac)
        #Zmiana okna
        self.setFixedSize(600, 400)
        #Refresh tabeli
        table = self.page2.findChild(QTableWidget)
        self.refresh_table(table)

    def switch_to_page1(self):
        self.setFixedSize(450, 350)
        self.stacked_widget.setCurrentIndex(0)
        #CZYSZCZENIE LISTY TAGÓW

    #Wybór koloru
    def select_color(self, row, table):
        color = QColorDialog.getColor()
        if color.isValid():
            button = table.cellWidget(row, 2)
            button.setStyleSheet(f"background-color: {color.name()};")

    #Aktualizacja wartości suwaka
    def update_accuracy_value(self, value):
        self.accuracy_value_label.setText(str(value) + "%")

    #Metody do zwracania wartości (strona 1)
    def get_accuracy(self):
        return self.accuracy_slider.value()

    def get_selected_language(self):
        return self.lang_combo.currentText()

    def get_selected_items(self, table):
        selected_items = []
        for row in range(table.rowCount()):
            checkbox = table.cellWidget(row, 3)

            #Sprawdzanie, czy checkbox jest zaznaczony
            if checkbox.isChecked():
                name_item = table.item(row, 0).text()
                color_button = table.cellWidget(row, 2)
                color = color_button.palette().button().color().getRgb()
                #Dodanie do listy (name, color)
                selected_items.append((name_item, (color[0], color[1], color[2])))
        return selected_items

    def create_new_classes(self, table):
        selected_items = self.get_selected_items(table)
        self.presenter.create_classes_from_tags(selected_items)
        self.accept()

    def refresh_table(self, table):
        table.setRowCount(len(self.tags))
        for row, tag in enumerate(self.tags):
            # Kolumna 1: Nazwa tagu
            name_item = QTableWidgetItem(tag["name"])
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            name_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 0, name_item)

            # Kolumna 2: Pewność
            certainty_item = QTableWidgetItem(f"{tag['certainty']}%")
            certainty_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            certainty_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 1, certainty_item)

            # Kolumna 3: Wybór koloru
            color_button = QPushButton()
            random_col = self.random_color()  # Losowanie koloru
            color_button.setStyleSheet(f"background-color: {random_col};")
            color_button.clicked.connect(lambda _, r=row: self.select_color(r, table))
            color_button.setFixedSize(20, 20)
            table.setCellWidget(row, 2, color_button)

            # Kolumna 4: Checkbox
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            table.setCellWidget(row, 3, checkbox)

    #Losowanie koloru
    def random_color(self):
        return f"#{random.randint(0, 0xFFFFFF):06x}"