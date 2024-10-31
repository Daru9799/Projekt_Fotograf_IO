from PyQt5.QtWidgets import QMainWindow, QAction, QListWidget, QGridLayout, QWidget, QLabel, QFrame, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainView(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

###Na razie lista z plikami, potem będzie tutaj dodawane wszystko co znajduje się w oknie
        # Layout główny
        main_layout = QGridLayout()

        #Lewy panel (lista plikow, dodatkowe informacje EXIF)
        left_panel_layout = QVBoxLayout()
        main_layout.addLayout(left_panel_layout,0,2)

        # Napis lista plików
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignLeft)
        left_panel_layout.addWidget(self.label)

        # Lista plików (wymiary na razie na sztywno)
        self.file_list_widget = QListWidget(self)
        left_panel_layout.addWidget(self.file_list_widget)

        #Panel srodkowy
        central_panel_layout = QVBoxLayout()
        main_layout.addLayout(central_panel_layout,0,1)

        green_frame = QFrame()
        green_frame.setStyleSheet("background-color: green;")
        main_layout.addWidget(green_frame)

        #Panel prawy
        right_panel_layout = QVBoxLayout()
        main_layout.addLayout(right_panel_layout, 0, 0)

        red_frame = QFrame()
        red_frame.setStyleSheet("background-color: red;")
        right_panel_layout.addWidget(red_frame)

        #Rozciaganie paneli
        main_layout.setColumnStretch(0, 1)  # Lewy panel
        main_layout.setColumnStretch(1, 4)  # Panel środkowy
        main_layout.setColumnStretch(2, 1)  # Prawy panel

        #Podpięcie do widgetu
        widget = QWidget()
        widget.setLayout(main_layout)
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

    #metoda do updatowania sobie tekstu z ścieżką folderu po prawej stronie widgetu
    def update_folder_path(self, folderPath):
        self.label.setText(f"Obrazy z {folderPath}:")