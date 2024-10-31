from PyQt5.QtWidgets import QMainWindow, QAction, QListWidget, QGridLayout, QWidget, QLabel, QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class MainView(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

###Na razie lista z plikami, potem będzie tutaj dodawane wszystko co znajduje się w oknie
        # Layout główny
        self.main_layout = QGridLayout()

        #Panel prawy (lista plikow, dodatkowe informacje EXIF)
        right_panel_layout = QVBoxLayout()
        self.main_layout.addLayout(right_panel_layout,0,2)

        # Napis lista plików
        self.label = QLabel("Nie wybrano folderu!", self)
        self.label.setAlignment(Qt.AlignLeft)
        right_panel_layout.addWidget(self.label)

        # Lista plików (wymiary na razie na sztywno)
        self.file_list_widget = QListWidget(self)
        right_panel_layout.addWidget(self.file_list_widget)
        self.file_list_widget.itemClicked.connect(lambda item: self.presenter.folder_list_on_click(item))

        #Panel srodkowy
        central_panel_layout = QVBoxLayout()
        self.main_layout.addLayout(central_panel_layout,0,1)

        #Obrazek w panelu srodkowym
        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        central_panel_layout.addWidget(self.graphics_view)

        #Panel lewy
        left_panel_layout = QVBoxLayout()
        self.main_layout.addLayout(left_panel_layout, 0, 0)

        red_frame = QFrame()
        red_frame.setStyleSheet("background-color: red;")
        left_panel_layout.addWidget(red_frame)

        #Rozciaganie paneli
        self.main_layout.setColumnStretch(0, 1)  # Lewy panel
        self.main_layout.setColumnStretch(1, 3)  # Panel środkowy
        self.main_layout.setColumnStretch(2, 1)  # Prawy panel

        #Podpięcie do widgetu
        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)


###Menu górne
        #Tworzenie paska menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Plik')

        #Tworzenie akcji
        new_project_action = QAction(QIcon('img\cameraIcon.png'), 'Załaduj folder ze zdjęciami', self)
        new_project_action.triggered.connect(self.presenter.create_new_project)

        #Dodawanie akcji do menu (tzn. dodanie akcji tworzenia projektu do plik)
        file_menu.addAction(new_project_action)


###Customizacja okna głównego
        self.setWindowTitle('Fotograf')
        self.setWindowIcon(QIcon('img\cameraIcon.png'))  #ikonka w lewym górnym
        self.showMaximized()

###Metody
    #metoda do updatowania sobie tekstu z ścieżką folderu po prawej stronie widgetu
    def update_folder_path(self, folderPath):
        self.label.setText(f"Obrazy z {folderPath}:")
#obrazek
    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Nie udało się załadować obrazu.")
            return
        self.scene.clear()
        self.scene.addItem(QGraphicsPixmapItem(pixmap))