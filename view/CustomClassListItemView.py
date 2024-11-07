from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox

class CustomClassListItemView(QWidget):
    def __init__(self, Class, parent=None):
        super(CustomClassListItemView, self).__init__(parent)

        self.Class = Class

        # Inicjalizacja układu:
        self.row = QHBoxLayout()

        # Dodawanie widgetów
        self.label = QLabel(Class.name)
        self.checkbox = QCheckBox("?")

        self.row.addWidget(self.label)
        self.row.addWidget(self.checkbox)
        self.setLayout(self.row)


    # Metoda do sprawdzania, czy checkbox jest zaznaczony
    def is_checked(self):
        return self.checkbox.isChecked()