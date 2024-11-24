from PyQt5.QtWidgets import QListWidgetItem

from model.AnnotationModel import AnnotationModel
from view.AnnotationListView import AnnotationListView

class AnnotationPreseter:
    def __init__(self, view, project):
        self.view = view
        self.project = project

    # Dodawanie nowej adnotacji i dodanie jej do obiektu obrazka
    def add_annotation(self, points):
        selected_class = self.view.get_selected_class()
        selected_image_name = self.view.get_selected_image()  # Wyciągam nazwę zaznaczonego obrazka
        img_obj = self.project.get_img_by_filename(selected_image_name)
        annotation_id = self.create_new_id(img_obj)
        new_annotation = AnnotationModel(annotation_id=annotation_id, area=points, class_id=selected_class.Class.class_id)
        img_obj.list_of_annotations.append(new_annotation)
        img_obj.list_of_annotations.sort(key=lambda annotation: annotation.annotation_id)  # Sortowanie po ID
        self.updateItems(img_obj.list_of_annotations)
        print("Nazwa pliku: " + img_obj.filename)
        for an in img_obj.list_of_annotations:
            print("Id anotacji: " + str(an.annotation_id))
            print("Punkty: " + str(an.segmentation))
            print("Klasa: " + str(an.class_id))

    def updateItems(self, annotations_list):
        self.view.annotation_list_widget.blockSignals(True)  # Zablokowanie sygnałów, aby uniknąć nadmiarowego odświeżania
        self.view.annotation_list_widget.clear()  # Usunięcie wszystkich elementów, aby uniknąć duplikatów
        for annotation in annotations_list:
            item = QListWidgetItem()
            row = AnnotationListView(annotation, self)  # Tworzenie widoku dla adnotacji
            print("ok")
            item.setSizeHint(row.minimumSizeHint())  # Ustawienie rozmiaru elementu w liście
            self.view.annotation_list_widget.addItem(item)  # Dodanie elementu do listy
            self.view.annotation_list_widget.setItemWidget(item, row)  # Ustawienie widgetu dla danego elementu
        self.view.annotation_list_widget.blockSignals(False)  # Odblokowanie sygnałów

    # Szuka maksymalnego ID wśród adnotacji i zwraca wartość+1, w przypadku pustej listy adnotacji zwraca 1
    def create_new_id(self, img_obj):
        # Tworzy listę wszystkich istniejących ID adnotacji
        existing_ids = [annotation.annotation_id for annotation in img_obj.list_of_annotations]

        # Znajduje najmniejsze brakujące ID w sekwencji
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
        self.updateItems(img_obj.list_of_annotations)

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
