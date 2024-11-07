#Model obrazka (informacje o nazwie, rozmiarach, danych exif i adnotacjach)
class ImageModel:
    def __init__(self, image_id=None, filename="", width=0, height=0, exif_obj=None, list_of_annotations=None):
        self.image_id = image_id
        self.filename = filename
        self.width = width
        self.height = height
        self.exif_obj = exif_obj if exif_obj is not None else []
        self.list_of_annotations = list_of_annotations if list_of_annotations is not None else []

    #Metoda ktora aktualizuje sie zawsze po zmianie liczby adnotacji (dynamicznie) i umozliwia sprawdzenie czy są adnotacje
    #JESZCZE DO TESTÓW
    @property
    def has_annotation(self):
        return len(self.list_of_annotations) > 0