import copy
#Model adnotacji
class AnnotationModel:
    def __init__(self, annotation_id=None, area=None, class_id = None):
        self.annotation_id = annotation_id
        self.segmentation = area #Zapis w formacie [(10, 20), (30, 40), (50, 20), (30, 10)]
        self.class_id = class_id

    def get_segmentation(self):
        return copy.deepcopy(self.segmentation)

    def set_segmentation(self, lista):
        cp_list = copy.deepcopy(lista)
        self.segmentation = cp_list


