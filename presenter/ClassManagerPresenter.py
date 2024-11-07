from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from PyQt5 import QtWidgets
from view.CreateClassWindowView import CreateClassWindowView
from view.CustomClassListItemView import CustomClassListItemView

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


    # !!!
    #   Narazie usuwa tylko 1 wybrany item, ale też można zaznaczyć jedną kalsę na raz
    #   więc nwm czy tak to zostawić
    # ! Trzeba jescze dodać jakiegoś MessageBox'a do potwierdzenia usuwania
    def deleteClass(self):
        selectedItems = self.view.class_list_widget.selectedItems()

        if selectedItems: # sprawdzenie czy cokolwiek jest zaznaczone
            # Wybieramy pierwszy zaznaczony element
            selected_item = selectedItems[0]

            # Pobieramy CustomClassListItemView powiązany z QListWidgetItem
            custom_view = self.view.class_list_widget.itemWidget(selected_item)
            # Wywołujemy usuwanie z listy Klasy
            self.project.deleteClass(custom_view.Class.class_id)
            self.updateItems() # odświeżenie listy

    # Metoda aktualizująca class_list_widget
    def updateItems(self):
        self.view.class_list_widget.clear()
        for cl in self.project.list_of_classes_model:
            #Kod służy do stworzenia customowego list itemu
            item = QListWidgetItem(self.view.class_list_widget) # dla każdej klasy cl tworzy nowy obiekt QListWidgetItem i przypisuje go do self.view.class_list_widget
            self.view.class_list_widget.addItem(item) # dodaje element item do widżetu listy
            row = CustomClassListItemView(cl) # tworzy nowy widok CustomClassListItemView
            item.setSizeHint(row.minimumSizeHint()) # ustawia rozmiar elementu item, aby pasował do minimalnego rozmiaru widoku row
            self.view.class_list_widget.setItemWidget(item, row) # ustawia widok row jako widok wewnętrzny dla item, co pozwala na dostosowany wygląd każdego elementu