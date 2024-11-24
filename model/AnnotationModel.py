#Model adnotacji
class AnnotationModel:
    def __init__(self, annotation_id=None, area=None, class_id = None,color=None):
        self.annotation_id = annotation_id
        self.segmentation = area #Tutaj prawdopodobnie zapis jako punkty w liście np. [(10, 20), (30, 40), (50, 20), (30, 10)]
        self.class_id = class_id
        self.color=color