from model.AnnotationModel import AnnotationModel

class AnnotationPreseter:
    def __init__(self, view):
        self.view = view

    # Dodawanie nowej adnotacji i dodanie jej do obiektu obrazka
    def add_annotation(self, points, project):
        selected_class = self.view.get_selected_class()
        selected_image_name = self.view.get_selected_image()  # wyciagam nazwe zaznaczonego obrazka
        img_obj = project.get_img_by_filename(selected_image_name)
        annotation_id = self.create_new_id(img_obj)
        new_annotation = AnnotationModel(annotation_id=annotation_id, area=points, class_id=selected_class.Class.class_id)
        img_obj.list_of_annotations.append(new_annotation)
        print("Nazwa pliku: " + img_obj.filename)
        for an in img_obj.list_of_annotations:
            print("Id anotacji: " + str(an.annotation_id))
            print("Punkty: " + str(an.segmentation))
            print("Klasa: " + str(an.class_id))

    #Szuka maksymalnego id wśród adnotacji i zwraca wartość+1 w przypadku pustej listy adnotacji zwraca 1
    def create_new_id(self, img_obj):
        if img_obj.list_of_annotations:
            max_id = max(annotation.annotation_id for annotation in img_obj.list_of_annotations if annotation.annotation_id is not None)
            return max_id + 1
        return 1