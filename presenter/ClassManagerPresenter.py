import copy

from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QColorDialog
from PyQt5 import QtWidgets
from view.CreateClassWindowView import CreateClassWindowView
from view.CustomClassListItemView import CustomClassListItemView

class ClassManagerPresenter:
    def __init__(self, view, project, presenter):
        self.view = view
        self.project = project
        self.presenter = presenter

        self.checkboxes_state = [[],[]]

        #Tworzenie widoku
        self.window = QtWidgets.QDialog(self.view) # Użycie QDialog zamiast QMainWindow() pozwala na zlockowanie głównego widoku
        self.window.setModal(True)
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

    def deleteClass(self):
        if self.presenter.drawing_tool is not None:
            self.view.show_message_OK("Informacja", "Nie można usunąć klas, gdy narzędzia do adnotacji są aktywne!")
            return

        checked_classes = []

        for index in range(self.view.class_list_widget.count()):
            item = self.view.class_list_widget.item(index)
            row_widget = self.view.class_list_widget.itemWidget(item)

            if row_widget.isToDeleteChecked():
                checked_classes.append(row_widget.Class)   # Dodajmey ID klasy które chcemy usunąć

        # Kiedy klikniemy a nie ma zaznaczonych klas:
        if len(checked_classes) == 0:
            self.view.show_message_OK("Informacja", "Zaznacz klasę do usunięcia")
            return

        # Potwierdzenie usunięcia klas:
        class_names = ", ".join([cls.name for cls in checked_classes])
        confirmation = self.view.show_message_Yes_No("Potwierdzenie",
                                                     f"Czy na pewno chcesz usunąć zaznaczone klasy: {class_names}?")

        if confirmation:
            # Wywołujemy usuwanie z listy Klasy
            for cl in checked_classes:
                self.project.deleteClass(cl.class_id)
                self.presenter.annotation_presenter.delete_annotations_by_class(cl.class_id)
            self.updateItems() # odświeżenie listy
            self.presenter.scene_presenter.get_annotations_from_project()   # Pobranie adnotacji
            self.presenter.scene_presenter.draw_annotations()               # Narysowanie/Odświerzenie adnotacji

    # Metoda aktualizująca class_list_widget
    def updateItems(self):
        if len(self.view.class_list_widget) != 0:
            self.save_checkboxes_states()
        self.view.class_list_widget.clear()
        for cl in self.project.list_of_classes_model:
            #Kod służy do stworzenia customowego list itemu
            item = QListWidgetItem(self.view.class_list_widget) # dla każdej klasy cl tworzy nowy obiekt QListWidgetItem i przypisuje go do self.view.class_list_widget
            self.view.class_list_widget.addItem(item) # dodaje element item do widżetu listy
            row = CustomClassListItemView(cl,self) # tworzy nowy widok CustomClassListItemView
            item.setSizeHint(row.minimumSizeHint()) # ustawia rozmiar elementu item, aby pasował do minimalnego rozmiaru widoku row
            self.view.class_list_widget.setItemWidget(item, row) # ustawia widok row jako widok wewnętrzny dla item, co pozwala na dostosowany wygląd każdego elementu
        self.load_checkboxes_states()

    # Metoda która updejtuje obiekt klasy w ProjectModel
    def updateColorClass(self, Class, rgba):
        updatedClass = Class
        updatedClass.color = (rgba[0],rgba[1],rgba[2])
        self.project.updateClass(updatedClass)
        self.presenter.annotation_presenter.update_items()
        self.presenter.scene_presenter.get_annotations_from_project()
        self.presenter.scene_presenter.draw_annotations()

    # Metoda zwracająca listę obkietów Klass z zaznaczonym checkboxem hidden
    def getHiddenClass(self):
        checked_classes = []
        for index in range(self.view.class_list_widget.count()):
            item = self.view.class_list_widget.item(index)
            row_widget = self.view.class_list_widget.itemWidget(item)
            if row_widget.isHiddenChecked():
                checked_classes.append(row_widget.Class)

        result = copy.deepcopy(checked_classes)
        return result

    def save_checkboxes_states(self):
        # Lista[[Clasy z Hidden Checked],[Clasy z ToDelete Checked]]
        tmp_checkboxes_state = [[],[]]

        for index in range(self.view.class_list_widget.count()):
            item = self.view.class_list_widget.item(index)
            row_widget = self.view.class_list_widget.itemWidget(item)

            if row_widget.isHiddenChecked():
                tmp_checkboxes_state[0].append(row_widget.Class)

            if row_widget.isToDeleteChecked():
                tmp_checkboxes_state[1].append(row_widget.Class)

        print(tmp_checkboxes_state)
        self.checkboxes_state = tmp_checkboxes_state
        print(self.checkboxes_state)

    def load_checkboxes_states(self):
        for index in range(self.view.class_list_widget.count()):
            item = self.view.class_list_widget.item(index)
            row_widget = self.view.class_list_widget.itemWidget(item)

            # Sprawdzanie w całej liście
            if row_widget.Class in self.checkboxes_state[0]:
                row_widget.checkboxHidden.setChecked(True)
                print("Hidden")
            if row_widget.Class in self.checkboxes_state[1]:
                row_widget.checkboxToDelete.setChecked(True)
                print("ToDelete")