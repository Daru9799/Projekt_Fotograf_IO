import cv2
import numpy as np
# Funkcja pomocnicza do rysowania poligonów
def draw_polygons(image, polygons):
    references = []  # Lista przechowująca referencje do poligonów
    for idx, points in enumerate(polygons):
        # Konwertuj punkty na odpowiedni format
        pts = np.array(points, np.int32).reshape((-1, 1, 2))
        # Rysuj poligon
        color = (0, 255 - idx * 50, 255)  # Zmienny kolor dla różnych poligonów
        thickness = 2  # Grubość linii
        cv2.polylines(image, [pts], isClosed=True, color=color, thickness=thickness)
        # Dodaj referencję do listy
        references.append({
            'id': idx,
            'points': points,
            'color': color,
            'thickness': thickness
        })
    return references

# Funkcja do usuwania poligonu
def remove_polygon(image, references, remove_id):
    # Filtruj referencje, usuwając poligon o podanym ID
    new_references = [ref for ref in references if ref['id'] != remove_id]
    # Stwórz czyste płótno
    image[:] = 0
    # Narysuj wszystkie pozostałe poligony
    for ref in new_references:
        pts = np.array(ref['points'], np.int32).reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, color=ref['color'], thickness=ref['thickness'])
    return new_references

# Utwórz pusty obraz (czarny)
height, width = 500, 500
image = np.zeros((height, width, 3), dtype=np.uint8)

# Definicja punktów dla kilku poligonów
polygons = [
    [(50, 50), (200, 50), (200, 200), (50, 200)],  # Kwadrat
    [(300, 100), (400, 50), (450, 150), (350, 200)],  # Czworokąt
    [(100, 300), (150, 350), (50, 450)]  # Trójkąt
]

# Narysuj poligony i zapisz referencje
references = draw_polygons(image, polygons)

# Wyświetl obraz początkowy
cv2.imshow('Polygons', image)
cv2.waitKey(0)

# Usuń jeden z poligonów, np. o `id=1`
references = remove_polygon(image, references, remove_id=1)

# Wyświetl obraz po usunięciu
cv2.imshow('Polygons After Removal', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Wydrukuj pozostałe referencje
print("Pozostałe poligony:")
for ref in references:
    print(ref)