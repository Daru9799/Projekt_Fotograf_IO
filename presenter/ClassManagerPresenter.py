from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets
from view.CreateClassWindowView import CreateClassWindowView

class ClassManagerPresenter:
    def __init__(self, view, project):
        self.view = view
        self.project = project

        #Tworzenie widoku
        self.window = QtWidgets.QMainWindow()
        self.windowUi = CreateClassWindowView()
        self.windowUi.setupUi(self.window,self)


    # Metoda do otwierania nowego okna
    def openCreateWindow(self):
        self.windowUi.Class_name_line_edit.setText("")
        self.window.show()

    # Metoda uruchamiana po kliknięciu w Zapisz w nowym oknie
    def saveClass(self):
        newClassName = self.windowUi.Class_name_line_edit.text()
        self.project.addNewClass(newClassName)
        self.updateItems() # aktulizacja
        self.window.close()

    # Metoda aktualizująca class_list_widget
    def updateItems(self):
        self.view.class_list_widget.clear()
        for cl in self.project.list_of_classes_model:
            self.view.class_list_widget.addItem(cl.name)