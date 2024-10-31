from PyQt5.QtWidgets import QMainWindow, QAction, QListWidget, QHBoxLayout, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainView(QMainWindow):
    def __init__(self, presenter):
        super().__init__()
        self.presenter = presenter

###Na razie lista z plikami, potem będzie tutaj dodawane wszystko co znajduje się w oknie
        # Główne widgety
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout główny
        self.layout = QHBoxLayout(self.central_widget)

        # Widget boczny
        self.sidebar_widget = QWidget(self)
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)

        #Napis lista plików
        self.label = QLabel("", self)
        self.layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignLeft)
        self.sidebar_layout.addWidget(self.label)

        # Lista plików (wymiary na razie na sztywno)
        self.file_list_widget = QListWidget(self)
        self.file_list_widget.setFixedWidth(200)  # Szerokość listy
        self.file_list_widget.setFixedHeight(300)  # Wysokość listy
        self.sidebar_layout.addWidget(self.file_list_widget)

        #Umieszczenie widgetu bocznego na glownym layoucie i dopasowanie go do prawego górnego rogu
        self.layout.addWidget(self.sidebar_widget, alignment=Qt.AlignTop | Qt.AlignRight)

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
        self.setGeometry(100, 100, 800, 600)

    #metoda do updatowania sobie tekstu z ścieżką folderu po prawej stronie widgetu
    def update_folder_path(self, folderPath):
        self.label.setText(f"Obrazy z {folderPath}:")