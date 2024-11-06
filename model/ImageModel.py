class ImageModel:
    #Kontruktor (bez argumentow tworzy pusty obiekt)
    def __init__(self, image_id=None, filename="", width=0, height=0, exif_obj=None, list_of_annotations=None):
        self.image_id = image_id
        self.filename = filename
        self.width = width
        self.height = height
        self.exif_obj = exif_obj if exif_obj is not None else []
        self.list_of_annotations = list_of_annotations if list_of_annotations is not None else []
        #Sprawdza czy lista adnotacji jest pusta i ustawia odpowiedni stan zmiennej boolowskiej has_annotation
        if not list_of_annotations:
            self.has_annotation = False
        else:
            self.has_annotation = True