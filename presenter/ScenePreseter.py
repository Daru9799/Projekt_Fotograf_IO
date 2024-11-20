class ScenePresenter:
    def __init__(self):
        self.annotation_objects = [] #obiekty adnotacji
        self.polygons = [] #przechowuje liste dwuelementową (punkty, kolor)
        self.polygon_items = []

    def draw_annotations(self):
        #pobierz aktualnie zaznaczony obrazek (nazwa pliku)
        #pobierz obiekt aktualnie zaznaczonego obrazka (funkcja w projectModel)
        #zapisz do listy annotation_objects wszystkie adnotacje z listy adnotacji obrazka (obiekty)

        #pobierz współrzedne poligonów z obiektów adnotacji i ich kolory i zapisz do
        #nowej listy polygons (punkty, kolor)

        #na podstawie listy polygons narysuj poligony i dodaj kazdego z nich do listy referencji polygons_item
        #(aby mozna bylo usunac np.\jeden obiekt)
        pass
