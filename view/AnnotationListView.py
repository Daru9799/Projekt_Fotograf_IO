from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QColorDialog, QPushButton

class AnnotationListView(QWidget):
    def __init__(self, Annotation, AnnotationPresenter, parent=None):

        super(AnnotationListView, self).__init__(parent or None)
        self.Annotation= Annotation
        self.presenter = AnnotationPresenter

        # Initialize layout
        self.row = QHBoxLayout()

        # Widgets
        self.label = QLabel(f"Annotacja nr. {self.Annotation.annotation_id}")
        self.checkbox = QCheckBox("?")
        self.colorBox = QPushButton()
        self.colorBox.setFixedSize(QSize(25, 25))

        # r, g, b = self.Annotation.color  # Rozpakowanie krotki (R, G, B)
        # qcolor = QColor(r, g, b)  # Tworzenie koloru
        # self.colorBox.setStyleSheet(f"background-color: {qcolor.name()}; border: none;")

        # Connect color change
        # self.colorBox.clicked.connect(self.setColor)

        # Add widgets to layout
        self.row.addWidget(self.label)
        self.row.addWidget(self.checkbox)
        self.row.addWidget(self.colorBox)
        self.setLayout(self.row)

    def isChecked(self):
        return self.checkbox.isChecked()

    def getAnnotation(self):
        return self.Annotation

    def set_color(self,class_color):
        r, g, b = class_color  # Rozpakowanie krotki (R, G, B)
        qcolor = QColor(r, g, b)  # Tworzenie koloru
        self.colorBox.setStyleSheet(f"background-color: {qcolor.name()}; border: none;")

