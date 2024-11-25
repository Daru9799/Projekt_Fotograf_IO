from PyQt5.QtWidgets import QListWidgetItem

from model.AnnotationModel import AnnotationModel
from view.AnnotationListView import AnnotationListView

class AnnotationPreseter:
    def __init__(self, view, project):
        self.view = view
        self.project = project

    def add_annotation(self, points):
        selected_class = self.view.get_selected_class()
        selected_image_name = self.view.get_selected_image()  # Pobranie nazwy zaznaczonego obrazka
        img_obj = self.project.get_img_by_filename(selected_image_name)

        # Generowanie ID z uwzględnieniem klasy
        class_id = selected_class.Class.class_id
        annotation_id = self.create_new_id(img_obj, class_id)

        # Tworzenie nowej adnotacji
        new_annotation = AnnotationModel(
            annotation_id=annotation_id,
            area=points,
            class_id=class_id
        )

        # Dodanie i sortowanie adnotacji
        img_obj.list_of_annotations.append(new_annotation)
        img_obj.list_of_annotations.sort(key=lambda annotation: (annotation.class_id, annotation.annotation_id))


        # Aktualizacja widoku
        self.updateItems()

        # Debugging: wypisywanie informacji
        print("Nazwa pliku: " + img_obj.filename)
        for an in img_obj.list_of_annotations:
            print("Id anotacji: " + str(an.annotation_id))
            print("Punkty: " + str(an.segmentation))
            print("Klasa: " + str(an.class_id))

    def updateItems(self):
        # Pobranie nazwy zaznaczonego obrazka
        selected_image_name = self.view.get_selected_image()

        # Próba pobrania obiektu obrazu na podstawie nazwy
        img_obj = self.project.get_img_by_filename(selected_image_name)

        # Sprawdzenie, czy obrazek został znaleziony
        if img_obj is None:
            print("Błąd: Nie znaleziono obiektu obrazka.")
            return

        # Pobranie listy adnotacji z obiektu obrazka
        annotations_list = img_obj.list_of_annotations

        # Zablokowanie sygnałów, aby uniknąć nadmiarowego odświeżania
        self.view.annotation_list_widget.blockSignals(True)
        self.view.annotation_list_widget.clear()  # Usunięcie wszystkich elementów, aby uniknąć duplikatów

        # Dodanie wszystkich adnotacji do widoku
        for annotation in annotations_list:
            item = QListWidgetItem()
            row = AnnotationListView(annotation, self)  # Tworzenie widoku dla adnotacji
            color = self.project.get_color_by_class_id(annotation.class_id)
            class_name = self.project.get_name_by_class_id(annotation.class_id)
            row.set_color(color)
            row.set_class_name(class_name)
            item.setSizeHint(row.minimumSizeHint())  # Ustawienie rozmiaru elementu w liście
            self.view.annotation_list_widget.addItem(item)  # Dodanie elementu do listy
            self.view.annotation_list_widget.setItemWidget(item, row)  # Ustawienie widgetu dla danego elementu

        # Odblokowanie sygnałów
        self.view.annotation_list_widget.blockSignals(False)

    def create_new_id(self, img_obj, class_id):
        # Tworzy listę ID istniejących adnotacji dla danej klasy
        existing_ids = [
            annotation.annotation_id
            for annotation in img_obj.list_of_annotations
            if annotation.class_id == class_id
        ]

        # Znajduje najmniejsze brakujące ID w sekwencji dla danej klasy
        new_id = 1
        while new_id in existing_ids:
            new_id += 1

        return new_id

    # Usuwanie zaznaczonych adnotacji
    def delete_selected_annotations(self):
        # Pobranie wybranego obrazka i odpowiadającego mu obiektu
        selected_image_name = self.view.get_selected_image()  # Pobranie nazwy zaznaczonego obrazka
        img_obj = self.project.get_img_by_filename(selected_image_name)

        # Pobranie zaznaczonych adnotacji
        checked_annotations = self.get_checked_annotations()

        # Usunięcie zaznaczonych adnotacji z listy
        initial_count = len(img_obj.list_of_annotations)
        img_obj.list_of_annotations = [
            annotation for annotation in img_obj.list_of_annotations
            if annotation not in checked_annotations
        ]

        # Informacja o liczbie usuniętych adnotacji
        removed_count = initial_count - len(img_obj.list_of_annotations)
        print(f"Usunięto {removed_count} adnotacji z pliku: {img_obj.filename}")

        # Zaktualizowanie widoku
        self.updateItems()

    # Pobranie zaznaczonych adnotacji
    def get_checked_annotations(self):
        checked_annotations = []

        # Iterowanie po wszystkich elementach w QListWidget
        for index in range(self.view.annotation_list_widget.count()):
            item = self.view.annotation_list_widget.item(index)
            row_widget = self.view.annotation_list_widget.itemWidget(item)  # Pobranie widgetu AnnotationListView

            # Sprawdzenie, czy checkbox jest zaznaczony
            if row_widget.isChecked():
                checked_annotations.append(row_widget.getAnnotation())  # Dodanie obiektu adnotacji

        return checked_annotations

    