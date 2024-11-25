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
        self.label = QLabel()
        self.checkbox = QCheckBox()

        # Add widgets to layout
        self.row.addWidget(self.label)
        self.row.addWidget(self.checkbox)
        self.setLayout(self.row)

    def isChecked(self):
        return self.checkbox.isChecked()

    def getAnnotation(self):
        return self.Annotation

    def set_color(self, class_color):
        r, g, b = class_color  # Rozpakowanie krotki (R, G, B)
        qcolor = QColor(r, g, b)  # Tworzenie koloru tła

        # Obliczanie jasności koloru (średnia ważona RGB)
        brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b

        # Ustalanie koloru tekstu: biały dla ciemniejszych, czarny dla jaśniejszych
        if brightness < 128:
            text_color = "#FFFFFF"  # Biały tekst
        else:
            text_color = "#000000"  # Czarny tekst

        # Łączenie stylów tła i koloru tekstu w jeden ciąg
        self.label.setStyleSheet(f"background-color: {qcolor.name()}; border: none; color: {text_color};")

    def set_class_name(self, class_name):
        self.label.setText(f"{class_name} - {self.Annotation.annotation_id}")



