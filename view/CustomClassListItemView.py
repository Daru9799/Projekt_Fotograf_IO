from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QColorDialog, QPushButton, QVBoxLayout, QSizePolicy


class CustomClassListItemView(QWidget):
    def __init__(self, Class, classManagerPresenter, parent=None):
        super(CustomClassListItemView, self).__init__(parent)

        self.Class = Class
        self.presenter = classManagerPresenter

        # Główne układy
        self.mainLayout = QVBoxLayout()  # Główny układ pionowy
        self.headerLayout = QHBoxLayout()  # Układ poziomy na nagłówki
        self.widgetLayout = QHBoxLayout()  # Układ poziomy na widgety

        # Tworzenie nagłówków
        self.labelTitle = QLabel("Nazwa")
        self.checkboxHiddenTitle = QLabel("Ukryj")
        self.checkboxToDeleteTitle = QLabel("Usuń")
        self.colorBoxTitle = QLabel("Kolor")

        # Stylizacja nagłówków
        for title in [self.labelTitle, self.checkboxHiddenTitle, self.checkboxToDeleteTitle, self.colorBoxTitle]:
            title.setStyleSheet("font-size: 10px; color: gray;")
            title.setAlignment(Qt.AlignCenter)

        # Dodanie nagłówków do układu poziomego
        self.headerLayout.addWidget(self.labelTitle)
        self.headerLayout.addWidget(self.checkboxHiddenTitle)
        self.headerLayout.addWidget(self.checkboxToDeleteTitle)
        self.headerLayout.addWidget(self.colorBoxTitle)

        # Tworzenie widgetów
        self.label = QLabel(Class.name)
        self.label.setMaximumWidth(90)  # Ustawienie maksymalnej szerokości
        self.label.setWordWrap(False)  # Wyłączenie zawijania tekstu
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)  # Ograniczenie wpływu na układ
        # self.label.setStyleSheet("text-overflow: ellipsis;")  # Dodanie elipsy
        self.label.setToolTip(Class.name)  # Podpowiedź pełnego tekstu
        self.checkboxHidden = QCheckBox()
        self.checkboxToDelete = QCheckBox()
        self.colorBox = QPushButton()
        self.colorBox.setFixedSize(QSize(25, 25))  # Ustawiamy rozmiar Buttona
        self.colorBox.setStyleSheet(
            f"background-color: rgb({self.Class.color[0]},{self.Class.color[1]},{self.Class.color[2]});"
        )

        # Połączenie sygnałów
        self.colorBox.clicked.connect(self.setColor)
        self.checkboxHidden.stateChanged.connect(self.onCheckboxHiddenChanged)

        # Dodanie widgetów do układu poziomego
        self.widgetLayout.addWidget(self.label)
        self.widgetLayout.addWidget(self.checkboxHidden)
        self.widgetLayout.addWidget(self.checkboxToDelete)
        self.widgetLayout.addWidget(self.colorBox)

        # Dodanie układów do głównego układu
        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.widgetLayout)

        self.setLayout(self.mainLayout)

    # Metoda do sprawdzania, czy checkbox jest zaznaczony
    def isHiddenChecked(self):
        return self.checkboxHidden.isChecked()

    def onCheckboxHiddenChanged(self, state):
        self.presenter.presenter.scene_presenter.get_annotations_from_project()
        self.presenter.presenter.scene_presenter.draw_annotations()

    def isToDeleteChecked(self):
        return self.checkboxToDelete.isChecked()

    def setColor(self):
        rgb = QColorDialog.getColor().getRgb()

        # Jeśli nie wybierzemy koloru to rgb będzie miało wartość: (0,0,0,255)
        # Minusem tego rozwiązanie jest to że nie można zrobić klasy o kolorze czarnym
        if rgb == (0,0,0,255):
            return
        self.colorBox.setStyleSheet(
            f"background-color: rgb({rgb[0]},{rgb[1]},{rgb[2]});")

        #Informuje prezentera że trzeba zaktualizwować klasę
        self.presenter.updateColorClass(self.Class, rgb)

