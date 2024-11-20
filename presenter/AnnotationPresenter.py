from model.AnnotationModel import AnnotationModel

class AnnotationPreseter:
    def __init__(self, view):
        self.view = view
        self.annotation_id = 0 #rozwiązanie tymczasowe

    # Dodawanie nowej adnotacji i dodanie jej do obiektu obrazka
    def add_annotation(self, points, project):

        selected_class = self.view.get_selected_class()
        new_annotation = AnnotationModel(annotation_id=self.annotation_id, area=points,
                                         class_id=selected_class.Class.class_id)
        self.annotation_id += 1
        selected_image_name = self.view.get_selected_image()  # wyciagam nazwe zaznaczonego obrazka
        img_obj = project.get_img_by_filename(selected_image_name)
        img_obj.list_of_annotations.append(new_annotation)
        print("Nazwa pliku: " + img_obj.filename)
        for an in img_obj.list_of_annotations:
            print("Id anotacji: " + str(an.annotation_id))
            print("Punkty: " + str(an.segmentation))
            print("Klasa: " + str(an.class_id))