from PyQt5.QtCore import QObject

class RectanglePresenter(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.start_point = None
        self.end_point = None
        self.points = [] #w tym przypadku zwróci 4 punkty (wierzchołki prostokąta w liście)

    def draw_rectangle(self):
        # Tutaj bedzie cala logika rysowania obiektu na scenie a nastepnie zwrócenia punktów
        pass
        # zwraca liste punktow głównemu prezenterowi aby ten dodał adnotacje
        return self.points