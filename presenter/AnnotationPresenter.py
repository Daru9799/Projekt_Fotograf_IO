from PyQt5.QtWidgets import QListWidgetItem

from model.AnnotationModel import AnnotationModel
from view.AnnotationListView import AnnotationListView
import copy

class AnnotationPreseter:
    def __init__(self, view, presenter, project):
        self.view = view
        self.presenter = presenter
        self.project = project

    def add_annotation(self, points):
        points = copy.deepcopy(points)  # potrzebne bo generowało Bug'a
        selected_class = self.view.get_selected_class()

        img_obj = self.get_selected_image_obj()

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

    def updateItems(self):
        # Pobranie listy adnotacji z obiektu obrazka
        annotations_list = self.get_selected_image_obj().list_of_annotations

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

        # connection przy zmianie elem. listy
        self.view.annotation_list_widget.itemSelectionChanged.connect(self.onItemSelectionChanged)

        # Odblokowanie sygnałów
        self.view.annotation_list_widget.blockSignals(False)


    def onItemSelectionChanged(self):
        selected_items = self.view.annotation_list_widget.selectedItems()
        for item in selected_items:
            # Pobierz widget powiązany z elementem
            annotation_view = self.view.annotation_list_widget.itemWidget(item)

            # Sprawdzenie, czy widget istnieje i czy nie ma wybranego narzędzia do adnotacji
            if annotation_view and self.presenter.drawing_tool is None:
                polygon_segmentation = annotation_view.getAnnotation().get_segmentation()
                self.presenter.scene_presenter.set_seleted_polygon(polygon_segmentation)
                self.presenter.scene_presenter.draw_annotations()


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

    def delete_selected_annotations(self):
        # Pobranie obiektu obrazu dla wybranego obrazka
        img_obj = self.get_selected_image_obj()
        if img_obj is None:
            return

        # Pobranie zaznaczonych adnotacji
        checked_annotations = self.get_checked_annotations()

        # Jeśli nie zaznaczono żadnych adnotacji, wyświetl komunikat informacyjny
        if len(checked_annotations) == 0:
            self.view.show_message_OK("Informacja", "Zaznacz adnotację do usunięcia")
            return

        # Wyświetlenie okna potwierdzenia
        confirmation = self.view.show_message_Yes_No("Potwierdzenie",
                                                     "Czy na pewno chcesz usunąć zaznaczone adnotacje?")

        # Jeśli użytkownik potwierdzi usunięcie
        if confirmation:
            # Usunięcie zaznaczonych adnotacji z listy
            img_obj.list_of_annotations = [
                annotation for annotation in img_obj.list_of_annotations
                if annotation not in checked_annotations
            ]
            # Zaktualizowanie widoku po usunięciu
            self.updateItems()
            self.presenter.scene_presenter.refresh()



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

    def delete_annotations_by_class(self, class_id):
        img_obj = self.get_selected_image_obj()
        if img_obj is None:
            return

        img_obj.list_of_annotations = [
            annotation for annotation in img_obj.list_of_annotations
            if annotation.class_id != class_id
        ]

        # Zaktualizowanie widoku
        self.updateItems()

    def get_selected_image_obj(self):
        selected_image_name = self.view.get_selected_image()
        img_obj = self.project.get_img_by_filename(selected_image_name)
        if img_obj is None:
            print("Błąd: Nie znaleziono obiektu obrazka.")
            return None
        return img_obj





    