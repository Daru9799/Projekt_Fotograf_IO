#Model obrazka (informacje o nazwie, rozmiarach, danych exif i adnotacjach)
import copy
class ImageModel:
    def __init__(self, image_id=None, filename="", width=0, height=0, exif_obj=None, list_of_annotations=None):
        self.image_id = image_id
        self.filename = filename
        self.width = width
        self.height = height
        self.exif_obj = exif_obj if exif_obj is not None else []
        self.list_of_annotations = list_of_annotations if list_of_annotations is not None else []

    #Metoda ktora aktualizuje sie zawsze po zmianie liczby adnotacji (dynamicznie) i umozliwia sprawdzenie czy są adnotacje
    @property
    def has_annotation(self):
        return len(self.list_of_annotations) > 0

    def zoom_change(self,value):
        self.zoom=value

    def get_zoom(self):
        return self.zoom

    def get_annotation_list(self):
        return copy.deepcopy(self.list_of_annotations)

    def set_annotation_list(self, list):
        self.list_of_annotations = list

    def get_annotation_size(self) -> int:
        return len(self.list_of_annotations)

    def get_exif_obj(self):
        return self.exif_obj

