import re

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QColorDialog, QPushButton


class CustomClassListItemView(QWidget):
    def __init__(self, Class,classManagerPresenter ,parent=None):
        super(CustomClassListItemView, self).__init__(parent)

        self.Class = Class
        self.presenter = classManagerPresenter

        # Inicjalizacja układu:
        self.row = QHBoxLayout()

        # Dodawanie widgetów
        self.label = QLabel(Class.name)
        self.checkboxHidden = QCheckBox("Ukryj")
        self.checkboxToDelete = QCheckBox("")
        self.colorBox = QPushButton()
        self.colorBox.setFixedSize(QSize(25,25)) # Ustawiamy rozmiar Buttona
        self.colorBox.setStyleSheet(f"background-color: rgb({self.Class.color[0]},{self.Class.color[1]},{self.Class.color[2]});")

        self.colorBox.clicked.connect(self.setColor)
        self.checkboxHidden.stateChanged.connect(self.onCheckboxHiddenChanged)

        self.row.addWidget(self.label)
        self.row.addWidget(self.checkboxHidden)
        self.row.addWidget(self.checkboxToDelete)
        self.row.addWidget(self.colorBox)
        self.setLayout(self.row)

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

